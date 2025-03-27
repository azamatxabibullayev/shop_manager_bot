from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///bot_data.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    icon = Column(String(100), nullable=True)  # could be emoji/icon code
    registration_cert = Column(String(255), nullable=True)  # file path of PDF certificate
    payment_contract = Column(String(255), nullable=True)  # file path PDF
    cadastral_doc = Column(String(255), nullable=True)  # file path PDF
    lease_contract = Column(String(255), nullable=True)  # file path PDF
    photo = Column(String(255), nullable=True)  # file path for photo
    area = Column(Float, nullable=False, default=0.0)  # in sq.m.


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, nullable=False)
    month = Column(String(20), nullable=False)  # e.g. "2025-01"
    shop_area = Column(Float, nullable=False)
    base_payment = Column(Float, nullable=False)  # calculated payment before VAT
    vat_amount = Column(Float, nullable=False)
    total_payment = Column(Float, nullable=False)
    left_over = Column(Float, nullable=False, default=0.0)
    paid = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ElectricityReading(Base):
    __tablename__ = "electricity_readings"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, nullable=False)
    reading_date = Column(DateTime, default=datetime.datetime.utcnow)
    previous = Column(Integer, nullable=False, default=0)
    current = Column(Integer, nullable=False, default=0)
    usage = Column(Integer, nullable=False, default=0)
    tariff = Column(Integer, nullable=False, default=1100)  # default tariff per unit
    calculated_amount = Column(Integer, nullable=False, default=0)
    paid_amount = Column(Integer, nullable=False, default=0)
    debt = Column(Integer, nullable=False, default=0)
    overpaid = Column(Integer, nullable=False, default=0)


# For Monitoring, you may create separate models or compute reports on the fly.
# In this example, monitoring reports will be generated from Payment and Electricity data.

def init_db():
    Base.metadata.create_all(bind=engine)
