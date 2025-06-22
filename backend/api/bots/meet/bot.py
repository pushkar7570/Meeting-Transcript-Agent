import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

GOOGLE_EMAIL = "libza.bot@gmail.com"
GOOGLE_PASSWORD = "Chauhans@123"
MEET_LINK = "https://meet.google.com/yet-qchz-dut"
BACKEND_API_URL = "http://localhost:5001/api/v1/meet/transcript"

def login_and_join_meet(email, password, meet_link):
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless")  # Optional: Uncomment for headless mode

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://accounts.google.com/ServiceLogin")

    # Login flow
    driver.find_element(By.ID, "identifierId").send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(3)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)
    
    driver.get(meet_link)
    time.sleep(10)  # Adjust if you have a slow network

    # Turn off mic and camera for bot
    try:
        mic_btn = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Turn off microphone']")
        cam_btn = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Turn off camera']")
        mic_btn.click()
        cam_btn.click()
    except Exception:
        pass

    # Enable captions
    try:
        captions_btn = driver.find_element(By.XPATH, "//button[@aria-label='Turn on captions (c)']")
        captions_btn.click()
        print("Captions enabled!")
    except Exception:
        print("Captions button not found!")
    return driver

def get_captions(driver, backend_api_url):
    captions_selector = "div[jsname='Y3TXzd']"
    already_seen = set()
    print("Scraping captions... Press Ctrl+C to stop.")
    while True:
        try:
            captions = driver.find_elements(By.CSS_SELECTOR, captions_selector)
            for caption in captions:
                text = caption.text.strip()
                if text and text not in already_seen:
                    already_seen.add(text)
                    timestamp = datetime.now().isoformat()
                    print(f"[{timestamp}] {text}")
                    # Send to backend
                    try:
                        requests.post(backend_api_url, json={"text": text, "timestamp": timestamp})
                    except Exception as e:
                        print(f"Failed to send to backend: {e}")
            time.sleep(2)
        except KeyboardInterrupt:
            print("Stopping caption scraping.")
            break
    return

if __name__ == "__main__":
    driver = login_and_join_meet(GOOGLE_EMAIL, GOOGLE_PASSWORD, MEET_LINK)
    get_captions(driver, BACKEND_API_URL)
