# I fucked up with redis fsm
# I'm too lazy to check out doc's, so I just copy someone sqlite fsm. Blame on me
from aiogram.filters.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey
from typing import Dict, Any, Optional
import aiosqlite
import json
import asyncio


class Storage(BaseStorage):
    async def update_data(self, key: StorageKey, data: Dict[str, Any], **kwargs):
        if data:
            _data = await self.get_data(key)
            _data.update(data)

            conn = await self._get_connection()
            await conn.execute("""
                INSERT OR REPLACE INTO fsm_data
                VALUES (?, (SELECT state FROM fsm_data WHERE key = ?), ?)
            """, (key.user_id, key.user_id, json.dumps(_data)))
            await conn.commit()
            await self.close()

    def __init__(self, path: str):
        self.path = path
        self._conn = None
        asyncio.run(self._init_db())

    async def _init_db(self):
        async with aiosqlite.connect(self.path) as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS fsm_data (
                    key TEXT PRIMARY KEY,
                    state TEXT,
                    data TEXT
                )
            """)
            await conn.commit()

    async def _get_connection(self):
        if self._conn is None:
            self._conn = await aiosqlite.connect(self.path)
        return self._conn

    async def close(self):
        if self._conn is not None:
            await self._conn.close()
            self._conn = None

    async def set_state(self, key: StorageKey, state: State = None) -> None:
        conn = await self._get_connection()

        if isinstance(state, State):
            state = state.state
        else:
            state = None

        await conn.execute("""
            INSERT OR REPLACE INTO fsm_data
            VALUES (?, ?, COALESCE((SELECT data FROM fsm_data WHERE key = ?), '{}'))
        """, (key.user_id, state, key.user_id))

        await conn.commit()
        await self.close()

    async def get_state(self, key: StorageKey) -> Optional[str]:
        conn = await self._get_connection()
        cursor = await conn.execute("SELECT state FROM fsm_data WHERE key = ?", (key.user_id,))
        result = await cursor.fetchone()
        await self.close()

        if result:
            state = result[0]
        else:
            state = None

        return state

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        conn = await self._get_connection()
        await conn.execute("""
            INSERT OR REPLACE INTO fsm_data 
            VALUES (?, COALESCE((SELECT state FROM fsm_data WHERE key = ?), null), ?)
        """, (key.user_id, key.user_id, json.dumps(data)))
        await conn.commit()
        await self.close()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        conn = await self._get_connection()
        cursor = await conn.execute("SELECT data FROM fsm_data WHERE key = ?", (key.user_id,))
        result = await cursor.fetchone()
        await self.close()
        return json.loads(result[0]) if result else {}

    async def clear(self, key: StorageKey | None = None):
        conn = await self._get_connection()
        await conn.execute("DELETE FROM fsm_data WHERE key = ?", (key.user_id,))
        await conn.commit()
        await self.close()
    