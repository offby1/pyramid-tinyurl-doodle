- Turn this into a paste site!  I'm sure I've thought about this, but
  can't find any notes.

- Keep track of how many times we've lengthened each short URL.  Also
  a timestamp for the last such time.

- Serve HTTPS with a cert from
  https://letsencrypt.readthedocs.org/en/latest/intro.html
  See `ssl-thoughts` in this directory.

- Nix PasteDeploy; use
  [Montague](https://metaclassical.com/announcing-montague-the-new-way-to-configure-python-applications/)
  instead!

- Some code review ideas from *** goodwill is ~goodwill@pdpc/supporter/active/goodwill (Good Will)
  <goodwill> . whitelist ip should be in config not global
  <goodwill> . test all the things
  <goodwill> . add docstrings with parameter and return docs to all the functions

- Consider [chalice](https://github.com/awslabs/chalice).  Of course then I'd have to change the name of this project, since it'd no longer be using pyramid.
