* deploying from my mac times out

* the above can be worked around by deploying from my EC2 box.  But now it's

     botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetItem operation: User: arn:aws:sts::661326993281:assumed-role/teensy-dev/teensy-dev is not authorized to perform: dynamodb:GetItem on resource: arn:aws:dynamodb:us-west-1:661326993281:table/hashes

I _thought_ I fixed this with

    30513280b4e644bf9fbc3fda702919a513e4082f
    Author:     Eric Hanchrow <eric.hanchrow@gmail.com>

    Woohoo -- I hadda fiddle a policy but this works.

but even after adding `"dynamodb:GetItem"` to the Allowed actions, it still fails :-(
