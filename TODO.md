- Keep track of how many times we've lengthened each short URL.  Also
  a timestamp for the last such time.

- Serve HTTPS with a cert from
  https://letsencrypt.readthedocs.org/en/latest/intro.html

- See if datatables has some provision for pagination -- that way I
  don't have to wait around while it scans the entire ddb table

- Nix PasteDeploy; use
  [Montague](https://metaclassical.com/announcing-montague-the-new-way-to-configure-python-applications/)
  instead!

- Some code review ideas from *** goodwill is ~goodwill@pdpc/supporter/active/goodwill (Good Will)
  <goodwill> . whitelist ip should be in config not global
  <goodwill> . test all the things
  <goodwill> . add docstrings with parameter and return docs to all the functions
