import asyncio
from app.database import engine
from app.services.analytics_service import generate_daily_reports

async def main():
    async with engine.begin() as conn:
        await generate_daily_reports(conn)

if __name__ == "__main__":
    asyncio.run(main())
