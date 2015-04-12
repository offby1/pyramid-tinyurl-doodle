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

from sqlalchemy.types import BINARY

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class HashModel(Base):
    __tablename__ = 'hashes'

    create_date   = Column(DateTime(timezone=True), default=func.now())
    human_hash    = Column(Text, primary_key=True)
    long_url      = Column(Text)
