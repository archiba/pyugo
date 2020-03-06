from typing import ClassVar

from sqlalchemy import Column, create_engine, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from pyugo_db import crawler_logger

logger = crawler_logger

logger.info('クローリング結果DBへ接続中')
engine = create_engine('sqlite:///sample_db.sqlite3', echo=True)
Base = declarative_base()


class YGOCrawlingPack(Base):
    id: str = Column(String(length=32), primary_key=True)
    name: str = Column(String(length=64))
    url: str = Column(String(length=64))

    __tablename__: ClassVar[str] = 'packs'


class YGOCrawlingCardInfo(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=64))
    password: str = Column(String(length=8))
    pack_id: str = Column(String(length=32), ForeignKey('packs.id'), nullable=False)

    __tablename__: ClassVar[str] = 'card_infos'
