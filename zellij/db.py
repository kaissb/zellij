# zellij/db.py
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    Boolean,
    LargeBinary,
    Numeric,
    Date,
    Time,
    Enum,
    ForeignKey,
    BigInteger,
    SmallInteger,
    Interval,
    PickleType,
    Unicode,
    UnicodeText,
    ARRAY,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .settings import config  # Adjust import according to your project structure

# Use settings from config
DATABASE_URL = config["database"]["url"]

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session():
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


# Abstraction layer for field types
class db:
    Integer = Integer
    String = String
    Text = Text
    DateTime = DateTime
    Float = Float
    Boolean = Boolean
    LargeBinary = LargeBinary
    Numeric = Numeric
    Date = Date
    Time = Time
    Enum = Enum
    ForeignKey = ForeignKey
    BigInteger = BigInteger
    SmallInteger = SmallInteger
    Interval = Interval
    PickleType = PickleType
    Unicode = Unicode
    UnicodeText = UnicodeText
    ARRAY = ARRAY
    JSON = JSON

    # MetaBase for adding functionalities like __tablename__ dynamically
    class MetaBase:
        @classmethod
        def __declare_last__(cls):
            cls.__tablename__ = cls.__name__.lower()
            # Here you can add more meta functionality like Django's Meta class

    # Model base class for users to inherit
    class Model(Base, MetaBase):
        __abstract__ = True
        id = Column(Integer, primary_key=True, index=True)

        # For enabling async operations
        @classmethod
        async def get(cls, _id):
            async with AsyncSessionLocal() as session:
                return await session.get(cls, _id)

        @classmethod
        async def create(cls, **kwargs):
            async with AsyncSessionLocal() as session:
                instance = cls(**kwargs)
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
