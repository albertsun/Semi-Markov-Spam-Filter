"""Semi-Markov Spam Filter of Doom
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
def partialGen(generator, n):
    count = 0
    for i in generator:
        if count >= n: return
        yield i
        count = count + 1

def flatten_message(message):
    if message.is_multipart():
        for i in message.get_payload():
            for j in flatten_message(i):
                yield j
    else:
        yield message.get_payload()

def start_message(message):
    if message.is_multipart():
        return start_message(message.get_payload()[0])
    else:
        return message.get_payload()
