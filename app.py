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

@app.route('/whatever/{something}')
def whatever(something):
    return f'Congratulations: {something}'


@app.route('/debug')
def debug():
    import pprint

    wat = {
        'app': vars(app),
        'request': app.current_request.to_dict(),
        'example_response': vars(Response(body='I am a body', headers={'Content-Type': 'text/shmext'}))
    }
    return Response(body=pprint.pformat(wat),
                    headers={'Content-Type': 'text/plain'})
