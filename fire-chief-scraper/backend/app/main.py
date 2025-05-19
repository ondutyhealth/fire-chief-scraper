from fastapi import FastAPI
from app import models, tasks, database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API Running"}

@app.post("/start-job")
def start_scraping_job():
    tasks.scrape_and_process.delay()
    return {"status": "started"}

@app.get("/results")
def get_results():
    db = database.SessionLocal()
    results = db.query(models.Contact).all()
    return results