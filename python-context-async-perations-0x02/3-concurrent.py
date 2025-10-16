import asyncio
import aiosqlite

DB_NAME = "users.db"


async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\nAll Users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
