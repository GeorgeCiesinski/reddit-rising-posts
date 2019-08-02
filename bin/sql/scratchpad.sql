/*
23.233.33.158
5432
reddit-rising-posts
s3cr3t
psql -h 23.233.33.158 -p 5432 -U reddit-rising-posts postgres
*/



/*
Thread 1: Get list of threads as a snapshot
Thread 2: Go through the post_control for any posts without a detail, and populate it
Thread 3: Go through the comments in comment_control that don't have a detail, and populate it
*/



/*
VW - Give a list of subreddits to crawl (next_snap)
VW - Give a list of posts to crawl whose next_snap is earlier than its parent subreddit next_snap (higher frequency)
VW - Give a list of comments to crawl whose next_step is earlier than its parent post next_snap (higher frequency)
SP - Accept snapshot details about a post
SP - Accept snapshot details about a comment
VW - Give a list of posts to get the details for (in snapshot, but not in detail)
SP - Accept post details
VW - Give a list of comments to get the details for (in snapshot, but not in detail)
SP - Accept comment details
VW - Give a list of active posts that are no longer hot for a given subreddit (post.last_snapped < subreddit.last_snapped), to do one final snap, then archive
SP - Archive a post (and its comments)
*/













/*
============
Okay, I'm going to go into a short info dump for some ideas I had for how we could go about __collecting__ the data. We should meet up next week to go over it in person, but I want this info available to lay the foundation in your minds (don't worry if you don't read it, or if this is confusing right now).

Most of the program's flow will be controlled by the database (because I want my role to look really cool and important). By that, I mean the program will query the database to get the instructions of what data to go get snapshots of, rather than having it hard coded.

I'll give a super high level overview of the program's steps (in relation to the database), and then outline the tables real quick (the tables are less important).

__A few notes as a preface:__
 - I might say "me" when referring to database tasks, and "you guys" for Python tasks, but I do want to be involved in the Python, and I'm sure you guys want to build experience in SQL.
 - I refer to the collecting of data as a "snapshot" or "crawling". When you check a subreddit for posts, you "crawl" it. When you check a post to see its comments and stuff, you're taking a "snapshot", or "scraping" it.
 - This program will, without a doubt, need to be multithreaded. At the database level, this will create some potential conflicts, race conditions, and needlessly repeated work, but since this is database driven, it'll be on me to sort that out. Right now I envision one thread per subreddit being crawled. Eg we might have 20 threads going, which are cycling through subreddits to crawl.
 - Some of the threads will need to be doing different tasks - not just crawling a subreddit. I refer to this a "branches" of the program, since I can't put my finger on the right term. But each branch will be running in parallel with the each other; just doing different tasks.
 - So far in my planning, it looks like all interactions with the database will be done via views (pre-built queries) and stored procedures (functions written in SQL that run on the database), rather than direct queries in Python.
 - I've split the tables into the "details" (the title, the body, the post date, summary count of votes, etc) and the "snapshot" (the number of comments/votes/etc at the time of the snapshot)
 - Anu wants to be able to take snapshots of individual posts at any given interval, so that adds a bit of complexity. Eg if we crawl subreddits every 30 minutes, but a specific post every 15 minutes, we need seperate logic to check these posts. This is a major concern for multithreaded race conditions that can result in extra processing (eg we don't want it to scrape the post using Python thread 1, if thread 2 is in the middle of crawling the subreddit that contains the post). My assumption right now is that there will be very few of these post "override" timers, and the vast majority of the posts will be scraped when their parent subreddit gets crawled.

__Program flow (from the database perspective):__
Branch 1: Crawling subreddits
 - A Python thread requests a single subreddit to crawl from the database.
 - API returns a list of all posts for that subreddit
 - Python sends the post's _snapshot info_ to the DB (not the full post info - you'll see why, below. This is to keep things lean and fast)
 - API returns a list of the comments for that post
 - Python sends the comment _snapshot info_ to the DB (again, not the full info), for whichever comments we want to track.

Branch 2: Scraping individual posts, outside of the subreddit's schedule
 - A Python thread requests a list of posts that need to be scraped (the number of posts in the list is limited, to allow for multithreading to get multiple different lists)
 - API returns the information about the post
 - Same data gets scraped and sent to the DB as in Branch 1 (only the snapshot; not the post details)

Branch 3: Populate details
 - A python thread will request a list of posts that have a snapshot but no details (ie: posts that have JUST appeared on the hot list, and have not had their details collected yet)
 - API returns the post details and the comments
 - Python sends the _post details_ (title, body, etc) to the database for insertion
 - Python sends the _comment details_ for the comments in the post to the database. I'm not sure if comment collection should be a seperate branch, but you get the idea.
 - Possibly repeat this for posts that need to be updated? I don't know if we care if a post gets edited while it's still in process of rising. See the "archiving" branch below.

Branch 4: Archive posts that are no longer hot. (Keep the tables with active data clean and fast)
 - A Python thread will request a list of posts from the DB that belong to a subreddit that has been crawled, but did not get scraped. (In other words, it's not hot anymore)
 - API returns the post details and comments about the post
 - Python writes back the _snapshot info_ for both the post and the relevant comments
 - Python also writes back the _post/comment details_, one final time. This is will be the final time that it is automatically checked for the details. An update can be forced though.
 - Python sends a command to the DB to archive the post (this removes the post from the tables that we need to keep small for efficiency, and into the "read only" tables)


__Main tables:__

 - subreddit_control - A list of all subreddits that we want to crawl, and their crawl schedule and crawl status.
 - post_control - A list of all active ("hot") posts, and their scrape schedules and scrape status.
 - comment_control - Same as above, but for comments

 - post_snapshot - Contains a row for each "snapshot" of a post that is active ("hot"). Contains the post ID, the datetime of the snap, and the metrics.
 - comment_snapshot - Same as above, but for comments.
 - post_snapshot_archive - Same as the above, but for posts that are no longer active. Inserting into a small table with few indexes (the above tables) is faster than this large, indexed, reading table.
 - comment_snapshot_archive - Again, the same as above, but for comments.

 - post_detail - Contains a row for each post, with the details (title, post date, body, etc) and summary count (total votes, peak rank, etc). But the summaries are only updated on demand, rather than with every snapshot, for efficiency.
 - comment_detail - Same as above.


That's it for tonight. I was going to feed my tables into that dbdiagram, but it requires its own non-SQL syntax, and it's getting too late in the evening to deal with that.

...Now that I've typed all this out, I should definitely clean it a bit and put it in a google doc. Let's discuss it in person first.
*/