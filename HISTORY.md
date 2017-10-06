# History and change log

## bibparse.py

### Original version numbering

 * 2012-05-29  0.1     First working version is already more robust than the ones using regexps. Preambles do not work. (TN)
 * 2012-05-29  0.1.1   Preambles now work too. (TN)
 * 2012-05-29  0.2     Nicer __str__() but still bogey bibitems. (TN)
 * 2012-10-28  0.2.1   Trying to be compatible with bibsh and define “name” attribute for the Bibliography object. (TN)
 * 2012-11-06  0.2.2   Corrected bibsh instead and use “filename” here. (TN)
 * 2012-11-06  0.3     Total rewriting of Bibliography.parse(). (TN)
 * 2014-03-17  0.3.1   __repr__ instead of __str__ in both classes. Also stylistic changes. (TN)
 * 2014-04-08  0.3.4   Discarded previous 0.3.2…0.3.3 because of total deadlock and started tinkering afresh. (TN)
 * 2014-04-26  0.3.5   Added origtitle, transorigtitle, pubyear, keywords and location to the list of known BibTeX keys. Not using super() in the __init__() functions of classes because that’s not downwards compatible with Python 2. (TN)
 * 2014-06-07  0.4.0   Totally reworking of some parts: Bibliography is now a dict instead of list; this of course mean downwards incompatibility with some tools. Removed the silly “transorigtitle” key. (TN)
 * 2014-08-10  0.5.0   Added “write” method. Removed reliance on predefined bibtypes. Name finally changed to “bibparse” instead of “bibparse3”. (TN)
 * 2014-08-11  0.5.1   Changed BibItem to Bibentry, BibDB to Bibliography. (TN)
 * 2015-02-11  0.6.0   Small changes. (TN)
 * 2015-02-11  0.6.1   Changed global function _parse_data() to static method BibEntry.parse(). (TN)
 * 2015-02-12  0.6.2   Small changes. (TN)
 * 2015-02-12  0.7.0   find_all() for queries. (TN)
 * 2016-01-07  0.7.1   Small stilistic changes. (TN)
 * 2016-01-27  0.8.1   Changed revert -> complement in Bibliography.by_type().
 * 2016-01-30  0.8.2   Changed Bibliography.find_all() -> by_regex(), Bibliography.by_type() -> by_type(). Now using generator expressions in dicts.
 * 2016-02-09  0.9.0   Simplified the parsing procedure.
 * 2016-02-13  0.10.0  Doesn’t discard unknown keys.
 * 2016-05-27  0.10.1  Maybe we should raise different exceptions on different errors? First one to go, duplicate ID.
 * 2016-06-07  0.10.2  The rest of the exceptions implemented. (TN)
 * 2016-06-14  0.10.3  Renamed the exceptions to end in “Error”. (TN)
 * 2016-06-15  0.10.4  Renamed BibEntry.data to preamble since that’s what it is.
 * 2016-06-16  0.11.0  Major corrections to parse(): now it’s ugly as h*** but very robust. Overloaded __setitem__() and update() in BibEntry to ensure lowercase keys.
 * 2016-06-20  0.11.1  Added “unordered” parameter to Bibliography.write().

### PyPI-compatible version numbering

 * 2016-08-18  0.1.0.dev1    New version numbering as a prelude to creating a PyPI package. Main class renamed BibParser.
 * 2016-08-27  0.1.1.dev1    Small fixes to ensure Python 2 compatibility.
 * 2016-08-28  0.1.1.dev2    Fix of a fix (needed to understand super() in Python 2 first).
 * 2016-11-03  0.1.1.dev3    Fix of an assert: None is not a type!
 * 2017-01-04  0.1.1.dev4    dev1 renaming propagated to by_type(), by_regex().
 * 2017-03-24  0.9.9.beta1   No changes: first beta.
