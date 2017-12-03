import pystache


def render_db_rows(request, list_o_dicts):

    def short_url(db_row):
        host = request.headers['host']
        return '//' + host + '/redirect/' + db_row['human_hash']

    with_short_urls = [dict(d, short_url=short_url(d)) for d in list_o_dicts]

    renderer = pystache.Renderer ()
    return renderer.render_path('chalicelib/wat.stache',
                                {'rows': with_short_urls})
