import datetime
import operator


def n_most_recent(
    most_recent_day, day_fetcher, num_items=10, days_back=10, later_than=None
):
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

    for day_offset in range(0, -days_back, -1):
        day = most_recent_day + datetime.timedelta(days=day_offset)
        if later_than and (later_than.date() > day):
            return
        one_days_worth = day_fetcher(day, later_than=later_than)
        one_days_worth = sorted(
            one_days_worth, key=operator.itemgetter('create_date'), reverse=True
        )

        for item in one_days_worth:
            yield item
            num_items -= 1
            if num_items == 0:
                return
