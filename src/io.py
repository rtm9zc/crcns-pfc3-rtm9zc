# -*- coding: utf-8 -*-
# -*- mode: python -*-
"""Functions for file IO"""
from __future__ import print_function, division, absolute_import
from scipy.io import loadmat

import csv

def file_to_trials(filename):
	'''Data is stored as several blocks of several trials in a nested structure of nparrays.
	Returns a list of the individual trial data'''
	matfile = loadmat(filename)
	outdata = []
	matdata = matfile['MatData'][0][0][0][0]
	for block in matdata:
		trials = block[0][0]
		for trial in trials:
			outdata.append(trial)
	return outdata

def files_from_csv(filename):
	'''Takes in a csv sheet from the SummaryDatabase 
	returns all filenames for relevant neurons listed in the csv'''
	files = []
	with open(filename, 'r', newline='') as f:
		reader = csv.reader(f)
		#ignore first row of labels
		next(reader)
		for row in reader:
		    files.append(str(row[0]) + '_' + str(row[1] + '.mat'))
	return files

