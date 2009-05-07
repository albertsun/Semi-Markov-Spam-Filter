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

import marshal

def loadbrain(file):
    try:
        n =       marshal.load(file)
        brain =   marshal.load(file)
        i =       marshal.load(file)
        output = Brain(n)
        output.brain = brain
        output.i = i
        return output
    except (IOError, EOFError, ValueError, TypeError),e:
        print e
        return None

class Brain:
    """Holds an internal model of some passages of text which it has read in."""
    
    STOP = ""

    def __init__(self,n):
        """n-gram like word model."""
        self.n = n
        self.brain = {} #of prior counts
        self.i = 0 #total tokens
    
    def save(self, file):
        marshal.dump(self.n,        file)
        marshal.dump(self.brain,    file)
        marshal.dump(self.i,        file)


    def add_sample(self,tokenizer):
        """Adds words from the generator tokenizer to the brain."""
        STOP = "\n"
        buf = [STOP]*self.n
        while 1:
            try:
                word = tokenizer.next()
                del buf[0]
                buf.append(word)
                bufhash = hash(tuple(buf))
                self._trydict(bufhash)
                self.brain[bufhash] += 1
                self.i += 1
            except StopIteration:
                word = STOP
                del buf[0]
                buf.append(word)
                bufhash = hash(tuple(buf))
                self._trydict(bufhash)
                self.brain[bufhash] += 1
                self.i += 1
                break

    def _trydict(self,bufhash):
        if not bufhash in self.brain: self.brain[bufhash] = 0

    def get_filescore(self,tokenizer):
        """Returns a probability score of how likely text was to come from this brain."""
        STOP = "\n"
        count = 0
        buf = [STOP]*self.n
        while 1:
            try:
                word = tokenizer.next()
                buf.append(word)
                del buf[0]
                try: count += self.brain[hash(tuple(buf))]
                except KeyError: pass
            except StopIteration:
                break
        if self.i:
            return float(count)/self.i
        else:
            print "empty"
            return 0

