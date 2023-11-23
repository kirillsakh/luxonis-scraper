from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_enum34 import EnumType

from database.types import EstateType


Base = declarative_base()


class Ad(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    address = Column(String)
    price = Column(String)
    image_url = Column(String)
    type = Column(EnumType(EstateType, name='estate_type'))

    # CheckConstraint to enforce the allowed values for 'type'
    __table_args__ = (
        CheckConstraint(type.in_(EstateType), name='check_valid_type'),
    )
