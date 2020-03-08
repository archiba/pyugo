from typing import ClassVar, Dict, Union

from sqlalchemy import Column, create_engine, String, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pyugo_db import crawler_logger
from pyugo_db.settings import PYUGO_DB_CRAWLING_DB_URI

logger = crawler_logger

logger.info('クローリング結果DBへ接続中')
engine = create_engine(PYUGO_DB_CRAWLING_DB_URI, echo=True)
Base = declarative_base()


def get_session():
    session = sessionmaker(bind=engine)()
    return session


class YGOCrawlingPack(Base):
    id: str = Column(String(length=32), primary_key=True)
    name: str = Column(String(length=64))
    url: str = Column(String(length=64))

    __tablename__: ClassVar[str] = 'packs'

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url


class YGOCrawlingCardInfo(Base):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(length=64))
    password: str = Column(String(length=8))
    card_no: str = Column(String(length=16))
    pack_id: str = Column(String(length=32), ForeignKey('packs.id'), nullable=False)

    __tablename__: ClassVar[str] = 'card_infos'

    def __init__(self, name, password, card_no, pack_id):
        self.name = name
        self.password = password
        self.card_no = card_no
        self.pack_id = pack_id


class YGOCrawlingCardText(Base):
    __tablename__: ClassVar[str] = 'card_text'

    id: int = Column(Integer, ForeignKey('card_infos.id'), primary_key=True)
    name: str = Column(String(length=64), nullable=False)
    kana: str = Column(String(length=128), nullable=False)
    card_type: str = Column(String(length=8), nullable=False)
    # モンスター情報
    card_attr: str = Column(String(length=16))
    type_: str = Column(String(length=16))
    has_effect: bool = Column(Boolean)
    is_pendulum: bool = Column(Boolean)
    is_fusion: bool = Column(Boolean)
    is_ritual: bool = Column(Boolean)
    is_synchro: bool = Column(Boolean)
    is_xyz: bool = Column(Boolean)
    is_link: bool = Column(Boolean)
    is_tuner: bool = Column(Boolean)
    is_toon: bool = Column(Boolean)
    is_union: bool = Column(Boolean)
    is_spirit: bool = Column(Boolean)
    is_gemini: bool = Column(Boolean)
    level: str = Column(String(length=2))
    rank: str = Column(String(length=2))
    link_arrows: str = Column(String(length=128))
    attack: str = Column(String(length=5))
    defense: str = Column(String(length=5))
    link: str = Column(String(length=2))
    # 魔法
    is_normal_spell: bool = Column(Boolean)
    is_continuous_spell: bool = Column(Boolean)
    is_field_spell: bool = Column(Boolean)
    is_quick_play_spell: bool = Column(Boolean)
    is_equip_spell: bool = Column(Boolean)
    is_ritual_spell: bool = Column(Boolean)
    # トラップ
    is_normal_trap: bool = Column(Boolean)
    is_continuous_trap: bool = Column(Boolean)
    is_counter_trap: bool = Column(Boolean)

    # パスワード
    password: str = Column(String(length=8))
    # ステータス
    status: str = Column(String(length=16))
    # テキスト
    card_text: str = Column(String(length=512))
    # ペンデュラムテキスト
    pendulum_text: str = Column(String(length=512))

    def __init__(self, card_info: YGOCrawlingCardInfo, text_values: Dict[str, Union[str, bool]]):
        self.id = card_info.id
        self.update(text_values)

    def update(self, text_values: Dict[str, Union[str, bool]]):
        for k, v in text_values.items():
            setattr(self, k, v)
