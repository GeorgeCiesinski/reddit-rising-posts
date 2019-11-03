-- Set the app version
insert into app_control values ('1900-01-01', '0.0.1');

-- Insert the data for the praw_threads
insert into praw_thread (client_id, client_secret, username, password, user_agent) values
    ('nrE5x4yJ_LUo9Q', 'm8ItmlnLRlJ6GVVS1KD5tWsvhsQ', 'cussbot', 'SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS', 'reddit-rising-posts'),
    ('Zfl37rh1asVTjQ', 'DX87ZhsDhvJrvxdoud0CXmcbLGA', 'top10tracket', 'k2T%5VuSJc8k', 'reddit-rising-posts'),
    ('SCeO8pAeCeWO1A', 'bp_Y0jHbdPnjr_3xwaI6FsdosRc', 'top10tracker', 'J7PHXrUbSraxpcr1n5', 'reddit-rising-posts'),
    ('hikvCCL02WpVng', 'xKqtZbDyh0Nr7X-Ngr7TRI6yQJU', 'top10tracker1', 'u50AfEAgMT5Y00!fFTy7', 'reddit-rising-posts')
    ;

-- Populate a subreddit
insert into subreddit (name) values ('science');