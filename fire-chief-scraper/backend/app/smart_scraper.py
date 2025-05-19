import openai
import time
from playwright.sync_api import sync_playwright
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def search_fire_dept_url(city: str, state: str) -> str:
    return f"https://www.{city.lower().replace(' ', '')}.gov/fire"

def extract_text_from_site(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        time.sleep(2)
        content = page.content()
        browser.close()
        return content

def ask_gpt_to_extract_contacts(html: str, city: str, state: str, url: str):
    prompt = f"""
Extract administrative fire personnel from the HTML below.
Return JSON array: name, title, email.

HTML:
{html}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1200
    )
    try:
        parsed = eval(response.choices[0].message.content)
        return [{
            "city": city, "state": state, "url": url,
            "name": p["name"], "title": p["title"], "email": p["email"]
        } for p in parsed if all(k in p for k in ("name", "title", "email"))]
    except:
        return []
    
def smart_scrape(city: str, state: str):
    try:
        url = search_fire_dept_url(city, state)
        html = extract_text_from_site(url)
        return ask_gpt_to_extract_contacts(html, city, state, url)
    except Exception as e:
        print(f"Scraping failed for {city}: {e}")
        return []