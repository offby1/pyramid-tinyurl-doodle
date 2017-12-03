* deploying from my mac times out

* the above can be worked around by deploying from my EC2 box.  But
  then after pointing my browser at
  https://h0bvqn56e3.execute-api.us-west-1.amazonaws.com/api/, I get

      Traceback (most recent call last):
        File "/var/task/chalice/app.py", line 649, in _get_view_function_response
          response = view_function(**function_args)
        File "/var/task/app.py", line 13, in index
          return Response(body=render_db_rows(app.current_request, db_rows_as_dicts),
        File "/var/task/chalicelib/render.py", line 12, in render_db_rows
          renderer = pystache.Renderer ()
      AttributeError: module 'pystache' has no attribute 'Renderer'
