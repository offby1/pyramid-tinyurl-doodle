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
    hash = Column(BINARY(length=32), primary_key=True)  # hashlib.new('sha256').digest_size => 32L
    long_url = Column(Text)
