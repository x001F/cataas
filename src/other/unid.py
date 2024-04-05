import aiosqlite
from aiogram.types import Message


async def unid(message: Message) -> None:
    uid = message.from_user.id
    uname = message.from_user.username
    db: aiosqlite.Connection
    async with aiosqlite.connect('./src/config/fsm.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS usr (id INTEGER PRIMARY KEY, username TEXT)')
        await db.execute('REPLACE INTO usr VALUES (?, ?)', (uid, uname))
        await db.commit()
