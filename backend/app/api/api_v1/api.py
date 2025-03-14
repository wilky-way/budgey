from fastapi import APIRouter

from app.api.api_v1.endpoints import budgets, accounts, transactions, categories, payees

api_router = APIRouter()

api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(payees.router, prefix="/payees", tags=["payees"])