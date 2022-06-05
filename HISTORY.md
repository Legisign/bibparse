# History and change log

## Prehistory

The project has had a long and convoluted history. My log goes as far as May 2012 when I seem to have rewrote the parsing routines from scratch. Even that was repeated in November of the same year. In June 2014 I decided to use a `dict` instead of a `list` as the main object class. The parsing routines were simplified in February 2016, and in June of that year I made major changes to them to increase their robustness.

In August 2016 I switched to using PyPI-compatible version numbering scheme in order to prepare for PyPI packaging, and made minor changes to the code in order to ensure Python 2 compatibility. The latter appears to have still caused issues since in July of the next year (2017) I had to do more changes towards it.

1 July 2019 was declared as the first “public” version (“1.0.0”), yet I continued to make bug fixes. During the next two weeks I made several semi-major changes to the code so the “1.0.0” moniker was clearly premature.

## 1.2.0 (2022-06-05)

Completely rewritten parsers and lots of other internal changes, **including** the possibility to use "..." for the BibTeX fields. Python 2 compatibility hacks discarded. f-strings utilized.

## 1.1.0 (2020-01-26)

`bibkeys` updated.

## 1.0.0 (2019-07-18)

Finally there.
