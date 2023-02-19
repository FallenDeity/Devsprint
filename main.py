import asyncio
from src import Website

app = Website(docs="/docs", redoc="/redocs")
loop = asyncio.get_event_loop()
loop.create_task(app.on_startup())


if __name__ == "__main__":
    app.run()
