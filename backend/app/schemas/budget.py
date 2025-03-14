from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class BudgetBase(BaseModel):
    """
    Base schema for budget data.
    """
    name: str
    last_modified_on: Optional[datetime] = None
    first_month: Optional[str] = None
    last_month: Optional[str] = None
    currency_format_iso_code: Optional[str] = None
    date_format: Optional[str] = None
    currency_format_symbol: Optional[str] = None

class Budget(BudgetBase):
    """
    Schema for budget data with ID.
    """
    id: str
    
    class Config:
        from_attributes = True

class BudgetResponse(BaseModel):
    """
    Schema for single budget response.
    """
    budget: Budget

class BudgetList(BaseModel):
    """
    Schema for list of budgets response.
    """
    budgets: List[Budget]