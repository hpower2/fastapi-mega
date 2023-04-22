from sqlalchemy import Column, String, BigInteger, Text, DateTime
from datetime import datetime
from db.connection import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    # is_actived = Column(String(1), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        
from sqlalchemy import Column, String, BigInteger, DateTime, Float, ForeignKey

class User_detail(Base):
    __tablename__ = 'user_detail'
    user_addres_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)
    nama = Column(String(50), nullable=False)
    no_telpon = Column(String, nullable=False)
    no_rekening = Column(String, nullable=False)
    no_pin = Column(String, nullable=False)
    saldo = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    
    def __init__(self, user_id, nama, no_telpon, no_rekening, no_pin, saldo):
        self.user_id = user_id
        self.nama = nama
        self.no_telpon = no_telpon
        self.no_rekening = no_rekening
        self.no_pin = no_pin
        self.saldo = saldo

    def serialize(self):
        return {
            'user_id': self.user_id,
            'nama': self.nama,
            'nomor_telepon' : self.no_telpon,
            'no_rekening' : self.no_rekening,
            'saldo': self.saldo
        }