from .celery_worker import celery
from .database import SessionLocal
from .models import Contact
from .smart_scraper import smart_scrape
import json

@celery.task
def scrape_and_process():
    cities = json.load(open("cities.json"))
    db = SessionLocal()
    for city in cities:
        results = smart_scrape(city["city"], city["state"])
        for r in results:
            db.add(Contact(**r))
    db.commit()
    db.close()