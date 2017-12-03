import mako.lookup


def render_db_rows(list_o_dicts):
    lookup = mako.lookup.TemplateLookup(["chalicelib"])

    template = lookup.get_template('wat.mak')
    return template.render(rows=list_o_dicts)
