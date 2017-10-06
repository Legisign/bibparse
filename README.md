# bibparse

`bibparse` reads and writes BibTeX files.

**Author:** Tommi Nieminen <software@legisign.org> 2012–17.
**License:** GPL version 3 or later

`BibParser()` is a special dict with added methods for parsing, reading, writing and searching for BibTeX data. Each entry in the `Bibliography` is another kind of special dict, `BibEntry`. Both define their own `__repr__()` methods so they can be directly printed in BibTeX format.
