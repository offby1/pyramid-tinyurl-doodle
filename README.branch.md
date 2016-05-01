You know what I should do?  I should make this thing use DynamoDB as
the backing store, instead of sqlite or postgres or whatever I'm
using.

Why?

- Because then I can spin up a new one of these things anywhere, and
  it will get the same data as the old one

- Because it'd be good for me to play with DynamoDB

I've created a table:

    arn:aws:dynamodb:us-west-1:661326993281:table/hashes

The code all seems to work nicely (and I wrote some tests, too, so I'm
more confident than just "seems").

# TODO

- Make sure it can run as a docker image.  I suspect I don't want to
  put my aws credentials in the image, so ...

- Do the tests in a different table!