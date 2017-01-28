import datetime
import hashlib
import logging
import operator

_log = logging.getLogger(__name__)


def n_most_recent(most_recent_day, day_fetcher, num_items=10, days_back=10, later_than=None):
    """Returns the most recent entries in the hashes table, newest first.

    Makes multiple calls (no more than `days_back`) to day_fetcher, if
    needed; each call is expected to retrieve one day's worth of
    entries, ordered by creation time (newest first).

    :param most_recent_day: datetime object
    :param day_fetcher: function of a date object that returns a list of dicts
    :param num_items: number of dicts to return
    :param days_back: maximum number of days to fetch.
    :param later_than: only return items later than this datetime
    :yields: dicts from day_fetcher

    """

    most_recent_day = most_recent_day.date()

    for day_offset in range (0, -days_back, -1):
        day = most_recent_day + datetime.timedelta(days=day_offset)
        if later_than and (later_than.date() > day):
            return
        one_days_worth = day_fetcher(day, later_than=later_than)
        one_days_worth = sorted(one_days_worth,
                                key=operator.itemgetter('create_date'),
                                reverse=True)

        for item in one_days_worth:
            yield item
            num_items -= 1
            if num_items == 0:
                return


class EtagMemoizer():
    def __init__(self):
        self.current_digest = None
        self.cached_computation = None

    def _compute_etag_from_return_value(self, value):
        m = hashlib.md5(str (value).encode ('utf-8'))
        return m.hexdigest()

    def _maybe_compute(self, thunk, digest):
        """
        Maybe compute thunk, and return its value along with a new digest.
        Don't bother computing if the input digest matches the "current" digest.
        Intended to help the view code decide whether to return a 304.
        """
        was_slow = False

        _log.debug("_maybe_compute: digest is {!r}".format(digest))
        if self.current_digest is None or (self.current_digest != digest):
            _log.debug("Doesn't match {!r}; recomputing".format(self.current_digest))
            self.cached_computation = thunk()
            self.current_digest = self._compute_etag_from_return_value(self.cached_computation)
            _log.debug("current_digest is now {!r}".format(self.current_digest))
            was_slow = True

        return self.cached_computation, self.current_digest, was_slow

    def do_it_functionally(self, expensive_computation, digest, slow, fast):
        thunk_value, new_digest, was_slow = self._maybe_compute(expensive_computation, digest)

        if was_slow:
            return slow(thunk_value, new_digest), new_digest
        else:
            return fast(thunk_value, new_digest), new_digest
