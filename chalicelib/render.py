import pystache


def render_db_rows(request, list_o_dicts):

    def short_url(db_row):
        return request.context.get('path', request.context.get('resourcePath', '')) + 'redirect/' + db_row['human_hash']

    with_short_urls = [dict(d, short_url=short_url(d)) for d in list_o_dicts]

    renderer = pystache.Renderer ()
    return renderer.render_path('chalicelib/home.stache',
                                {'rows': with_short_urls})
