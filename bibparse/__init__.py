#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''bibparse -- a BibTeX parser.

  bibparse reads and writes BibTeX files.

  BibParser() is a special dict with added methods for parsing, reading,
  writing and searching for BibTeX data. Each entry in the Bibliography is
  another kind of special dict, BibEntry. Both define their own __repr__()
  methods so they can be directly printed in BibTeX format.

  Author:       Tommi Nieminen <software@legisign.org>
  License:      GPL version 3 or later

  2018-07-05  0.9.9.beta2   One more Python2 compatibility change to super().

'''

import re

version = '1.0.0'

# Recognized BibTeX keys; these keys will appear in the order given
# when BibEntry.__repr()__ is called. Any other keys in an entry will
# appear in random order tailing these ones.
bibkeys = ('key',
           'author',
           'title',
           'subtitle',
           'origtitle',
           'translator',
           'crossref',
           'editor',
           'booktitle',
           'booksubtitle',
           'origbooktitle',
           'chapter',
           'journal',
           'series',
           'volume',
           'number',
           'edition',
           'organization',
           'institution',
           'school',
           'publisher',
           'address',
           'pubstate',
           'howpublished',
           'url',
           'urldate',
           'doi',
           'month',
           'year',
           'pubyear',
           'pages',
           'isbn',
           'issn',
           'annote',
           'eprint',
           'type',
           'note',
           'keywords')

### HELPER FUNCTIONS

def to_bibtex(key, value):
    '''Convert Python list value to BibTeX string.'''
    if isinstance(value, list):
        if key.lower() == 'pages':
            value = '-'.join(value)
        elif key.lower() == 'keywords':
            value = ' '.join(value)
        else:
            value = ' and '.join(value)
    return value

def to_python(key, value):
    '''Convert BibTeX string to a Python value.'''
    if key.lower() in ('author', 'editor', 'publisher', 'translator'):
        value = value.split(' and ')
    elif key.lower() == 'pages':
        value = value.split('-')
    elif key.lower() == 'keywords':
        value = value.split()
    return value

### CLASSES

# Exceptions

class BibError(Exception):
    '''Base class of bibparse errors'''
    pass

class DuplicateError(BibError):
    '''Duplicate ID or preamble'''
    pass

class NoIDError(BibError):
    '''No ID in an entry'''
    pass

class PreambleError(BibError):
    '''Invalid preamble'''
    pass

# BibTeX classes

class BibEntry(dict):
    '''BibEntry is a dict containing one BibTeX entry.'''

    def __init__(self, bibid=None, bibtype=None, data=None):
        assert isinstance(data, (str, dict, type(None)))
        self.bibid = bibid
        self.bibtype = bibtype
        self.preamble = None
        if isinstance(data, dict):
            if bibtype == 'preamble':
                raise PreambleError(data)
            self.update(data)
        elif isinstance(data, str):
            if bibtype == 'preamble':
                self.preamble = data
            else:
                self.bibid, entry = BibEntry.parse(data)
                self.update(entry)

    def __lt__(self, entry):
        x = self.bibid if isinstance(self.bibid, str) else ''
        y = entry.bibid if isinstance(entry.bibid, str) else ''
        return x < y

    def __repr__(self):
        global bibkeys
        if self.bibtype == 'preamble':
            ret = '@preamble{{{}}}'.format(self.preamble)
        else:
            buff = ['@{}{{{}'.format(self.bibtype, self.bibid)] + \
                   ['    {} = {{{}}}'.format(key, to_bibtex(key, self[key])) \
                       for key in bibkeys if key in self] + \
                   ['    {} = {{{}}}'.format(key, val) \
                       for key, val in self.items() if key not in bibkeys]
            ret = ',\n'.join(buff) + '\n}'
        return ret

    def __setitem__(self, key, val):
        '''Overloaded __setitem__() to ensure lowercase keys.'''
        # super() needs arguments here for Python 2 compatibility
        super(BibEntry, self).__setitem__(key.lower(), val)

    def update(self, entries):
        '''Overloaded update() to ensure lowercase keys.'''
        # super() needs arguments here for Python 2 compatibility
        super(BibEntry, self).update({key.lower(): val \
                                     for key, val in entries.items()})

    @staticmethod
    def parse(data):
        '''Parse BibEntry data from a string.'''

        def discard_comments(s):
            '''Discard all trailing comments from data.'''
            buff = s.split('\n')
            for lineno, line in enumerate(buff):
                if '%' in line:
                    in_quotes = False
                    braces = 0
                    for col, c in enumerate(line):
                        if c == '"':
                            in_quotes = not in_quotes
                        elif c == '{':
                            braces += 1
                        elif c == '}':
                            braces -= 1
                        elif c == '%' and not in_quotes and not braces:
                            buff[lineno] = line[:col]
                            break
            return ' '.join(buff)

        data = discard_comments(data)
        bibid_pat = re.compile(r'^\s*([^,]+)\s*,\s*(.*)\s*$')
        try:
            bibid, keyvals = bibid_pat.match(data).groups()
        except AttributeError:
            raise NoIDError(data)
        bibid = bibid.strip()
        bibentry = {}
        next_is_key = True
        key = val = ''
        for c in keyvals:
            if next_is_key:
                if c.isalnum():
                    key += c
                elif c == '{':
                    next_is_key = False
                    val = c
            else:
                val += c
                if c == '}' and val.count('{') == val.count('}'):
                    bibentry[key] = to_python(key, val[1:-1])
                    next_is_key = True
                    key = val = ''
        return bibid, bibentry

class BibParser(dict):
    '''Bibliography is a dict of BibEntries.'''

    def __init__(self, filename=None, entries=None):
        self.filename = filename
        if self.filename:
            self.read(filename)
        if entries:
            if isinstance(entries, dict):
                self.update(entries)
            elif isinstance(entries, (list, set)):
                for entry in entries:
                    if not isinstance(entry, BibEntry):
                        raise ValueError(entry)
                    self[entry.bibid] = entry
            else:
                raise ValueError(entries)

    def __repr__(self):
        return '\n\n'.join([repr(entry) for entry in sorted(self.values())])

    def by_regex(self, field, pattern):
        '''Fetch all entries where field matches pattern (a regex).'''
        regex = re.compile(pattern)
        return BibParser(entries={k: v for k, v in self.items() \
                         if regex.search(str(v.get(field.lower(), '')))})

    def by_type(self, bibtypes, complement=False):
        '''Fetch all entries of given bibtype(s).'''
        if isinstance(bibtypes, str):
            bibtypes = {bibtypes}
        if not complement:
            f = lambda x, y: x in y
        else:
            f = lambda x, y: x not in y
        return BibParser(entries={k: v for k, v in self.items() \
                         if f(v.bibtype, bibtypes)})

    def parse(self, buff):
        '''Parse text buffer into a list of BibEntrys.'''
        # state can be one of the following:
        #   'wait' : wait for a bibentry (starts with “@”)
        #   'type' : read bibentry type (“book” etc.)
        #   'skip' : skip a trailing comment
        #   'data' : read bibentry data (between braces)
        state = 'wait'
        itemtype = itemdata = ''
        for c in buff:
            if state == 'skip':
                if c == '\n':
                    state = previous_state
            elif state == 'wait':
                if c == '@':
                    state = 'type'
                elif c == '{':
                    state = 'data'
                elif c == '%':
                    previous_state = state
                    state = 'skip'
            elif state == 'type':
                if c.isalpha():
                    itemtype += c.lower()
                elif c.isspace():
                    state = 'wait'
                elif c == '{':
                    state = 'data'
                elif c == '%':
                    previous_state = state
                    state = 'skip'
            elif state == 'data':
                if c == '}' and itemdata.count('{') == itemdata.count('}'):
                    if itemtype.lower() == 'preamble':
                        if '@preamble' in self:
                            raise DuplicateError
                        self['@preamble'] = BibEntry(bibtype='preamble',
                                                     data=itemdata)
                    else:
                        item = BibEntry(bibtype=itemtype, data=itemdata)
                        if item.bibid in self:
                            raise DuplicateError(item.bibid)
                        self[item.bibid] = item
                    state = 'wait'
                    itemtype = itemdata = ''
                else:
                    itemdata += c

    def read(self, filename):
        '''Read and parse a BibTeX file.'''
        self.filename = filename
        with open(filename, 'r') as f:
            buff = ' '.join([line for line in f])
        self.parse(buff)

    def write(self, filename=None, unordered=False):
        '''Write the bibliography to a BibTeX file.'''
        if not filename and not self.filename:
            raise ValueError(filename)
        if not filename:
            filename = self.filename
        with open(filename, 'w') as f:
            # Ensure decent ordering: first preamble, then not-collections,
            # then collections—because sometimes BibTeX can’t find crossrefs
            # unless they *follow* the reference
            if unordered:
                f.write(repr(self))
            else:
                f.write(repr(self.by_type('preamble')))
                f.write(repr(sorted(self.by_type(['preamble', 'collection'], \
                    complement=True))))
                f.write(repr(sorted(self.by_type('collection'))))

# Basic test if run as a script
if __name__ == '__main__':
    import sys

    def die(msg):
        # Can’t use print('…', file=…) here if called from Python 2
        sys.stderr.write(msg + '\n')
        sys.exit(1)

    for arg in sys.argv[1:]:
        try:
            db = BibParser(arg)
        except (FileNotFoundError, PermissionError, IOError):
            die('I/O-virhe: "{}"'.format(arg))
        except DuplicateError as exc:
            die('toistuva tunniste: "{}"'.format(exc.args[0]))
        except NoIDError as exc:
            die('puuttuva tunniste: "{}"'.format(exc.args[0]))
        except PreambleError:
            die('virheellinen @preamble')
        print(db)
