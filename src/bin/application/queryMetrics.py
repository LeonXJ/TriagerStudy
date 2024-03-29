#!/usr/bin/python

# Author: LeonXie
# Date: 2013-5-14
# Parameters: 1) Product Assignment Record
#	      2) Login Product Assignment Record
#	      3) Peer Record
#	      4) Comment Record
#	      5) Actor
#	      6) Action Time
#	      7) New Product Name
# Output Stream: nPrdCorAssi nPrdAssi nLogPrdCorAssi nLogPrdCorAssi cntMaxExp cntN cmtN

import sys
import leon_lib as lib

# input
actor = sys.argv[5]
actionTime = int(sys.argv[6])
newProductName = sys.argv[7].lower()
# output
nPrdCorAssi = 0
nPrdAssi = 0
nLogPrdAssi = 0
nLogPrdCorAssi = 0
cntMaxExp = 0
cntN = 0
cmtN = 0

def GetTimeFromStr(string):
	return int((string.split(lib.fsep))[1])

def GetValueFromStr(string):
	return (string.split(lib.fsep))[0]

def GetValueByTimeFromStr(string, time):
	seq = string.split(lib.tsep)
	index = lib.binary_search(seq, GetTimeFromStr, time)
	if index < 0:
		return 0;
	return GetValueFromStr(seq[index])

def ReadProductAssignmentRecord(header, raw, curline):
	global nPrdAssi
	global nPrdCorAssi
	
	product = raw[header['product']]
	if product == newProductName:
		# nPrdAssi
		nPrdAssi = GetValueByTimeFromStr(raw[header['n_tri']], actionTime)
		# nPrdCorAssi
		nPrdCorAssi = GetValueByTimeFromStr(raw[header['n_cor_tri']], actionTime)

		return 1

def ReadLoginProductAssignmentRecord(header, raw, curline):
	global nLogPrdAssi
	global nLogPrdCorAssi
	
	login = raw[header['login']]
	product = raw[header['product']]
	if login == actor and newProductName == product:
		# nLogPrdAssi
		nLogPrdAssi = GetValueByTimeFromStr(raw[header['n_tri']], actionTime)
		# nLogPrdCorAssi
		nLogPrdCorAssi = GetValueByTimeFromStr(raw[header['n_cor_tri']], actionTime)

		return 1

def ReadLoginPeerRecord(header, raw, curline):
	global cntN
	global cntMaxExp
	
	login = raw[header['login']]
	if login == actor:
		# cntN
		cntN = GetValueByTimeFromStr(raw[header['contacter_num']], actionTime)
		# cntMaxExp
		cntMaxExp = GetValueByTimeFromStr(raw[header['max_contecter_exp']], actionTime)

		return 1

def ReadCommentRecord(header, raw, curline):
	global cmtN
	
	login = raw[header['login']]
	if login == actor:
		# cmtN
		cmtN = GetValueByTimeFromStr(raw[header['cmt_num']], actionTime)

		return 1

lib.read_file(sys.argv[1], lib.empty_header, ReadProductAssignmentRecord)

lib.read_file(sys.argv[2], lib.empty_header, ReadLoginProductAssignmentRecord)

lib.read_file(sys.argv[3], lib.empty_header, ReadLoginPeerRecord)

lib.read_file(sys.argv[4], lib.empty_header, ReadCommentRecord)

print str(nPrdCorAssi) + ',' + str(nPrdAssi) + ',' + str(nLogPrdCorAssi) + ',' + str(nLogPrdAssi) + ',' + str(cntMaxExp) + ',' + str(cntN) + ',' + str(cmtN)
