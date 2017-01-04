from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    hashed_password = Column(Text)
    email = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    favorite_food = Column(Text)
