import asyncpg
import aiohttp
from fastapi import HTTPException
from typing import Any, Dict, Optional

class PostgRESTClient:
    def __init__(self, base_url: str, session: Optional[aiohttp.ClientSession] = None):
        self.base_url = base_url
        self.session = session or aiohttp.ClientSession()

    async def fetch(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        url = self.base_url + endpoint
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 404:
                return None
            else:
                raise HTTPException(status_code=response.status, detail="Error fetching data")

    async def post(self, endpoint: str, json: Dict[str, Any]) -> Dict[str, Any]:
        url = self.base_url + endpoint
        async with self.session.post(url, json=json) as response:
            if response.status == 201:
                return await response.json()
            else:
                raise HTTPException(status_code=response.status, detail="Error creating resource")

    async def put(self, endpoint: str, json: Dict[str, Any]) -> Dict[str, Any]:
        url = self.base_url + endpoint
        async with self.session.put(url, json=json) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise HTTPException(status_code=response.status, detail="Error updating resource")

    async def delete(self, endpoint: str) -> None:
        url = self.base_url + endpoint
        async with self.session.delete(url) as response:
            if response.status != 204:
                raise HTTPException(status_code=response.status, detail="Error deleting resource")

    async def close(self):
        await self.session.close()


class PostgresDB:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        """Establish a connection pool to the database."""
        if self.pool is None:  # Only create a pool if it doesn't exist
            self.pool = await asyncpg.create_pool(self.database_url)

    async def fetch(self, query: str, *args) -> Optional[asyncpg.Record]:
        await self.connect()  # Ensure the connection pool is established
        if self.pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetch_one(self, query: str, *args) -> Optional[asyncpg.Record]:
        await self.connect()  # Ensure the connection pool is established
        if self.pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def execute(self, query: str, *args) -> str:
        """Execute a SQL query and return the status message.

        Args:
            query (str): The SQL query to execute.
            *args: Any arguments to pass to the query.

        Returns:
            str: The status message returned from the query.
        """
        await self.connect()  # Ensure the connection pool is established
        
        if self.pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        print(f"Executing query: {query}")
        print(f"Arguments: {args}")
        
        try:
            async with self.pool.acquire() as connection:
                return await connection.execute(query, *args)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise

    async def disconnect(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            self.pool = None  # Clear the pool after closing


