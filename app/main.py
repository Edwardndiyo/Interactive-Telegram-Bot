import asyncio
from fastapi import FastAPI
from app.buyers_bot.bot import app as buyers_bot
from app.sellers_bot.bot import app as sellers_bot

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bot server is running!"}

async def start_bots():
    """Runs both the buyers and sellers bot asynchronously inside FastAPI's event loop."""
    await buyers_bot.initialize()  
    await sellers_bot.initialize()

    await buyers_bot.start()  
    await sellers_bot.start()

    await buyers_bot.updater.start_polling()
    await sellers_bot.updater.start_polling()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bots())  # Start bots without blocking FastAPI

@app.on_event("shutdown")
async def shutdown_event():
    """Stops both bots when the server shuts down."""
    await buyers_bot.stop()
    await sellers_bot.stop()




