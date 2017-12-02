from chalice import Chalice

from chalicelib.db import get_some_entries_as_json

app = Chalice(app_name='teensy')
app.debug = True


@app.route('/')
def index():
    return get_some_entries_as_json ()
