#!/usr/bin/python

import os, sys, re, argparse

parser = argparse.ArgumentParser()
parser.add_argument("matchnum", type=int, help="Number of matches to warrent logging")
parser.add_argument("filepath", help="location to start sweep for PII disclosures")
parser.add_argument("-o", "--output", help="output verbose report to file")
parser.add_argument("-s", "--silent", action='store_true', help="disable output to terminal")
args = parser.parse_args()

path = args.filepath
files =  os.listdir(path)
pattern = re.compile(r'\b((\d{3}[\. -]?\d{2}[\. -]?\d{4})|((\d{4}|[xX*#\-_]{4})[\. \-]?(\d{4}|[xX*#\-_]{4})[\. \-]?(\d{4}|[xX*#\-_]{4})[\. \-]?\d{4}))\b')
matches = args.matchnum
if args.output:
	report = open(args.output,'w')
	report.write("Starting at " + path +"\nLogging all files with " +str(matches)+ "or more flags\n")
if not args.silent:
	print("[+]Starting at " + path)

dircount = 0
filecount = 0
posscount = 0

for root, dirs, files in os.walk(path):
	dircount = dircount + len(dirs)
	for entry in files:
		filecount += 1
		try:
			fp = open(os.path.join(root,entry))
		except:
			pass
		else:
			try:
				text = fp.read()
			except:
				pass
			else:
				results = pattern.findall(text)
				if len(results) >= matches:
					posscount += 1
					if args.output:
						report.write("Match	"+str(len(results))+"	" + os.path.join(root,entry) + "\n")
					if not args.silent:
						print("  Possible: " + os.path.join(root,entry))
if args.output:
	report.write("Finished, found " + str(posscount) + " possible disclosures. Visited " + str(dircount) + " directories and " + str(filecount) + " files.")
if not args.silent:
	print("[+]Finished, found %d possible disclosures. Visited %d directories and %d files." % (posscount, dircount, filecount))

