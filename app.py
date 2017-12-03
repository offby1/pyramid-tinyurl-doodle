from chalice import Chalice, Response

from chalicelib.db import get_some_entries_as_json
from chalicelib.render import render_db_rows

app = Chalice(app_name='teensy')
app.debug = True


@app.route('/')
def index():
    db_rows_as_dicts = get_some_entries_as_json ()
    return Response(body=render_db_rows(app.current_request, db_rows_as_dicts),
                    headers={'Content-Type': 'text/html'})

@app.route('/debug')
def debug():
    import pprint
    request_as_dict = app.current_request.to_dict()
    purty_request = pprint.pformat(request_as_dict)
    purty_app = pprint.pformat(vars(app))
    return Response(body=purty_app + '\n' + purty_request,
                    headers={'Content-Type': 'text/plain'})
