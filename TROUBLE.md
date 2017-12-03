* deploying from my mac times out, but that can be worked around by deploying from my EC2 box.

* After pointing my browser at
  https://h0bvqn56e3.execute-api.us-west-1.amazonaws.com/api/ and
  clicking one of the short links, I get

     botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetItem operation: User: arn:aws:sts::661326993281:assumed-role/teensy-dev/teensy-dev is not authorized to perform: dynamodb:GetItem on resource: arn:aws:dynamodb:us-west-1:661326993281:table/hashes

I _thought_ I fixed this with

    30513280b4e644bf9fbc3fda702919a513e4082f
    Author:     Eric Hanchrow <eric.hanchrow@gmail.com>

    Woohoo -- I hadda fiddle a policy but this works.

but even after adding `"dynamodb:GetItem"` to the Allowed actions, it
still fails :-( So  I've removed the stuff that I added, and instead
attached the `AmazonDynamoDBReadOnlyAccess` built-in policy to the IAM
user, and that seems to get past it, and on to the next problem.
