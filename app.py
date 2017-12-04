from chalice import Chalice, Response

from chalicelib.db import a_few_recent_entries, lengthen_short_string
from chalicelib.render import render_db_rows

app = Chalice(app_name='teensy')
app.debug = True


@app.route('/')
def index():
    db_rows_as_dicts = a_few_recent_entries ()
    return Response(body=render_db_rows(app.current_request, db_rows_as_dicts),
                    headers={'Content-Type': 'text/html'})


@app.route('/redirect/{short_string}')
def redirect(short_string):
    long_url = lengthen_short_string(short_string)
    if long_url:
        return Response(body='Please hold while I get that number',
                        status_code=302,
                        headers={'Location': long_url})
    return Response(body="Ain't no thang",
                    status_code=404)


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
