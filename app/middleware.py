# Honestly I don't understand this stuff, but I have two separate goals:

# 1) prevent the site from showing up in Google search results.  Those results benefit nobody.

# 2) prevent Google from crawling the site in the first place.  Crawls distract me because the requests appear in my logs, and I'd prefer to see only *real* requests (i.e., from humans creating or using the short URLs).

# Afaict, this middleware takes care of #1; serving "robots.txt" should handle #2.

# https://developers.google.com/search/docs/crawling-indexing/block-indexing
# https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag#xrobotstag


class NoIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Robots-Tag"] = "none"
        return response
