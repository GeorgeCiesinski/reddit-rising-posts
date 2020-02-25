-- TODO: change inserts to use "using" https://dev.to/samuyi/a-primer-on-postgresql-stored-functions-plpgsql-1594

/* Util */

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

-- Calculate (sync) the summarized columns in post_detail from the snapshots
create or replace function
	maint_submission_detail_sync
	(
		_sid	text
	)
returns void
as $$
begin
	update
		submission_detail
	set
		-- Set the last_snapped to the latest snapshot
		last_snapped = coalesce(
			-- First, check the live post_snapshot table
			(select max(snapped_on) from submission_snapshot where submission_id=_sid),
			-- Second (if not found), check the archived post_snapshot table
			(select max(snapped_on) from submission_snapshot_archived where submission_id=_sid),
			-- Finally (else), leave with the original value
			last_snapped
		)
	where
		submission_id = _sid;
end;
$$
language plpgsql;


/* Reset claimed rows */

create or replace function subreddit_schedule_release
	(
		_subreddit_name text default ''
	)
returns void
as $$
begin
	-- Reset all crawling
	if _subreddit_name = '' then
		update
			subreddit
		set
			next_crawl = last_crawled + (snapshot_frequency || ' seconds')::interval,
			assigned_on = null
		where
			assigned_on is not null;
	-- Or only update one specific subreddit
	else
		update
			subreddit
		set
			next_crawl = last_crawled + (snapshot_frequency || ' seconds')::interval,
			assigned_on = null
		where
			name = _subreddit_name;
	end if;
end;
$$
language plpgsql;

-- Reset the post crawling schedule
create or replace function submission_schedule_release
(
	_release_id text default ''
)
returns void
as $$
begin
	-- Reset all crawling
	if _release_id = '' then
		update
			submission_control
		set
			assigned_on = null
		where
			assigned_on is not null;
	-- Or only update one specific post
	else
		update
			submission_control
		set
			assigned_on = null
		where
			submission_id = _release_id;
	end if;
end;
$$
language plpgsql;

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

-- Reset the praw logins (on program start)
create or replace function praw_login_release
(
	_login_id int default 0
)
returns void
as $$
begin
	-- Release all threads
	if _login_id = 0 then
		update
			praw_login
		set
			released_on = now();
	-- Release only the specified thread, and update the app_control
	else
		-- Release the thread
		update
			praw_login
		set
			released_on = now()
		where
			thread_id = _login_id;
	end if;
end;
$$
language plpgsql;

/* Get a PRAW login */

-- Retrieve one login of
create or replace function praw_login_get ()
returns table
(
	client_id text, client_secret text, username text, password text, user_agent text
)
as $$
begin
	-- Retrieve the praw login information
	return query
	with cid as (
		select p.client_id
		from praw_login p
		where released_on > provided_on -- Make sure the thread is released
		order by released_on -- Get the thread that was released the longest time ago
		limit 1
	)
	-- Mark the praw login as "in use"
	update praw_login p
	set	provided_on = now()
	from cid
	where p.client_id = cid.client_id
	returning p.client_id, p.client_secret, p.username, p.password, p.user_agent;
end;
$$
language plpgsql;


/* Retrieve scheduled content to scrape */

-- Get the next subreddit to crawl
create or replace function subreddits_to_crawl_get
(
	_row_limit int
)
returns table
(
	name text,
	last_crawled timestamp
)
as $$
begin
	return query
	with sr as (
		-- Pick the subreddits
		select s.name, s.last_crawled
		from subreddit s
		where
			s.next_crawl <= now()
			and s.assigned_on is null
		limit (_row_limit)
	)
	-- Claim the subreddits
	update subreddit
	set	assigned_on = now()
	from
		subreddit p
		join sr
			on (sr.name=p.name)
	returning p.name, p.last_crawled;
end;
$$
language plpgsql;

create or replace function submission_control_get
(
	_row_limit int
)
returns table
(
	id text
)
as $$
begin
	return query
	with s_id as (
		select t.submission_id
		from submission_control t
		where
			t.next_snap <= now()
			and t.assigned_on is null
		order by
			t.next_snap desc
		limit (_row_limit)
		for update
	)
	update submission_control s
	set assigned_on = now()
	from s_id
	where s.submission_id=s_id.submission_id
	returning s.submission_id as id;
end;
$$
language plpgsql;


/* Submission */

create or replace function
	submission_snapshot_insert
(
	_sid			text,
	_score			int,
	_num_comments	int,
	_upvote_ratio   float
)
returns void
as $$
begin
	-- Insert the snapshot
	insert into submission_snapshot
		(submission_id, snapped_on, score, num_comments, upvote_ratio)
	values 
		(_sid, now(), _score, _num_comments, _upvote_ratio);

	-- Release and update the schedule table to mark when the last snapshot was scraped
	update submission_control t
	set
	    last_snap = now(),
		assigned_on = null
	where submission_id = _sid;
end;
$$
language plpgsql;

-- Reschedule the submission (with the new frequency, if supplied)
create or replace function
	reschedule_submission
(
	_sid			text,
	_snapshot_frequency int=null,
	_next_crawl		timestamp=null
)
returns void
as $$
begin
	-- Update the detail table to reschedule it (with the new frequency, if supplied)
	update submission_control t
	set
		snapshot_frequency = coalesce(_snapshot_frequency, t.snapshot_frequency),
		next_snap = last_snap + (coalesce(_next_crawl, t.next_crawl) || ' seconds')::interval
	where submission_id = _sid;
end;
$$
language plpgsql;

-- Schedule a post to be scraped
create or replace function submission_control_upsert
(
	_sid			text,
	_snap_freq	 	int = 300,
	_next_snap	  	timestamp = null
)
returns void
as $$
begin
	-- Insert the row into post_control (if it doesn't exist)
	insert into submission_control as t
		(submission_id, snapshot_frequency, next_snap)
	values
		(_sid, _snap_freq, coalesce(_next_snap, (now() + (_snap_freq * interval '1 second'))))
	on conflict on constraint submission_control_pkey
		do update
		set
			snapshot_frequency = _snap_freq,
			next_snap = coalesce(
				_next_snap,
				(
					coalesce(t.last_snap, now())
					+ (_snap_freq * interval '1 second')
				)
			);
end;
$$
language plpgsql;

-- Upsert a row into post_details
create or replace function submission_detail_upsert
	(
		_sid				text,
		_subreddit_name		text,
		_posted_by			text,
		_title				text,
		_posted_on			timestamp,
		_url				text
	)
returns void
as $$
begin
	-- Upsert the row into post_detail
	with subreddit_insert as (  -- Try to insert the subreddit if it does not already exist
        insert into subreddit (name)
        values (_subreddit_name)
        on conflict on constraint subreddit_pkey do nothing
	    returning subreddit_id
	),
	sr_id as (  -- Get the ID of the subreddit (either existing, or newly inserted)
		select subreddit_id as id from subreddit_insert  -- Newly inserted
	    union all
	    select subreddit_id as id from subreddit where name=_subreddit_name
	),
	user_insert as (  -- Try to insert the user if they do not already exist
        insert into reddit_user (name)
        values (_posted_by)
        on conflict on constraint reddit_user_name_key do nothing
	    returning id
	),
	user_id as (  -- Get the ID of the user (either existing, or newly inserted)
		select id from user_insert  -- Newly inserted
	    union all
	    select id from reddit_user where name=_posted_by
	)
	insert into submission_detail as pd
		(submission_id, subreddit_id, posted_by, title, posted_on, url)
	values
		(_sid, (select id from user_id), (select id from sr_id), _title, _posted_on, _url)
	on conflict on constraint submission_detail_pkey do
		update
		set
			subreddit_id = excluded.subreddit_id,
			title = excluded.title,
			updated_on = now()
		where
			pd.submission_id = _sid
			and pd.subreddit_id <> excluded.subreddit_id
			and pd.title <> excluded.title;

	-- TODO: Upsert the row into the user table (upsert instead of insert, in case user changes name)
	-- TODO: Query to get the subreddit_id (this function accepts the subreddit name)
end;
$$
language plpgsql;

/* Comment */

-- Upsert a row into comment_details
create or replace function comment_detail_upsert
(
	_comment_id	 text,
	_submission_id  text,
	_posted_on	  timestamp
)
returns void
as $$
begin
	-- Upsert the row into detail
	insert into comment_detail as d
		(comment_id, submission_id, posted_on)
	values
		(_comment_id, _submission_id, _posted_on)
	on conflict on constraint comment_detail_pkey
		do nothing;
end;
$$
language plpgsql;

-- Insert a scraped summary
create or replace function comment_snapshot_insert
(
	_comment_id	 text,
	_score		  int
)
returns void
as $$
begin
	-- Insert the snapshot
	insert into comment_snapshot
		(comment_id, score, snapped_on)
	values
		(_comment_id, _score, now());

	-- Release and update the schedule table to mark when the last snapshot was scraped
	update comment_control
	set
	    last_snap = now(),
	    assigned_on = null
	where comment_id = _comment_id;
end;
$$
language plpgsql;

-- Reschedule the submission (with the new frequency, if supplied)
create or replace function
	reschedule_comment
(
	_id				text,
	_snapshot_frequency int=null,
	_next_crawl		timestamp=null
)
returns void
as $$
begin
	-- Update the detail table to reschedule it (with the new frequency, if supplied)
	update comment_control t
	set
		snapshot_frequency = coalesce(_snapshot_frequency, t.snapshot_frequency),
		next_snap = last_snap + (coalesce(_next_crawl, t.next_snap) || ' seconds')::interval
	where comment_id = _id;
end;
$$
language plpgsql;

-- Schedule a post to be scraped
create or replace function comment_control_upsert
(
	_id			text,
	_snap_freq	 	int = 300,
	_next_snap	  	timestamp = null
)
returns void
as $$
begin
	-- Insert the row into post_control (if it doesn't exist)
	insert into comment_control as t
		(comment_id, snapshot_frequency, next_snap)
	values
		(_id, _snap_freq, coalesce(_next_snap, (now() + (_snap_freq * interval '1 second'))))
	on conflict on constraint comment_control_pkey
		do update
		set
			snapshot_frequency = _snap_freq,
			next_snap = coalesce(
				_next_snap,
				(
					coalesce(t.last_snap, now())
					+ (_snap_freq * interval '1 second')
				)
			);
end;
$$
language plpgsql;


/* Archiving */


-- Archive a post
create or replace function
	archive_post
	(
		_pid /*post_id*/	text
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