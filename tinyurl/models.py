from sqlalchemy import (
    Column,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.types import BINARY

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class HashModel(Base):
    __tablename__ = 'hashes'
    human_hash = Column(Text, primary_key=True)
    long_url = Column(Text)
