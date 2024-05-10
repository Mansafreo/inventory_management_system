from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    sales = relationship("Sale", back_populates="item")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    total_amount = Column(Float)

    items = relationship("Item", back_populates="sale")

    def __repr__(self):
        return f"<Sale(id={self.id}, date={self.date}, total_amount={self.total_amount})>"
