# reddit-rising-posts

A bot that collects data on rising posts on Reddit as they either reach the front page, or stops rising for another reason. 

## Overview

### Purpose

The purpose of this project is to build a bot that monitors rising posts and collects
data for later analysis. 

### Screenshots and video

TBA

- Pics of consoles
- Gif of PostgresSQL receiving data
- Gifs showing project in action

## Features

TBA

- Expand on docker
- Multiprocessing
- etc.

## ChangeLog & Roadmap

TBA

- Start basic changelog from some working version. Maybe next master.
- Lay out vision for project future

## Project Directory

- config : All config files will be kept here
- Main executable scripts (the ones humans will run and or start) are kept at the project root
- bin : Usually used for compiled binaries, will be used for store python files that will be imported by the main script
  - bin/DAL : Data access layer scripts used to interact with the database
  - bin/sql : Sql file used to create or modify the database
  - bin/__init__.py : empty init script allowing the directory to be searchable for python modules
  - bin/Comment.py : Our own comment object. Given the reddit comment, will extract the necessary data, sanitize it for use
  - bin/CommentFunctions.py : Contains functions to retrieve comments from a given submission object. Creates the Comment objects
  - bin/Submission.py : Our own Submission object. Given the reddit submission, will extract the nessary data, sanitize it for use.
  - bin/SubmissionFunctions.py : Contains function to retrieve submissions from a given sub-reddit. Creates Submission objects.
  - bin/LIB.py : Lib object that contains commonly used functions in python. It standardises reading from config files (refer to config/config.cfg), writing to log/error files, and even reading/writing for files.
- bin/DataCollector.py : Started by RedditRisingPosts.py (talked about later) with a sub-reddit. It begins collecting submission data from the sub-reddit.
  - collect submissions from sub-reddit
  - collect comments from those submissions
  - upsert submissions and comments in to the database
  - request for sub-reddit submissions that are scheduled for data collection from the database
  - collect snapshot data from submissions
  - insert snapshots
  - request for sub-reddit comments that are scheduled for data collection from the database
  - collect snapshot data from comments
  - insert snapshots
  - start again from the top
- RedditRisingPosts.py : This is main of the application. Started as a service, it will connect to a database, open reddit praw connections, start data collectors for each monitored sub-reddit, and open a UDP port for application communication
  - crate praw connection q to be used as a pool for all data collectors to use
  - establish a database connection
  - create database connection q to be used as pool for all data collectors to use
  - get list of sub-reddits from the database
  - start data collectors (DataCollector.py) for each sub-reddit
  - start an application server on port 500
  - listen for incoming requests on the port.DataCollector
    - status, start <sub-reddit>, stop <sub_reddit>, stop
    - each client connection is treated as a transaction, client connects with request, server process the request and returns results to the client connection, the client connection is then closed.
            
## Credits

This bot was built by: 
- Anupam Sharma
- Robbie Toyota
- George Ciesinski  

With special thanks to: 
- The PRAW team for creating the PRAW api. 
