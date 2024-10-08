from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func

engine = create_engine(
    'postgresql://ad_agent:agent_password@127.0.0.1:5431/ad_site_pgdb'
)

Session = sessionmaker(engine)
Base = declarative_base(bind=engine)


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'ad_users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
        )
    username = Column(
        String,
        nullable=False,
        unique=True,
        index=True
        )
    password = Column(
        String,
        nullable=False
        )
    email = Column(
        String,
        nullable=False,
        index=True
        )
    creation_time = Column(
        DateTime,
        server_default=func.now()
        )


class Ad(Base):
    """Модель объявления"""
    __tablename__ = 'ads'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
        )
    header = Column(
        String,
        nullable=False,
        index=True
        )
    description = Column(
        String
        )
    creation_time = Column(
        DateTime,
        server_default=func.now()
        )
    user_id = Column(
        Integer,
        nullable=False
    )


Base.metadata.create_all()
