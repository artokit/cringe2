from fastapi import FastAPI
from account.controller import router as account_router
from transport.controller import router as transport_router
from payments.controller import router as payment_router
import logger


logger.load_config()

app = FastAPI()
app.include_router(account_router, prefix='/api/Account', tags=['Account Endpoints'])
app.include_router(transport_router, prefix='/api/Transport', tags=['Transport Endpoints'])
app.include_router(payment_router, prefix='/api/Payment', tags=['Payment Endpoints'])
# app.include_router(rent.controller.router, prefix='/api/Rent', tags=['Rent Endpoints'])
