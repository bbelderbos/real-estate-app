from datetime import datetime

from sqlalchemy import VARCHAR, Boolean, Column, DateTime, Float, Integer

from data.modelbase import SqlAlchemyBase


class RentProperty(SqlAlchemyBase):
    __tablename__ = "rent_properties"
    id = Column(VARCHAR(255), primary_key=True, index=True)
    source_site = Column(VARCHAR(255), index=True)
    title = Column(VARCHAR(255), nullable=True)
    address = Column(VARCHAR(255), index=True)
    added_on = Column(DateTime, index=True, default=datetime.now)
    price = Column(Integer, index=True, nullable=False)
    rooms = Column(Integer, index=True, nullable=True)
    living_area = Column(Float, index=True, nullable=True)
    url = Column(VARCHAR(255), nullable=False)
    thumbnail_url = Column(VARCHAR(255), nullable=True)
    private_offer = Column(Boolean, nullable=True)
