I managed to put cloudfront in front of this, and thus can now serve
https.

It's got some problems, though:

- the caching seems to prevent me from seeing recent changes

- when the web app generates a URL to itself, it winds up using http,
  not https -- probably because it's examining the URL in the request
  _it_ got, which is indeed http://whatever (that's the URL that
  cloudfront generates).

  The result is that when I type something into the text box, and
  click the button to shorten it, I get redirected to the http://
  version of the site.

Not really a problem, but a surprise: at some point I tweaked it to
`79b657d Serve HTML rather than TEXT when there's no 'Accept' header`,
since otherwise I was seeing a blank page in my browser.  Well (I
should have thought of this) that broke rudybot: it was now getting
HTML instead of text.  Happily that was easily fixed: I just changed
rudybot to explicitly pass `Accept: text/json`.
