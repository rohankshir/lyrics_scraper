#!/usr/bin/ruby
# coding: utf-8
require 'rubygems'
require 'bundler/setup'
Bundler.require

require 'genius'
require 'nokogiri'
require 'open-uri'

workdir = ARGV[0]
keywords = $stdin.read

filepath = workdir + "/" +  keywords.gsub(' ', '-').gsub("/", "-")
print filepath

if File.exist?(filepath)
  exit
end

Genius.access_token = 'QfcNFORWYYHMb2l48a95UsfzXqNTjnbJZkn3TZZ6HTquOw58d7JQdERD8VnOa71y'

songs = Genius::Song.search(keywords) # Returns an array of Song objects
the_hills = songs.first

doc = Nokogiri::HTML(open(the_hills.url))

file = File.open(filepath, 'w')
doc.xpath("//*[contains(@class, 'lyric')]").each do |node|
   file.write( node.text )
end
