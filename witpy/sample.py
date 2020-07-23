#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:54:56 2020

@author: Main
"""

import pymongo

from witpy_analyzer import Analyzer

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mongoClientDB = myclient['mywikidump']

analyzer = Analyzer(myclient, mongoClientDB)

filename = 'Indian_Institute_of_Technology_Ropar'

analyzer.downloadAndLoad(filename, filename)