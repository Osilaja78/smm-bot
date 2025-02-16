import time, json, random, hashlib, requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configuration
USERNAME = "nexusdomains360@gmail.com"
PASSWORD = "Hameed123.tiktok.com"
VIDEO_URL = "https://www.tiktok.com/@nexusdomains360/video/7469170137950735671"  # Replace with actual video URL
REPLY_TEXT = "Automated reply from me"
video_id = "7469170137950735671"
comment_id = "7469170932062946103"

def generate_ms_token():
    """Dynamic msToken generation (simplified version)"""
    base = f"{int(time.time())}{random.randint(1000,9999)}"
    return base + hashlib.md5(base.encode()).hexdigest()[:50]

def generate_x_bogus(params: dict):
    """X-Bogus signature (requires full reverse-engineering)"""
    sorted_params = "&".join([f"{k}={v}" for k,v in sorted(params.items())])
    return hashlib.sha256(sorted_params.encode()).hexdigest()[:20].upper()

def generate_signature(driver):
    """_signature generation (pseudo-implementation)"""
    secret = driver.get_cookie("tt_chain_token")['value'] + driver.get_cookie("odin_tt")['value']
    return hashlib.md5(secret.encode()).hexdigest()

def convert_cookies(cookie_list):
    """Convert list of cookie dictionaries to requests-compatible dict"""
    return {c['name']: c['value'] for c in cookie_list}

# Initialize undetected chromedriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
# Optionally, use your real Chrome user profile to better mimic your actual browser:
# options.add_argument(r'--user-data-dir=C:\Path\To\Your\Chrome\User Data')

driver = uc.Chrome(version_main=132, options=options)

try:
    # Navigate to TikTok login page
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(5)  # Let page load

    # Locate username/email field (XPath may need adjustment)
    username_field = driver.find_element(By.XPATH, "//input[@type='text']")
    username_field.clear()
    username_field.send_keys(USERNAME)

    # Locate password field using type attribute
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.clear()
    password_field.send_keys(PASSWORD)

    # Submit the form
    password_field.send_keys(Keys.RETURN)
    print("Attempting login...")
    time.sleep(40)  # Wait for login process to complete

    # Confirm login success
    if "login" in driver.current_url.lower():
        print("Login appears to have failed. Exiting.")
        driver.quit()
        exit()

    print("✅ Login successful!")

    # Navigate to target video page
    driver.get(VIDEO_URL)
    time.sleep(5)  # Wait for page to load

    print("\n--- Extracted Session Cookies ---")
    cookies = driver.get_cookies()
    print(json.dumps(cookies, indent=2))

    msToken = driver.get_cookie('msToken')['value']

    # **************************************************************************************************************************** #
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "0",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://www.tiktok.com",
        "priority": "u=1, i",
        "referer": "https://www.tiktok.com/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    }

    params = {
        "WebIdLastTime": str(int(time.time())),
        "aid": "1988",
        "app_language": "en",
        "app_name": "tiktok_web",
        "aweme_id": video_id, # VIDEO ID HERE
        "browser_language": "en-US",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "Win32",
        "browser_version": "5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        "data_collection_enabled": "true",
        "device_id": str(random.randint(10**18, 10**19 - 1)),
        "device_platform": "web_mobile",
        "focus_state": "true",
        "from_page": "video",
        "history_len": "2",
        "is_fullscreen": "false",
        "is_page_visible": "true",
        "odinId": str(random.randint(10**18, 10**19 - 1)),
        "os": "android",
        "priority_region": "NG",
        "referer": "",
        "region": "NG",
        "reply_id": comment_id, # COMMENT ID HERE
        "reply_to_reply_id": "0",
        "screen_height": "719",
        "screen_width": "2730",
        "text": "Replyy, that's sick", # REPLY TEXT HERE
        "text_extra": "[]",
        "tz_name": "Africa/Lagos",
        "user_is_login": "true",
        "webcast_language": "en",
    }

    xbogus =  generate_x_bogus(params)
    signature = generate_signature(driver)
    params["X-Bogus"] = xbogus
    params["_signature"] = signature

    print(f"msToken: {msToken}")
    print(f"xbogus: {xbogus}")
    print(f"signature: {signature}")

    converted_cookies = convert_cookies(cookies)
    response = requests.post("https://www.tiktok.com/api/comment/publish/", headers=headers, params=params, cookies=converted_cookies)
    print(response)
    print(response.text)
    print(response.json())

finally:
    driver.quit()

