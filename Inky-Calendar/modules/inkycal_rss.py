#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
RSS module for Inky-Calendar software.
Copyright by aceisace
"""
from __future__ import print_function
import feedparser
from random import shuffle
from settings import *
from configuration import *

fontsize = 14

"""Add a border to increase readability"""
border_top = int(bottom_section_height * 0.05)
border_left = int(bottom_section_width * 0.02)

"""Choose font optimised for the weather section"""
font = ImageFont.truetype(NotoSans+'Light.ttf', fontsize)
space_between_lines = 1
line_height = font.getsize('hg')[1] + space_between_lines
line_width = bottom_section_width - (border_left*2)

"""Find out how many lines can fit at max in the bottom section"""
max_lines = (bottom_section_height - (border_top*2)) // (font.getsize('hg')[1]
  + space_between_lines)

"""Calculate the height padding so the lines look centralised"""
y_padding = int( (bottom_section_height % line_height) / 2 )

"""Create a list containing positions of each line"""
line_positions = [(border_left, bottom_section_offset +
  border_top + y_padding + _*line_height ) for _ in range(max_lines)]

def main():
  if bottom_section == "RSS" and rss_feeds != [] and internet_available() == True:
    try:
      print('RSS module: Connectivity check passed. Generating image...',
            end = '')

      """Parse the RSS-feed titles & summaries and save them to a list"""
      parsed_feeds = []
      for feeds in rss_feeds:
          text = feedparser.parse(feeds)
          for posts in text.entries:
              parsed_feeds.append('•{0}: {1}'.format(posts.title, posts.summary))

      """Shuffle the list, then crop it to the max number of lines"""
      shuffle(parsed_feeds)
      del parsed_feeds[max_lines:]


      """Check the lenght of each feed. Wrap the text if it doesn't fit on one line"""
      flatten = lambda z: [x for y in z for x in y]
      filtered_feeds, counter = [], 0

      for posts in parsed_feeds:
        wrapped = text_wrap(posts, font = font, line_width = line_width)
        counter += len(filtered_feeds) + len(wrapped)
        if counter < max_lines:
          filtered_feeds.append(wrapped)
      filtered_feeds = flatten(filtered_feeds)

      """Write the correctly formatted text on the display"""
      for _ in range(len(filtered_feeds)):
        write_text(line_width, line_height, filtered_feeds[_],
          line_positions[_], font = font, alignment= 'left')

      del filtered_feeds, parsed_feeds

      rss_image = image.crop((0,bottom_section_offset, display_width,
        display_height))
      rss_image.save(image_path+'rss.png')
      print('Done')

    except Exception as e:
      """If something went wrong, print a Error message on the Terminal"""
      print('Failed!')
      print('Error in RSS module!')
      print('Reason: ',e)
      pass

if __name__ == '__main__':
  main()
