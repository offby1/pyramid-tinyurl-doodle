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

The only remaining thing is to figure out how to backfill -- i.e.,
take the data that's currently in Postgres "in production", and export
it to Dynamo ... so that when I switch over to the new version, all
the old URLs are still present.
