from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.db.postgres import PostgresDB
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Initialize the database connection
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")

@app.on_event("startup")
async def startup():

    try:
        await db.connect()  # Establish a connection to the database
        await db.execute("SELECT 1")  # Test query to check connection
        logging.info("Database connection established successfully.")
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    logging.info("Database connection pool closed.")

@app.get("/test-db")
async def test_db():
    try:
        await db.execute("SELECT 1")  # Test query to check connection
        return {"status": "Database is reachable"}
    except Exception as e:
        return {"error": str(e)}

# Include the authentication router
app.include_router(auth_router, tags=["auth"])

# Run the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    # Run the app
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Set reload=True for local development
