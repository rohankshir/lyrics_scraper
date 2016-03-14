# Purpose

This is a tool to help in the acquisition of song metadata and lyrics. It has two facets: 
* Fetching the top songs in the Billboards playlist for the genre and time period of the user's choice
* Fetching the lyrics of a song based on the title and artist information from (genius.com)[genius.com]

# Usage

`create_corpus.sh` combines the two functionalities together to build a corpus of lyrics into your local file system. It has a few different parameters:
1. The Billboard Chart you want to get the songs from. This chart info can be found by browsing [billboard.com](billboard.com) and finding the chart of interest by looking at the suffix of the URL, such as suffix 'r-b-hip-hip-songs' in the URL [http://www.billboard.com/hip-hop-rap-r-and-b](http://www.billboard.com/hip-hop-rap-r-and-b).

2. The number of songs you want to download from each year of the given Billboard

3. The years for which you want to fetch songs from. This is baked into the for loop `seq 2000 2015` which means from the years 2000 to 2015, download me the top 300 songs for the `r-b-hip-hop-songs`.


# Dependencies

The `create_corpus.sh` depends on `gnu parallel` for efficiency's sake but can easily not be by commenting out the line that usages `parallel` and uncommenting the while loop. 

The scraper, [`genius.rb`](genius.rb), is written in ruby and depends on all the third party gems listed in the [Gemfile](Gemfile).

The Billboard song fetcher is written in Python 2.7 and depends on [`billboard`](https://github.com/guoguo12) API, which can be installed using `pip`. 
