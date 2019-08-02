/*
Install the tables
*/

-- Single-row table to control the app's state
create table app_control
(
	last_crawl 			timestamp,
	app_version			text
);



-- Keep track of active threads
create table praw_thread
(
	thread_id			serial primary key,
	client_id			text,
	client_secret		text,
	username			text,
	password			text,
	user_agent			text,
	provided_on			timestamp default '1900-01-01',
	released_on			timestamp default now(),
	inserted_on			timestamp default now()
);


-- Lookup table of users (for posted_by columns)
create table reddit_user
(
	user_id				text not null primary key,
	name 				text,
	inserted_on			timestamp default now()
);
create index reddit_user_idx_name on reddit_user (name);


-- Both a control and lookup table for the subreddits
create table subreddit
(
	subreddit_id		text,
	thread_id			int default 0,
	thread_assigned_on	timestamp default null,
	name 				text primary key,
	snapshot_frequency	int default 300,
	last_crawled		timestamp default now(),
	next_crawl			timestamp default now(),
	crawl_status		char(1) default 'Q', -- Q = queued up; otherwise, store an identifier for which Python thread is doing the crawl
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index subreddit_idx_id on subreddit (subreddit_id);
create index subreddit_idx_crawl on subreddit (next_crawl);


-- Control table for posts that are actively being monitored
create table post_control
(
	post_id 			text not null primary key,
	thread_id			int default 0,
	thread_assigned_on	timestamp default null,
	snapshot_frequency	int default 300,
	last_snap			timestamp default null,
	next_snap			timestamp default now(),
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index post_control_idx_next_snap on post_control (next_snap);
create index post_control_idx_assigned_on on post_control (thread_assigned_on);


create table post_detail_control
(
	post_id				text not null primary key,
	thread_id			int default 0,
	thread_assigned_on	timestamp default null,
	inserted_on			timestamp default now()
);
create index post_detail_control_idx_ins on post_detail_control (inserted_on);


-- Control table for comments that are actively being monitored
create table comment_control
(
	comment_id			text not null primary key,
	thread_id			int default 0,
	thread_assigned_on	timestamp default null,
	snapshot_frequency	int default 300,
	last_snap			timestamp default null,
	next_snap			timestamp default now(),
	snap_status			char(1) default 'Q',
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index comment_control_idx_crawl on comment_control (next_snap);

create table comment_detail_control
(
	post_id				text not null primary key,
	thread_id			int default 0,
	thread_assigned_on	timestamp default null,
	inserted_on			timestamp default now()
);
create index comment_detail_control_idx_ins on comment_detail_control (inserted_on);


-- Snapshot details for posts being actively monitored
create table post_snapshot
(
	post_id 			text,
	thread_id			int,
	snapped_on			timestamp,
	rank				int,
	upvotes				int,
	downvotes			int,
	comments 			int,
	is_hot				boolean,
	primary key (post_id, snapped_on)
);


-- Snapshot details for posts are no longer being monitored
create table post_snapshot_archive
(
	post_id 			text,
	thread_id			int,
	snapped_on			timestamp,
	rank				int,
	upvotes				int,
	downvotes			int,
	comments 			int,
	is_hot				boolean,
	primary key (post_id, snapped_on)
);


-- Snapshot details for comments being actively monitored
create table comment_snapshot
(
	comment_id 			text,
	thread_id			int,
	snapped_on			timestamp,
	rank				int,
	upvotes				int,
	downvotes			int,
	replies 			int,
	primary key (comment_id, snapped_on)
);


-- Snapshot details for posts are no longer being monitored
create table comment_snapshot_archive
(
	comment_id 			text,
	thread_id			int,
	snapped_on			timestamp,
	rank				int,
	upvotes				int,
	downvotes			int,
	replies 			int,
	primary key (comment_id, snapped_on)
);


-- Details about the posts
create table post_detail
(
	post_id				text not null primary key,
	subreddit_id		text,
	posted_by			int,
	title				text,
	body				text,
	posted_on			timestamp,
	last_snapped		timestamp default null,
	archived			timestamp default null,
	inserted_on			timestamp default now(),
	updated_on			timestamp default now()
);
create index post_detail_idx_posted_on on post_detail (posted_on);
create index post_detail_idx_subreddit on post_detail (subreddit_id);


-- Details about the comments
create table comment_detail
(
	comment_id		text not null primary key,
	post 			int,
	parent_comment	int default 0,
	body			text,
	replies			int,
	posted_by		int,
	posted_on		timestamp,
	last_snapped	timestamp default null,
	archived		timestamp default null,
	inserted_on		timestamp default now(),
	updated_on		timestamp default now()
);
create index comment_detail_idx_parent on comment_detail (parent_comment);

grant all privileges on all tables in schema public to rr_pool;
select 'drop table '||tablename||';' from pg_catalog.pg_tables where schemaname='public';