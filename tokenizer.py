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
import re

def chartokenizer(linelist):
    """Separates an iterable of lines into one of characters"""
    for line in linelist: 
        for char in line:
            yield char

def wordtokenizer(linelist, striphtml=False):
    """Separates an iterable of lines into tokens: 
    two-and-a-half-hour is 9 tokens
    'muffin' is 3 tokens
    didn't is 1 token
    """
    regex = re.compile(r"""(
\w              # Word token starts with an alphanumeric a-zA-Z0-9_
(?:             # may also include: [non capturing group]
[\w']*\w        # indefinitely manu alphanumerics or apostrophes, ending with an alphanumeric
)?              # [end non capturing group]
|               # OR
\S              # Symbol token is one symbol (non-whitespace)
)""", re.VERBOSE)
    for line in linelist:
        if striphtml is True:
            line = strip_html(line)
        words = regex.findall(line)
        if words:
            for word in words:
                yield word

def strip_html(s):
    r = re.compile('<.*?>')
    return r.sub('',data)
