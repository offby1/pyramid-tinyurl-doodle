# https://developers.google.com/search/docs/crawling-indexing/block-indexing
# https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag#xrobotstag
class NoIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Robots-Tag"] = "none"
        return response
