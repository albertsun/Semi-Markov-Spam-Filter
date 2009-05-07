#! /usr/bin/python
"""
Semi-Markov Spam Filter of Doom
    Filters spam, but not as well as other filters. Mostly intended as an experiment in the use of Markov chain-like objects for natural language analysis.
    Copyright (c) 2009 Matthew Croop
    Copyright (c) 2009 Albert Sun


    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License version 3 as
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    A copy the GNU General Public Licence version 3 is provide along
    with this program in the file name LICENCE. If not, see
    <http://www.gnu.org/licenses/>.
"""
import getopt
import email.parser
import email.message
from directory import *
from tokenizer import *
from Brain import *
from tools import *
import sys


"""Instructions for setting up .forward file.
add a line with |"/path/to/spamfilter.py -o outputfile"
"""

def loadbrain_from_file(filename):
     try:
         brainfile = open(filename)
     except IOError,e:
         print "Creating new brain \"" + filename + "\"..."
         brainfile = None
     if brainfile:
         try:
              return loadbrain(brainfile)
         except Exception,e:
              print e
              print "Error loading brain \"" + filename + "\""
     return Brain(1)

def savebrain_to_file(brain, filename):
    try:
         brain.save(open(filename, "w"))
    except Exception, e:
        print "Error saving brain \""+filename+"\""
        print e

class SpamFilter:
    def __init__(self, spambrain_filename, hambrain_filename):
        self.spambrain_filename, self.hambrain_filename = spambrain_filename, hambrain_filename
        self.spambrain = loadbrain_from_file(spambrain_filename)
        self.hambrain = loadbrain_from_file(hambrain_filename)
        self.spambrain_modified = False
        self.hambrain_modified = True
    
    def save(self):
        if self.spambrain_modified:
            savebrain_to_file(self.spambrain, self.spambrain_filename)
        if self.hambrain_modified:
            savebrain_to_file(self.hambrain, self.hambrain_filename)

FILTER_SPAM_LIST, MARK_SPAM, MARK_NOT_SPAM, FILTER_SPAM_SAVE = range(4)

def usageError(e = None):
    if e: print e
    progname = "spamfilter.py"
    if sys.argv[0]: progname = sys.argv[0]
    print "Usage: python "+progname+""" [-f FILE | -d DIRECTORY [-r] | -i INDEX -t TAG] [-l LIMIT] [-s | -n | -o OUTFILE]

-h print this help message

Read location:

-f read from file
-d read all files in directory
   -r (recursively)
-i read all files in index with given tag
   -t name of tag (e.g spam, ham)
** [default: read from standard input]

-l limit number of elements of directory/index to read

Action:

-s mark as spam
-n mark as not spam
-o used in .forward file, specify a location to save mail file with added header
** [default: determine if spam, print out results]
"""
    exit()

def filelist_from_argsdict(args_dict):
    fileoptions = []
    if '-f' in args_dict:
        assert not '-r' in args_dict
        assert not '-t' in args_dict
        fileoptions += [[args_dict['-f']]]
    if '-d' in args_dict:
        assert not '-t' in args_dict
        if '-r' in args_dict:
            fileoptions += [directoryIterRecurse(args_dict['-d'])]
        else:
            fileoptions += [directoryIter(args_dict['-d'])]
    if '-i' in args_dict:
        assert not '-r' in args_dict
        assert     '-t' in args_dict
        fileoptions += [fileIndexIter(args_dict['-i'], args_dict['-t'])]
    if not fileoptions:
        fileoptions += [[sys.stdin]]
    assert len(fileoptions) == 1
    return fileoptions[0]
        
def parse_argv(args_raw = sys.argv[1:]):
    """parses argv (not counting program name)
    returns an (Action, filelist, outputfile) tuple"""
    try:
        args, args_rest = getopt.getopt(sys.argv[1:],"f:d:ri:t:l:sno:h")
        args_dict = dict(args)
    except getopt.GetoptError, e: print usageError(e)
    if args_rest: usageError()
    if '-h' in args_dict: usageError()
    try:
        outputfile = ""
        filelist = filelist_from_argsdict(args_dict)
        if '-l' in args_dict:
            filelist = partialGen(filelist, int(args_dict['-l']))
        Actions = []
        if '-s' in args_dict:
            Actions += [MARK_SPAM]
        if '-n' in args_dict:
            Actions += [MARK_NOT_SPAM]
        if '-o' in args_dict:
            Actions += [FILTER_SPAM_SAVE]
            outputfile = args_dict['-o']
        if not Actions:
            Actions += [FILTER_SPAM_LIST]
        assert len(Actions) == 1

        return (Actions[0], filelist, outputfile)
        
    except IOError, e: usageError(e)
    except AssertionError: usageError()

def filter(Action, filelist, outputfile):
    """Score files in one of several ways depending on which Action is passed to it"""
    parser = email.parser.Parser()
    SF = SpamFilter("spam.brain","ham.brain")
    index = 0
    if Action in (MARK_SPAM, MARK_NOT_SPAM):
        if Action == MARK_SPAM:
            brain = SF.spambrain
            SF.spambrain_modified = True
        else:
            brain = SF.hambrain
            SF.hambrain_modified = True
        for i in OPENIter(filelist):
            messages = [start_message(parser.parse(i))]
            try:
                brain.add_sample(wordtokenizer(messages))
            except IOError: print 'x',
            index = index + 1
            if (index % 100) == 0:
                print '.',
                sys.stdout.flush()
            #print i.name
        SF.save()
    elif Action == FILTER_SPAM_LIST:
        msgs, spams, hams, unknowns = 0,0,0,0
        for i in OPENIter(filelist):
            l = list(wordtokenizer([start_message(parser.parse(i))]))
            spamscore = SF.spambrain.get_filescore(iter(l))
            hamscore = SF.hambrain.get_filescore(iter(l))
            msgs += 1
            if spamscore == hamscore:
                type = ' unknown'
                unknowns += 1
            elif spamscore > hamscore:
                type = '    spam'
                spams += 1
            else:
                type = 'not spam'
                hams += 1
            print i.name, type, hamscore,spamscore
        if msgs:
            print "Spam: ", spams*100.0/msgs, "    Not spam: ",hams*100.0/msgs, "    Unknown: ",unknowns*100.0/msgs
    elif Action == FILTER_SPAM_SAVE:
         for i in OPENIter(filelist):
              msg = parser.parse(i)
              l = list(wordtokenizer([start_message(msg)]))
              spamscore = SF.spambrain.get_filescore(iter(l))
              hamscore = SF.hambrain.get_filescore(iter(l))
              if spamscore == hamscore:
                   msg['MarkovBrainSpamStatus'] = "Unknown"
              elif spamscore > hamscore:
                   msg['MarkovBrainSpamStatus'] = "Spam"
              else:
                   msg['MarkovBrainSpamStatus'] = "Not Spam"
              #in normal use cases, this should get redirected to a file from stdout
              if outputfile:
                   saveout = sys.stdout
                   outfile = open(outputfile,'a')
                   sys.stdout = outfile
                   print str(msg)
                   sys.stdout = saveout
              else: print str(msg)
if __name__=="__main__":
    Action, filelist, outputfile = parse_argv()
    try:
         filter(Action, filelist, outputfile)
    except (KeyboardInterrupt): pass
    #except (Exception), e: print e
