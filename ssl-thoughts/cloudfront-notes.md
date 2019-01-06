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

Here's a GET request to `http://teensy.info`, hence without cloudfront:

    GET / HTTP/1.1.
    Host: teensy.info.
    Connection: keep-alive.
    Cache-Control: max-age=0.
    Upgrade-Insecure-Requests: 1.
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.353 8.110 Safari/537.36.
    DNT: 1.
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8.
    Accept-Encoding: gzip, deflate.
    Accept-Language: en-US,en;q=0.9.

Here's the equivalent to `https://www.teensy.info` (i.e., with cloudfront):

    GET / HTTP/1.1.
    Host: teensy.info.
    X-Amz-Cf-Id: OEimu7-b9IoyQ3zx-BlRQFVOljhTn2VVRfcPvCdnt-_WKxzXZjBHJQ==.
    Connection: Keep-Alive.
    User-Agent: Amazon CloudFront.
    Via: 2.0 0e018abb74f4918cb6e427c3e0a7ee33.cloudfront.net (CloudFront).
    X-Forwarded-For: 63.226.219.226.
    Accept-Encoding: gzip.
    upgrade-insecure-requests: 1.
    dnt: 1.

Unfortunately I don't see anything in the latter that clearly says "The dude typed `https` into his browser" :-|
