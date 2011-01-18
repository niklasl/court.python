"""
URIFS URI to File System Mapper
========================================================================

URIFS defines a way to convert URI:s to and from file system paths.

The principle is to keep the resulting directory structure as "faithful" as
possible to hierarchical URI structures. This may seem a daunting task, and
URIFS only makes some basic assumption based on what is believed to be common
patterns.

URIFS does *not* claim to be entirely generic and versatile. The purpose is to
create fairly maintainable directory structures which are easy to read and
write.

For the entirely generic use case, other, more appropriate mechanisms exist;
especially the PairTree algorithm. (Such solutions are much more suitable for
massive, like gazillions, of collected URIs from all kinds of imaginable,
unordered sources..)

Algorithm
------------------------------------------------------------------------

The canonical algorithm is defined as primitive, chained regular expression
based mechanism, which allows it to be used in URL rewrite capable web servers,
such as Apache, Nginx, Lighttd, etc.

Examples
------------------------------------------------------------------------

Given the following test function:

    >>> def test(uri):
    ...     fspath = uri_to_fspath(uri)
    ...     print "Filepath:", fspath
    ...     newuri = fspath_to_uri(fspath)
    ...     assert newuri == uri, newuri
    ...     print "Filetree:"
    ...     print "".join(("/\\n" if i else "")+("  "*(i+1))+part
    ...         for i, part in enumerate(fspath.split('/')))

Here are some examples of how URI:s are turned into file system paths::

    >>> test("item@2011-02-12T16:32:00-0100/data?rev=1&l=100#main")
    Filepath: item@^/2011-^/02-12^/T16%3A32%3A^/00-0100/data%3F^/rev=1%26l=100%23^/main
    Filetree:
      item@^/
        2011-^/
          02-12^/
            T16%3A32%3A^/
              00-0100/
                data%3F^/
                  rev=1%26l=100%23^/
                    main

    >>> test("http://abc/def:ghi/jkl@mno")
    Filepath: http%3A%2F%2F^/abc/def%3A^/ghi/jkl@^/mno
    Filetree:
      http%3A%2F%2F^/
        abc/
          def%3A^/
            ghi/
              jkl@^/
                mno

    >>> test("http://example.org/publ/abc:xyz/r@2011-02-12T16:32:00.000Z/data?rev=1&l=100#main")
    Filepath: http%3A%2F%2F^/example.org/publ/abc%3A^/xyz/r@^/2011-^/02-12^/T16%3A32%3A^/00.000Z/data%3F^/rev=1%26l=100%23^/main
    Filetree:
      http%3A%2F%2F^/
        example.org/
          publ/
            abc%3A^/
              xyz/
                r@^/
                  2011-^/
                    02-12^/
                      T16%3A32%3A^/
                        00.000Z/
                          data%3F^/
                            rev=1%26l=100%23^/
                              main

    >>> test("0f7d48e4-2292-11e0-95ee-002332c94cb6")
    Filepath: 0f7d48e4-^/2292-^/11e0-^/95ee-^/002332c94cb6
    Filetree:
      0f7d48e4-^/
        2292-^/
          11e0-^/
            95ee-^/
              002332c94cb6

    >>> test("http://example.org/some%20escapes%20(%3F%)")
    Filepath: http%3A%2F%2F^/example.org/some%2520escapes%2520(%253F%25)
    Filetree:
      http%3A%2F%2F^/
        example.org/
          some%2520escapes%2520(%253F%25)

It also works for some bizarre cases, like multiple slashes::

    >>> #test("http://abc")
    >>> #test("http:///abc")
    >>> #test("http:////abc")
    >>> #test("http://///abc")
    >>> #test("http:///://abc")

"""
import re
import os.path
from functools import partial
from urllib import unquote


REWRITE_PATTERNS = [
    # escape escapes (so we can escape more stuff)
    (r'%', r'%25'),
    # escape chars (those we consider ok in URL:s but not in the fs)
    (r'\^', r'%5E'),
    (r'\$', r'%24'),
    (r'\|', r'%7C'),
    (r'\*', r'%2A'),
    ('&', '%26'),
    # split on uuid-like or year
    (r'([0-9a-f]{4,}-)', r'\1^/'),
    # split on month-day (after rewritten year)
    (r'\^/(\d\d-\d\d)', r'^/\1^/'),
    # split time (Thh:mm:, ss.millisTZ))
    (r'(T\d\d):(\d\d):(\d\d(?:\.\d{3})?(?:[+-]\d\d?\d\d|Z))',
            r'\1%3A\2%3A^/\3'),
    # splitting chars including multiple slashes
    (r'((?:/{2,}|[@:?!#])+)', r'\1^/'),
    # escaped splitting chars
    (r':', r'%3A'),
    (r'\!', r'%21'),
    (r'\?', r'%3F'),
    (r'#', r'%23'),
    # escaped multiple slashes (brittle..)
    (r'//', r'%2F%2F'),
    (r'/\^', r'%2F^'),
]


uri_transforms = [partial(re.compile(exp).sub, repl)
    for exp, repl in REWRITE_PATTERNS]


def uri_to_path(uri):
    return reduce(lambda path, transform:
            transform(path), uri_transforms, uri)

def uri_to_fspath(uri, pathsep=os.path.sep):
    return pathsep.join(uri_to_path(uri).split('/'))

def fspath_to_uri(path, pathsep=os.path.sep):
    return "/".join(map(unquote, path.split(pathsep))).replace('^/', '')


if __name__ == '__main__':

    from sys import argv
    args = argv[1:]
    if '-f' in args:
      args.remove('-f')
      print fspath_to_uri(args[0])
    else:
      print uri_to_fspath(args[0])


