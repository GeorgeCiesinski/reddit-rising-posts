/*
Install the tables
*/



/*
App and lookup tables
*/
create table app_control
(
	app_version			text
);


create table praw_login
(
	client_id			text primary key,
	client_secret		text,
	username			text,
	password			text,
	user_agent			text,
	provided_on			timestamp default '1900-01-01',
	released_on			timestamp default now(),
	inserted_on			timestamp default now()
);


create table reddit_user
(
	id					serial,
	name 				text unique,
	inserted_on			timestamp default now()
);


-- Both a control and lookup table for the subreddits
create table subreddit
(
    subreddit_id		serial,
    name 				text primary key,
    assigned_on	        timestamp default null,
    snapshot_frequency	int default 300,
    last_crawled		timestamp default now(),
    next_crawl			timestamp default now(),
    inserted_on			timestamp default now(),
    updated_on			timestamp default now()
);
create index subreddit_idx_id on subreddit (subreddit_id);
create index subreddit_idx_crawl on subreddit (next_crawl);



/*
 Submissions
*/
-- Control table for submissions that are actively being monitored
create table submission_control
(
	submission_id 		text not null primary key,
	assigned_on	        timestamp default null,
	snapshot_frequency	int default 300,
	last_snap			timestamp default null,
	next_snap			timestamp default now(),
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index submission_control_idx_next_snap on submission_control (next_snap);
create index submission_control_idx_assigned_on on submission_control (assigned_on);
create index submission_control_idx_inserted_on on submission_control (inserted_on);


-- Details about the submissions
create table submission_detail
(
	submission_id		text not null primary key,
	subreddit_id		int,
	posted_by			int,
	title				text,
	url                 text,
	posted_on			timestamp,
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index submission_detail_idx_posted_on on submission_detail (posted_on);
create index submission_detail_idx_subreddit on submission_detail (subreddit_id);


-- Snapshot details for submissions being actively monitored
create table submission_snapshot
(
	submission_id 		text,
	snapped_on			timestamp,
	score				int,
	num_comments 		int,
	upvote_ratio        float,
	primary key (submission_id, snapped_on)
);



grant all privileges on all tables in schema public to rr_pool;
-- select 'drop table '||tablename||';' from pg_catalog.pg_tables where schemaname='public';