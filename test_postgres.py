from fastapi import FastAPI, Depends
from app.db.postgres import PostgresDB
from app.db.postgres import PostgRESTClient
app = FastAPI()

# Initialize instances (for example purposes)
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")
client = PostgRESTClient("http://localhost:3000")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    await client.close()

@app.get("/users")
async def get_users():
    return await db.fetch("SELECT * FROM users")
