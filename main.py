from fastapi import FastAPI
<<<<<<< HEAD
from app.api.v1.auth import router as auth_router
=======
from app.api.v1.auth import router as auth_routerpip 
from app.api.v1.support import router as support_router
>>>>>>> minor fixes and requirements.txt
from app.db.postgres import PostgresDB
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

<<<<<<< HEAD
# Initialize the database connection
=======

>>>>>>> minor fixes and requirements.txt
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")

@app.on_event("startup")
async def startup(tags=["utility-api"]):

    try:
<<<<<<< HEAD
        await db.connect()  # Establish a connection to the database
        await db.execute("SELECT 1")  # Test query to check connection
=======
        await db.connect()  
        await db.execute("SELECT 1") 
>>>>>>> minor fixes and requirements.txt
        logging.info("Database connection established successfully.")
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    logging.info("Database connection pool closed.")

@app.get("/db-connection-check")
async def db_connection_check():
    try:
<<<<<<< HEAD
        await db.execute("SELECT 1")  # Test query to check connection
=======
        await db.execute("SELECT 1")
>>>>>>> minor fixes and requirements.txt
        return {"status": "Database is reachable"}
    except Exception as e:
        return {"error": str(e)}

# Include the authentication router
<<<<<<< HEAD
app.include_router(auth_router, tags=["auth"])
=======
app.include_router(auth_routerpip, tags=["auth"])
app.include_router(support_router, tags=["faq", "support"])
>>>>>>> minor fixes and requirements.txt

# Run the app with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    # Run the app
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Set reload=True for local development
