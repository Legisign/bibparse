# bibparse -- read and write BibTeX files

## Description

`bibparse` reads and writes BibTeX files.

`BibParser()` is a special dict with added methods for parsing, reading, writing and searching for BibTeX data. Each entry in the `Bibliography` is another kind of special dict, `BibEntry`. Both define their own `__repr__()` methods so they can be directly printed in BibTeX format.

## Copyrights

Copyright © 2019 Legisign.org, Tommi Nieminen <software@legisign.org>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Module contents

### 1. Helper functions

* `to_bibtex(key, val)` -- convert an internal Python value into a BibTeX string
* `to_python(key, val)` -- convert a BibTeX string into an internal Python value

Both functions take a BibTeX `key` in order to decide, how to handle the value.

For example converting Python values to BibTeX strings:

* `key` = "pages", val = [100, 110] → "100-110"
* `key` = "address", val = ["London", "New York"] → "London and New York"

### 2. Exceptions

* `BibError` -- the base exception
    * `DuplicateError` -- duplicate ID’s
    * `NoIDError` -- missing ID in an entry
    * `PreambleError` -- invalid preamble

### 3. BibEntry class

A `dict`-derived object representing a single BibTeX entry.

#### 3.1 Methods

##### 3.1.1 Derived methods

These are derived from `dict` but modified to ensure lower-case keys, reasonable ordering of keys in a printout, and sort ordering.

* `__lt__()`
* `__repr__()`
* `__setitem__()`
* `update()`

##### 3.1.2 New method

* `parse(data)` -- parse string data into a BibTeX entry

### 4. Bibliography class

The main class. The constructor can be given an optional filename argument; the file is opened and parsed automatically.

#### 4.1  Methods

##### 4.1.1 Derived methods

* `__repr__()`

##### 4.1.2 New methods

* `by_regex(field, regex)` -- search in field by regex
* `by_types(bibtypes, complement=False)` -- search by BibTeX type
* `parse(data)`  -- parse string as BibTeX data
* `read(filename)` -- read and parse file as BibTeX data
* `write(filename)` -- write file in BibTeX format

`by_regex(field, regex)` searches the database by field values and returns the matches in a new `Bibliography` object. E.g., `by_regex('author', '.*Smith.*')` returns all entries where the "author" field contains "Smith".

`by_types(bibtypes, complement=False)` searches the database by BibTeX types (given without the initial `"@"`) and returns the matches in a new `Bibliography` object. `bibtypes` can be a string specifying a single type (e.g., `"article"`) or a list of strings specifying several types (e.g., `["article", "book"]`). If the optional `complement` parameter is set to True, the function returns the complement, i.e., all entries **not** matching the criteria.
