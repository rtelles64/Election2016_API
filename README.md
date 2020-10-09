# 2016 US Presidential Election API

The 2016 Election API delivers data that is clean and easy to use from the 2016 US Presidential Election.

Here is a [presentation](https://docs.google.com/presentation/d/1YibLy1wAP1ENraETwLsrkM0p3E9VuM430oiiU5SVvA8/edit?usp=sharing) to check it out!

## Introduction

There were a lot of emotions broiling in the events leading up to the 2016 Presidential election. These emotions came to fruition following the election.

Authors and journalists, among others, may want to gain insight on the positive and negative reactions to these events. They may alaso want to asses the risks of these events and would want to generate a list of article URLs within these parameters.

### Problem

The problem, though, is that the data provided by the GDELT project covers global events and doesn't contain column headers, nor does it enforce type constraints.

### Solution

As a solution, the Election API delivers GDELT data in a more usable format. The API will deliver just the data from January 2016 to September 2020, as well as events pertaining only to the US.

## Architecture

The data stack used in this project is as follows:

- S3: For raw data storage
- Spark: For data processing/cleaning
- PostgreSQL: For data modeling
- Flask: Frontend API delivery

## Dataset

The dataset used for this project is the [GDELT Project](https://www.gdeltproject.org) dataset, specifically in the US, from January 2016 to September 2020.

### Final Dataset

The final dataset will contain relevant headers. It will also extract useful information such as the Goldstein Scale which indicates an event's impact, and Average Tone which indicates how the event was perceived.

## Engineering Challenges

### Dynamic Table Changes

I needed a way to dynamically query specific tables in the database based on what URL the user was visiting. A solution to this challenge was solved by switching to Object Relational Mapping (ORM), which enabled targeted querying within one table.

### Simple Reads

A simple read using at first a (cleaned) master table, limited to 10 rows, took 5 minutes! This limited the API's availability, which meant the API wasn't available until after the data was loaded.

What I ended up having to do was separate my master table into individual tables based on specific actors. Switching to the ORM model granted 5 second query times, which was a 99% improvement.

