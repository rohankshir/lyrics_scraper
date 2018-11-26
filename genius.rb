#!/usr/bin/ruby
# coding: utf-8
require 'rubygems'
require 'bundler/setup'
Bundler.require

require 'genius'
require 'nokogiri'
require 'open-uri'
require 'similar_text'

def sanitize_filename(filename)
  # Split the name when finding a period which is preceded by some
  # character, and is followed by some character other than a period,
  # if there is no following period that is followed by something
  # other than a period (yeah, confusing, I know)
  fn = filename.split /(?<=.)\.(?=[^.])(?!.*\.[^.])/m

  # We now have one or two parts (depending on whether we could find
  # a suitable period). For each of these parts, replace any unwanted
  # sequence of characters with an underscore
  fn.map! { |s| s.gsub /[^a-z0-9\-]+/i, '_' }

  # Finally, join the parts with a period and return the result
  return fn.join '.'
end

def get_song(results, keywords)
  maxSimilarity = 0
  bestSong = nil
  for song in results
    titleAndArtist = song.title + " " + song.primary_artist.name
    currSim = titleAndArtist.similar(keywords)
    if currSim > maxSimilarity
      maxSimilarity = currSim
      bestSong = song
    end
  end
  return bestSong
end
             

workdir = ARGV[0]
keywords = $stdin.read
keywords = keywords.downcase.gsub(/[^a-z0-9\s]/i, '')

filepath = workdir + "/" +  keywords.gsub(' ', '-').gsub("/", "-")

filepath = filepath.gsub(/[\s]/i,'')
puts filepath

# if File.exist?(filepath)
#   exit
# end

Genius.access_token = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'
puts keywords
songs = Genius::Song.search(keywords) # Returns an array of Song objects
song = get_song(songs, keywords) # get the most likely Song from the results using simstring

if song.nil?
  puts "ERROR: no song found. Either too ambiguous or no results"
  exit
end
puts song.url

doc = Nokogiri::HTML(open(song.url))

file = File.open(filepath, 'w')
doc.xpath("//*[contains(@class, 'lyrics')]").each do |node|
   file.write( node.text )
end
