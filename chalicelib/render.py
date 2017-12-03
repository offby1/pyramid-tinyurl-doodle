import mako.lookup

def render_db_rows(request, list_o_dicts):

    def short_url(db_row):
        host = request.headers['host']
        return '//' + host + '/redirect/' + db_row['human_hash']

    lookup = mako.lookup.TemplateLookup(["chalicelib"])

    template = lookup.get_template('wat.mak')
    return template.render(compute_short_url=short_url,
                           rows=list_o_dicts)
