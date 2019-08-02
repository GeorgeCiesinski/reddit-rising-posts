-- Set the app version
insert into app_control values ('1900-01-01', '0.0.1');

-- Insert the data for the praw_threads
insert into praw_thread (client_id, client_secret, username, password, user_agent)
	values ('nrE5x4yJ_LUo9Q', 'm8ItmlnLRlJ6GVVS1KD5tWsvhsQ', 'cussbot', 'SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS', 'cussbot by /u/th1nker');

-- Populate a subreddit
insert into subreddit (name) values ('science');