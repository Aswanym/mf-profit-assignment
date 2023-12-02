from fastapi import FastAPI
from profit_calc_app.router import router as profit_calc_router

app = FastAPI()
app.include_router(profit_calc_router)
