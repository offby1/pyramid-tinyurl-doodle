from chalice import Chalice, Response

from chalicelib.db import get_some_entries_as_json
from chalicelib.render import render_db_rows

app = Chalice(app_name='teensy')
app.debug = True


@app.route('/')
def index():
    db_rows_as_dicts = get_some_entries_as_json ()
    return Response(body=render_db_rows(db_rows_as_dicts),
                    headers={'Content-Type': 'text/html'})
