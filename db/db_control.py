import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
DATABASE_URL = os.getenv('DATABASE_URL')


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rate_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    exchange_rate = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def save_exchange_rate_history(user_id: int, base_currency: str, target_currency: str, exchange_rate: float):
    session = Session()
    history = ExchangeRateHistory(
        user_id=user_id,
        base_currency=base_currency,
        target_currency=target_currency,
        exchange_rate=exchange_rate
    )
    session.add(history)
    session.commit()
    session.close()


def get_exchange_rate_history(user_id: int):
    session = Session()
    history = session.query(ExchangeRateHistory).filter(ExchangeRateHistory.user_id == user_id).all()
    session.close()
    return history
