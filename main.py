from fastapi import FastAPI
from routers import router


app = FastAPI(title='Crypto Idolz rendering API')
app.include_router(router)