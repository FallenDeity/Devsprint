import asyncio
from src import Website

app = Website(docs="/docs", redoc="/redocs")


if __name__ == "__main__":
    app.run()
