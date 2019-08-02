/*
-- This is done manually
create database
	reddit_rising
with
	encoding='UTF8'
	connection limit=-1;
*/

create role
	rr_pool
with
	encrypted password 'SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS';

alter role
	rr_pool
with
	login;