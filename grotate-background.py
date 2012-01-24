#!/usr/bin/python

#
# A simple hack to generate a transitioning background for a Gnome desktop and automagically update
# your user preferences with the result.  You stick the pics you want in a folder, point this at
# it, and away you go.
#
# You could use icron if you want it to auto-update.
#
# Copyright (c) 2009-2012 Rodger Donaldson.  Consider this under the 2-clause BSD license.
#

import dircache
from optparse import OptionParser
from os.path import expanduser
import gconf

#
# TODO: Check you're running under a valid GNOME environment and bail gracefully otherwise.
#

# Set the home directory, were we expend to find the ~/.gnome2 directory, and the defaults
# for finding a pictures directory.
user_dir =  expanduser('~')

#
# Get the user's specified directories,
#
parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory", default=user_dir + '/Pictures/Backgrounds/', help="The directory your pictures to rotate through live in.  This will default to HOME/Pictures/Backgrounds if you don't set a value.")

(options, args) =  parser.parse_args()

#
# TODO: Graceful error/exit if the directory doesn't exist or somesuch
#
files = dircache.listdir(options.directory)

#
# TODO: Bail gracefully on errors.
#
xml = open(user_dir + '/.gnome2/gbackground.xml', 'w')

# Boilerplate header.  We just need a date at some arbitary point in the past.
xml.write('<background><starttime><year>2009</year><month>08</month><day>04</day><hour>00</hour><minute>00</minute><second>00</second></starttime>\n')

for (count, file) in enumerate(files):
    xml.write('<static><duration>295</duration><file>' + options.directory + file +'</file></static>')
    xml.write('<transition><duration>5</duration><from>' + options.directory + file + '</from>')
    if count + 1 < len(files):
        # In the normal case we need to get the next file in the list for marking the transition
        xml.write('<to>' + options.directory + files[count + 1] + '</to></transition>\n')
else:
        # Otherwise we go back to the first element.
        xml.write('<to>' + options.directory + files[0] + '</to></transition>\n')
    
xml.write('</background>\n')

# TODO: Check for XML success
client = gconf.client_get_default()
client.set_string('/desktop/gnome/background/picture_filename', user_dir + '/.gnome2/gbackground.xml')
