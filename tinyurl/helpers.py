import datetime
import operator

def n_most_recent(most_recent_day, day_fetcher, num_items=10, days_back=10):
    """Returns the most recent entries in the hashes table, newest first."""

    most_recent_day = most_recent_day.date()

    for day_offset in range (0, -days_back, -1):
        day = most_recent_day + datetime.timedelta(days=day_offset)
        one_days_worth = day_fetcher(day)
        one_days_worth = sorted(one_days_worth,
                                key=operator.itemgetter('create_date'),
                                reverse=True)

        for item in one_days_worth:
            yield item
            num_items -= 1
            if num_items == 0:
                return
