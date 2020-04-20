#!/usr/bin/env python
# Created and tested on Python 2.7.13 by Ismael Goncalves https://sharingsec.net

import sys
import os
import time
from termcolor import colored
import threading
import logging

# Log Levels
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

# Controls whether the script will use experimental methods (Threads for parsing files/mounting dictionary)
# 0 = normal, 1 = experimental
exp = 0


def get_files(directory):
	# check for existence of the informed directory
	# exit if there is no such directory
	try:
		files = os.listdir(directory)
	except:
		print "Directory does not exist"
		quit()

	# listdir returns files and directory in specific folder
	# remove directory leaving only files
	# here it could be added a logic to verify whether a file is text or not

	logging.debug(files)

	files = [f for f in files if os.path.isfile(directory + '/' + f)]

	return files

def simple_normalization(wordsList):

	# transform all words into lower case
	words = [x.lower() for x in wordsList]

	# strip undesirable character (punctuation) from the words !!! Very Expensive?
	words = [s.strip('?|-|!|,|.|"|\'|;|:|_') for s in words]

	# remove repated elements - better way to do that?
	words = list(set(words))

	return words

# Experimental method to be used when using Threads
def dict_mount(dict,directory, f, pos):
	words = open(directory + '/' + f).read().split()
	words = simple_normalization(words)
	for k in words:
		if k in dict:
			dict[k].append(pos)
		else:
			dict.update({k:[pos]})
	return


def mount_reverse_index(fileList, directory):

	dict = {}
	threads = []
	for pos, f in enumerate(fileList):
		logging.debug('Processing file '+f)
		file = open(directory + '/' + f)
		words = file.read().split()
		words = simple_normalization(words)
		for k in words:
			if k in dict:
				dict[k].append(pos)
			else:
				dict.update({k:[pos]})
		del words[:]
		file.close()
	return dict

# experimental method to use Threads
def mount_reverse_index_experimental(fileList, directory):
	dict = {}
	threads = []
	for pos, f in enumerate(fileList):
		logging.debug('Processing file '+f)
		t = threading.Thread(target = dict_mount, args = (dict, directory, f, pos))
		threads.append(t)
		t.start()
		t.join()
	return dict

def display_files(reverseIndex, searchTerm, fileList):

	found_files  = { }

	for term in searchTerm:
		if term in reverseIndex:
			fileIndex = reverseIndex[term]
			for f in fileIndex:
				if  fileList[f] in found_files:
					found_files[fileList[f]].append(term)
				else:
					found_files.update({fileList[f]:[term]})

	if len(found_files) == 0:
		print colored("\r\nNo occurrences found :(\r\n", "red")
		return

	print colored("Words found on the following files (Top Ten):\r\n", "green")


	logging.debug(found_files)

	# calculate percentual of search terms found on each file and mount a dictionary 
	top_ten = {}

	# order by Score Reverse and Name Ascending
	for k, v in found_files.iteritems():
		vf = float( len(v))
		sf = float( len(searchTerm))
		percent =  ( vf / sf ) * 100.00
		top_ten.update({k:int(percent)})


	# convert Dictionary to Tuple and rerverse order
	top_ten = sorted(top_ten.items(), key=lambda x: (-x[1],x[0]))

	logging.debug(top_ten)

	# print only Top Ten
	for item in top_ten[:10]:
		print "%30s\t\t %3s%%" % (item[0], str(item[1]))

	print "\r"
	return

def main(argv):

	path_dir = ""

	# verify arguments
	if len(sys.argv) > 1:
		path_dir = sys.argv[1]
		# check for simple log level
		try:
			level = sys.argv[2]
			level = LEVELS.get(level, logging.INFO)
		except:
			level = logging.INFO
		logging.basicConfig(level=level, format="%(levelname)s:%(message)s")
	else:
		print "Search\r\n"
		print "Usage:\n\tSearch.py <directory-to-be-scanned> [debug]"
		print "\tLog level: info|debug"
		quit()

	# get file list
	print "Written by Ismael Goncalves\r\n"
	print "Obtaining file list...\r\n"
	files = get_files(path_dir)

	print colored("\r\nBuilding index...this might take from a few seconds to minutes...\r\n", 'red')

	# capture initial time prior to start building index
	timeinit = time.time()

	if exp == 1:
		# mount reverse index based on the files - EXPERIMENTAL using Threads
		index = mount_reverse_index_experimental(files,path_dir)
	else:
		# mount reverse index based on the files - default
		index = mount_reverse_index(files,path_dir)

	# show elapsed time when building index
	print "\nIndex built in %.2f seconds." % (time.time() - timeinit)
	print "Number of entries in the index: " + str(len(index)) + "\n"
	# This needs to be verified for proper information 
	print "Memory used to store index....: " + str(sys.getsizeof(index)) +" bytes\n"

	while True:
		search = raw_input("Type a string to search or :q to exit: ")
		if search == ":q":
			print "\nTchau! Cleaning and exiting..."
			index.clear()
			quit()
		else:
			print "\nSearching the word(s):"
			print colored(search + "\n", 'cyan')
			search = simple_normalization(search.split())
			timeinit = time.time()
			display_files(index, search, files)
			print "\nResults returned in %0.4f seconds" % ( time.time() - timeinit)


if __name__ == "__main__":
    main(sys.argv)
