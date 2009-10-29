#!/usr/bin/env python
"""Parser for 454 Flowgram files"""

__author__ = "Jens Reeder, Julia Goodrich"
__copyright__ = "Copyright 2009, The Cogent Project"
__credits__ = ["Jens Reeder","Julia Goodrich"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jens Reeder"
__email__ = "jreeder@colorado.edu"
__status__ = "Development"

from string import strip
from random import sample
from itertools import izip

from cogent.parse.flowgram import Flowgram
from cogent.parse.record_finder import LabeledRecordFinder, is_fasta_label,\
     DelimitedRecordFinder, is_empty

__author__ = "Jens Reeder, Julia Goodrich"
__copyright__ = "Copyright 2009, The Cogent Project"
__credits__ = ["Jens Reeder","Julia Goodrich"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jens Reeder"
__email__ = "jreeder@colorado.edu"
__status__ = "Development"


def getHeaderInfo(lines):
    """Returns the Information stored in the common header as a dictionary

    lines can be a a list or a file handle
    """

    header_dict = {}

    for line in lines[1::]:
        if is_empty(line):
            break
       
        key, value = line.strip().split(':')
        header_dict[key] = value.strip()
        
    return header_dict

def getSummaries(handle, number_list = None, name_list=None, all_sums = False):
    """Returns specified flowgrams and sequence summaries as generator
    handle can be a list of lines or a file handle
    number_list is a list of the summaries wanted by their index in the sff
        file, starts at 0
    name_list is a list of the summaries wanted by their name in the sff file
    all_sums if true will yield all the summaries in the order they appear in
        the file

    One and only one of the parameters must be set
    """
    sff_info = LabeledRecordFinder(is_fasta_label,constructor=strip)
    sum_gen = sff_info(handle)

    if number_list:
        assert not (name_list or all_sums)
        num = len(number_list)
        for i,s in enumerate(sum_gen):
            if i-1 in number_list:
                yield s
                num -= 1
            if num == 0:
                break
            
    elif name_list:
        assert not all_sums
        for s in sum_gen:
            if s[0].strip('>') in name_list:
                yield s

    elif all_sums:
        header = True
        for s in sum_gen:
            if header:
                header = False
                continue
            yield s
    else:
        raise ValueError, "number_list, name_list or all_sums must be specified"


def getAllSummaries(lines):
    """Returns all the flowgrams and sequence summaries in list of lists"""
    sff_info = LabeledRecordFinder(is_fasta_label,constructor=strip)

    return list(sff_info(lines))[1::]

def splitSummary(summary):
    """Returns dictionary of one summary"""
    summary_dict = {}

    summary_dict["Name"] = summary[0].strip('>')
    for line in summary[1::]:
        key, value = line.strip().split(':')
        summary_dict[key] = value.strip()
        
    return summary_dict

def SFFParser(lines):
    """Creates list of flowgram objects from an SFF file
    """
    head = getHeaderInfo(lines)
    summaries = getAllSummaries(lines)

    flows = []
    for s in summaries:
        t = splitSummary(s)
        flowgram = t["Flowgram"]
        del t["Flowgram"]
        flows.append(Flowgram(flowgram, Name = t["Name"],
                              floworder =head["Flow Chars"], header_info = t))
    return flows, head


def LazySFFParser(handle):

    sff_info = LabeledRecordFinder(is_fasta_label,constructor=strip)
    sff_gen = sff_info(handle)

    header_lines = sff_gen.next()
    header = getHeaderInfo(header_lines)

    return (_sffParser(sff_gen, header), header)

def _sffParser(handle, header):
    for s in handle:
        t = splitSummary(s)
        flowgram = t["Flowgram"]
        del t["Flowgram"]
        flowgram = Flowgram(flowgram, Name = t["Name"], KeySeq=header["Key Sequence"],
                        floworder = header["Flow Chars"], header_info = t)
        
        yield flowgram

def getRandomFlowsFromSFF(filename, num=100, size=None):
    """Reads size many flows from filename and return a sample of num random ones.
    
    Note: size has to be the exact number of flowgrams in the file, otherwise 
    the result won't be random or less than num flowgrams wiil be returned

    filename: sff.txt input file

    num: number of flowgrams in returned sample

    size: number of flowgrams to sample from 
    """

    if(size==None):
        size = count_sff(open(filename))
    if (size<num):
        size = num
    
    (flowgrams, header) =  LazySFFParser(open(filename))
    idxs = sample(xrange(size), num)
    idxs.sort()
    i = 0   
    for (j,f) in izip(xrange(size), flowgrams):
        if (idxs[i] == j):
            i += 1
            yield f
            if (i>=num):
                break

def count_sff(sff_fh):
    """Counts flowgrams in a sff file"""
    
    (flowgrams, header) = LazySFFParser(sff_fh)
    i=0
    for f in flowgrams:
        i+=1
    return i


def SFFtoFasta(sff_fp, out_fp):
    """Transform an sff file to fasta"""
    (flowgrams, header) = LazySFFParser(open(sff_fp))

    out_fh = open(out_fp, "w")
                                     
    for f in flowgrams:
        out_fh.write(f.toFasta()+"\n")
