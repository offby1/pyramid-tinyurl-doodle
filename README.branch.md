You know what I should do?  I should make this thing use DynamoDB as
the backing store, instead of sqlite or postgres or whatever I'm
using.

Why?

- Because then I can spin up a new one of these things anywhere, and
  it will get the same data as the old one

- Because it'd be good for me to play with DynamoDB
