-- TODO: change inserts to use "using" https://dev.to/samuyi/a-primer-on-postgresql-stored-functions-plpgsql-1594

-- Find any subreddits, posts, and comments, that are scheduled too far into the future
create or replace function
	maint_correct_scrape_schedules()
returns void
as $$
begin
	-- subreddit schedule that is set too far ahead
	update
		subreddit
	set
		next_crawl = last_crawled + (snapshot_frequency * interval '1 second')
	where
		next_crawl > now() -- Test to see how well this improves the index
		and next_crawl > last_crawled + (snapshot_frequency * interval '1 second');

	-- subreddit schedule that has been running too long
	-- Finds a subreddit that has been assigned to a thread for crawling, and if it
	-- is due to be picked up for crawling again, then it will release and reschedule it
	update
		subreddit
	set
		-- Double the time since last_crawled.
		next_crawl = last_crawled + ((snapshot_frequency * 2) * interval '1 second'),
		-- Release the thread
		thread_assigned_on = null,
		thread_id = 0
	where
		thread_id > 0
		and thread_assigned_on + (snapshot_frequency * interval '1 second') < now();

	-- TODO: Do the above two updates for post, comment
	-- TODO: Check for long-running post_detail_queue and release it to be picked up again
end;
$$
language plpgsql;


-- Reset the subreddit crawling schedule
create or replace function
	subreddit_schedule_release
	(
		release_subreddit_name text default ''
	)
returns void
as $$
begin
	-- Reset all crawling
	if release_subreddit_name = '' then
		update
			subreddit
		set
			next_crawl = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			thread_id <> 0;
	-- Or only update one specific subreddit
	else
		update
			subreddit
		set
			next_crawl = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			name = release_subreddit_name;
	end if;
end;
$$
language plpgsql;


-- Reset the post crawling schedule
create or replace function
	post_control_release
	(
		release_id text default ''
	)
returns void
as $$
begin
	-- Reset all crawling
	if release_id = '' then
		update
			post_control
		set
			next_snap = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			thread_id <> 0;
	-- Or only update one specific post
	else
		update
			post_control
		set
			next_snap = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			post_id = release_id;
	end if;
end;
$$
language plpgsql;


-- Reset the comment crawling schedule
create or replace function
	comment_control_release
	(
		release_id text default ''
	)
returns void
as $$
begin
	-- Reset all crawling
	if release_id = '' then
		update
			comment_control
		set
			next_snap = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			thread_id <> 0;
	-- Or only update one specific comment
	else
		update
			comment_control
		set
			next_snap = now(),
			thread_id = 0,
			thread_assigned_on = null
		where
			comment_id = release_id;
	end if;
end;
$$
language plpgsql;


-- Reset the praw threads (on program start)
create or replace function
	praw_thread_release
	(
		release_thread_id int default 0
	)
returns void
as $$
begin
	-- Release all threads
	if release_thread_id = 0 then
		update
			praw_thread
		set
			released_on = now();

	-- Release only the specified thread, and update the app_control
	else
		-- Release the thread
		update
			praw_thread
		set
			released_on = now()
		where
			thread_id = release_thread_id;

		-- Update app_control to set the last_crawl
		update
			app_control
		set
			last_crawl = now();
	end if;
end;
$$
language plpgsql;



-- Get the praw credentials for initializing a new thread
create or replace function praw_login_get()
returns table
    (
        client_id			text,
        client_secret		text,
        username			text,
        password			text,
        user_agent			text
    )
as $$
declare
	_tid int; -- thread_id
begin
	-- Retrieve the praw login information
	_tid := (
		select
			thread_id
		from
			praw_thread
		where
			released_on > provided_on -- Make sure the thread is released
		order by
			released_on -- Get the thread that was released the longest time ago
		limit 1
	);

	-- Mark the praw login as "in use"
	update
		praw_thread
	set
		provided_on = now()
	where
		thread_id = _tid;

	-- Return the praw login
	return query
	select p.client_id, p.client_secret, p.username, p.password, p.user_agent
	from praw_thread p
	where thread_id=_tid;
end;
$$
language plpgsql;


-- Get the next subreddit to crawl
create or replace function
	subreddits_to_crawl_get
	(
		in tid int,
		in row_limit int
	)
returns table
	(
		subreddit_name text
	)
as $$
begin
	-- Pick the subreddits
	create temp table subreddits as
	select
		name
	from
		subreddit
	where
		next_crawl <= now()
		and thread_assigned_on is null
	order by
		next_crawl desc
	limit (row_limit);

	-- Claim the subreddits, in the name of tid!
	update
		subreddit
	set
		thread_id = tid,
		thread_assigned_on = now()
	from
		subreddits sr
		join subreddit p
			on (sr.name=p.name);

	-- Return the list of post_ids
	return query
	select name from subreddits;
end;
$$
language plpgsql;


-- Schedule a post to be scraped
create or replace function
	post_control_upsert
	(
		in pid /*post_id*/	text,
		in snap_freq	 	int
	)
returns void
as $$
begin
	-- Insert the row into post_control (if it doesn't exist)
	insert into
		post_control
		(post_id, snapshot_frequency)
	values
		(pid, snap_freq)
	on conflict on constraint post_control_pkey
		do update
		set
			snapshot_frequency=snap_freq;
end;
$$
language plpgsql;


-- Get the next set of posts to scrape
create or replace function
	post_control_get
	(
		in tid int,
		in row_limit int
	)
returns table
	(
		post_id text
	)
as $$
begin
	-- Pick the posts
	create temp table posts as
	select
		post_id
	from
		post_control
	where
		next_snap <= now()
		and thread_assigned_on is null
	order by
		next_snap desc
	limit (row_limit);

	-- Claim the posts, in the name of tid!
	update
		post_control
	set
		thread_id = tid,
		thread_assigned_on = now()
	from
		post_control pc
		join posts p
			on (pc.post_id=p.post_id);

	-- Return the list of post_ids
	return query
	select post_id from posts;
end;
$$
language plpgsql;


-- Insert a scraped summary
create or replace function
	post_snapshot_insert
	(
		in pid /*post_id*/	text,
		in tid				int,
		in rank				int,
		in upvotes			int,
		in downvotes		int,
		in comments			int,
		in is_hot			boolean
	)
returns void
as $$
declare 
	snapped timestamp := now();
begin
	-- Insert the snapshot
	insert into
		post_snapshot
		(post_id, thread_id, snapped_on, rank, upvotes, downvotes, comments, is_hot)
	values
		(pid, tid, snapped, rank, upvotes, downvotes, comments, is_hot);

	-- Release the post for another thread to snap it again
	update
		post_control
	set
		thread_id = 0,
		thread_assigned_on = null,
		last_snap = snapped,
		next_snap = snapped + (snapshot_frequency * interval '1 second')
	where
		post_id = pid;
end;
$$
language plpgsql;


-- Insert a row into the post_detail_control queue
create or replace function
	post_detail_control_insert
	(
		in pid /*post_id*/	text
	)
returns void
as $$
begin
	-- Insert the row if it does not exist
	insert into
		post_detail_control
		(post_id)
	values
		(pid)
	on conflict
		(post_detail_control_pkey)
		do nothing;
end;
$$
language plpgsql;


-- Select a list of posts that need to be scraped for their details
create or replace function
	post_detail_control_get
	(
		in tid 			int,
		in row_limit	int
	)
returns void
as $$
begin
	-- Get the posts to get the details for
	create temp table posts as
	select
		post_id
	from
		post_detail_control
	order by
		inserted_on
	limit (row_limit);

	-- Claim those posts
	update
		post_detail_control
	set
		thread_id = tid,
		thread_assigned_on = now()
	where
		post_id in (select post_id from posts);
end;
$$
language plpgsql;


-- Upsert a row into post_details
create or replace function
	post_details_upsert
	(
		in in_pid /*post_id*/	text,
		in in_subreddit_id 		text,
		in in_posted_by_id		int,
		in in_title				text,
		in in_body				text,
		in in_posted_on			timestamp
	)
returns void
as $$
begin
	-- Upsert the row into post_detail
	insert into
		post_detail
		(post_id, subreddit_id, posted_by, title, body, posted_on)
	values
		(in_pid, in_subreddit_id, in_posted_by_id, in_title, in_body, in_posted_on)
	on conflict
		(post_detail_pkey)
		do
		-- Perform the update, if required
		update
		set
			subreddit_id = excluded.subreddit_id,
			title = excluded.title,
			body = excluded.boy,
			updated_on = now()
		where
			post_id = in_pid;

	-- TODO: Upsert the row into the user table (upsert instead of insert, in case user changes name)
	-- TODO: Make this into a function itself


	-- Remove the post from the queue
	delete from
		post_detail_control
	where
		post_id = in_pid;
end;
$$
language plpgsql;


-- Calculate (sync) the summarized columns in post_detail from the snapshots
create or replace function
	maint_post_detail_sync
	(
		in pid /*post_id*/	text
	)
returns void
as $$
begin
	update
		post_detail
	set
		-- Set the last_snapped to the latest snapshot
		last_snapped = coalesce(
			-- First, check the live post_snapshot table
			(select max(snapped_on) from post_snapshot where post_id=pid),
			-- Second (if not found), check the archived post_snapshot table
			(select max(snapped_on) from post_snapshot_archived where post_id=pid),
			-- Finally (else), leave with the original value
			last_snapped
		)
	where
		post_id = pid;
end;
$$
language plpgsql;


-- Archive a post
create or replace function
	archive_post
	(
		in pid /*post_id*/	text
	)
returns void
as $$
begin
	-- TODO: Mark the post_detail as archived
	-- TODO: Move the post_snapshots to archive
	-- TODO: Mark the comment_detail as archived
	-- TODO: Move the comment_snapshots to archive
	-- TODO: Make the comment archival an individual function
end;
$$
language plpgsql;