from fastapi import APIRouter
from .service import CalculateNetProfit


router = APIRouter()

@router.get("/profit")
async def calculate_mf_profit(scheme_code: str, start_date: str, end_date: str, capital: float = 1000000.0):
    net_profit = CalculateNetProfit().calculate_profit(scheme_code, start_date, end_date, capital)
    return net_profit

