from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetResponse, BudgetList

router = APIRouter()

@router.get("/", response_model=BudgetList)
def get_budgets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve all budgets.
    """
    budgets = db.query(Budget).filter(Budget.deleted == False).offset(skip).limit(limit).all()
    return {"budgets": budgets}

@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific budget by ID.
    """
    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.deleted == False).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"budget": budget}