- Ensure that our db doesn't vanish if we upgrade docker!

  That happened once :-| I assume the thing to do is create a
  [data-only container](https://docs.docker.com/userguide/dockervolumes/).

- Keep track of how many times we've lengthened each short URL.  Also
  a timestamp for the last such time.
