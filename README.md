# bibparse -- read and write BibTeX files

## Description

`bibparse` reads and writes BibTeX files.

The main class, `Biblio`, is a `dict` with methods for parsing, reading, writing and searching for BibTeX data. Each entry in the `Biblio` is another kind of special dict, `BibItem`. The user usually only needs to access `Biblio`.

**NOTE** Just because I use only `{...}` myself, I’ve never thought of adding the more traditional `"..."` field marking before version 1.2.*.

## Current version

Version 1.3.0-dev.1 -- 5 July 2023.

## Copyrights

Copyright © 2019–2023 Legisign.org <mailto:software@legisign.org>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Example usage

    import bibparse
    db = bibparse.Biblio(filename)
    print(db)

The sample code loads, parses and pretty-prints a BibTeX file.

## Module contents

### 1. Helper functions

The values in some fields (namely author, editor, translator, publisher, address, and pages, all of which may have several names, locations, or other data in their values) of `BibItem` are stored internally as `list`s.

* `to_bibtex(key, val)` -- convert an internal Python value into a BibTeX string
* `to_python(key, val)` -- convert a BibTeX string into an internal Python value

Both functions take a BibTeX field name (key) in order to decide how to handle the value. Except for "pages" where the separator is a single dash "-", the separator is the string " and ", the leading and trailing whitespace included.

Examples:

*   `to_bibtex('pages', [100, 110])` →  '100-110'
*   `to_python('address', 'London and New York')` → ['London', 'New York']

### 2. Exceptions

* `BibError` -- the base exception
    * `DuplicateError` -- duplicate ID’s
    * `NoIDError` -- missing ID in an entry
    * `PreambleError` -- invalid preamble

Each exception has a property `lineno` in order to refer to the line that has raised the exception:

    try:
        db = bibparse.Biblio(filename)
    except bibparse.DuplicateError as exc:
        print(f'duplicate bibid on line {exc.lineno}')

### 3. BibItem class

A `dict`-derived object representing a single BibTeX entry.

#### 3.1 Methods

These are derived from `dict` but modified to ensure lower-case keys, reasonable ordering of keys in a printout, and sort ordering.

* `__lt__()`
* `__repr__()`
* `__setitem__()`
* `gets(key)` -- get key value as BibTeX-formatted string (or the empty string)
* `update()` -- update `Biblio` using another object
* static method `parse()`: parse data into a `BibItem`.

`gets()` is for convenience: it’s equivalent to `to_bibtex(BibItem.get())`.

`update()` has an additional optional `overwrite=bool` parameter. If `True` (the default), `update()` functions exactly like `dict.update()`, updating BibItem contents from data in the supplied `dict`. If `False`, only new keys in supplied data is added but existing values are not overwritten.

### 4. Biblio class

The main class. The constructor can be given an optional filename argument; the file is opened and parsed automatically.

#### 4.1  Methods

The `__repr__()` method is provided so that merely `print()`ing the `Biblio` object produces valid BibTeX output.

* `by_bibid(bibids)` -- return all entries whose bibid is in the list (or set)
* `by_regex(field, regex)` -- search in field by regex
* `by_type(bibtypes, complement=bool)` -- search by BibTeX type
* `get(key, default)` -- return a `BibItem` or the given default (by default, `None`)
* `parse(data)`  -- parse string as BibTeX data
* `read(filename)` -- read and parse file as BibTeX data

`by_bibid(bibids)` was written in order to make combining searches easier. Each `by_regex()` call returns a `Biblio` object whose keys can be obtained with `Biblio.keys()`. These keys can be used in `set` operations to provide a new list of keys that match either any (intersection) or all (union) of the keys, and `by_bibid()` can then be used to return all the entries.

`by_regex(field, regex)` searches the database by field values and returns the matches in a new `Biblio` object. E.g., `by_regex('author', '.*Smith.*')` returns all entries where the "author" field contains "Smith".

`by_types(bibtypes, complement=False)` searches the database by BibTeX types (given without the initial `"@"`) and returns the matches in a new `Biblio` object. `bibtypes` can be a string specifying a single type (e.g., `"article"`) or a list of strings specifying several types (e.g., `["article", "book"]`). If the optional `complement` parameter is set to True, the function returns the complement, i.e., all entries _not_ matching the criteria.

`parse()` can be manually called for `str` input; however, `read()` automatically calls it, as does the constructor `Biblio()` when given a filename argument.

**NOTE**: There used to be `write(filename)` method as well, and the code for it still exists but is commented out. Usually all that is needed is to `print()` the `Biblio`.
