from sqlalchemy import (
    Column,
    DateTime,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.sql.expression import func

from zope.sqlalchemy import ZopeTransactionExtension
import calendar
import pytz
import time

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class HashModel(Base):
    __tablename__ = 'hashes'

    create_date   = Column(DateTime(timezone=True), default=func.now())
    human_hash    = Column(Text, primary_key=True)
    long_url      = Column(Text)

    @property
    def time_t(self):
        dt = self.create_date

        # sqlite doesn't store time zones.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.utc)

        return calendar.timegm(dt.timetuple()) + dt.microsecond / 1E6

    @property
    def create_date_with_tz(self):
        return time.strftime('%FT%TZ', time.gmtime(self.time_t))
