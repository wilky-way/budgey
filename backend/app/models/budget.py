from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.db.session import Base

class Budget(Base):
    """
    Budget model.
    """
    __tablename__ = "budgets"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_modified_on = Column(DateTime)
    first_month = Column(String)
    last_month = Column(String)
    currency_format_iso_code = Column(String)
    date_format = Column(String)
    currency_format_symbol = Column(String)
    deleted = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Budget {self.name}>"