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
import os

def OPENIter(filelist):
    """Returns an open file for each path in the given list"""
    for filename in filelist:
        try:
            if type(filename) == str:
                theFile = open(filename)
                yield theFile
                theFile.close()
            elif type(filename) == file:
                yield filename
            else:
                print "Not a file or filename:", filename
        except IOError,e:
            print "[IOError]",e

def directoryIter(directory):
    """Returns a path for each item in the given directory (string)"""
    for filename in os.listdir(directory):
        yield os.path.join(directory, filename)

def directoryIterRecurse(directory):
    """Returns a path for each item in the given directory (string) and all its subdirectories"""
    for dirpath, dirnames, filenames in os.walk(directory):
        for i in filenames:
            yield os.path.join(dirpath, i)

def fileIndexIter(indexfilename, type):
    """Returns a path for each item in the given index (filename) whose first word is type"""
    try:
        indexFile = open(indexfilename)
        for i in indexFile:
            thistype, path = i.strip().split(" ")
            if thistype == type:
                yield os.path.normpath(os.path.join(indexfilename, "..", path))
        indexFile.close()
    except IOError,e:
        print "[IOError]",e
