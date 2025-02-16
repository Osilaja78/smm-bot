from sqlalchemy.orm import Session
from fastapi import Depends
from api.database import get_db
from datetime import datetime, timedelta
from api import models
import requests
import time


def fetch_recent_videos(db: Session):
    try:
        user_token = db.query(models.AccessToken).first()
        access_token = user_token.access_token

        url = "https://open.tiktokapis.com/v2/video/list/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "fields": "id,title,video_description,duration",
            "max_count": 20
        }

        response = requests.post(url, headers=headers, params=params)
        # print(f"Response {response}")
        videos = response.json()
        video_ids = [video['id'] for video in videos['data']['videos']]
        print(video_ids)
        for id in video_ids:
            fetch_comments(access_token, id)
        return video_ids
        # return videos.get("data", [])
    except Exception as e:
        return e


def fetch_comments():
    # post_url = f"https://www.tiktok.com/@realpeller/video/7469107183553187077"
    # fetch_url = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime=1739433993&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={video_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20(Windows)&channel=tiktok_web&cookie_enabled=true&count=20&cursor=0&data_collection_enabled=false&device_id=7470812063988860471&device_platform=web_pc&focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&odinId=7470811911627310086&os=windows&priority_region=&referer=&region=NG&screen_height=864&screen_width=1536&tz_name=Africa/Lagos&user_is_login=false&webcast_language=en&msToken=SvbTYnDexjWQqGh5fr0wVUgjgQz1okDN6mn4hsyqSe2ytiN2iMayCZsjhMh4rQxFjNNArz1Wk5XN6H9aFl_sCYfx_o6W6RyLGNgIEX4whP9RTnGn8HFGghm7MmXUGBXYVuvCyw==&X-Bogus=DFSzsIVOCBkANe3ItkburqMHkvaH&_signature=_02B4Z6wo00001NDqxfQAAIDCaUVzfFmKM.jQ6MFAAFOcdf"
    fetch_url = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime=1739433993&aid=1988&app_language=en&app_name=tiktok_web&aweme_id=7469107183553187077&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20(Windows)&channel=tiktok_web&cookie_enabled=true&count=20&cursor=0&data_collection_enabled=false&device_id=7470812063988860471&device_platform=web_pc&focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&odinId=7470811911627310086&os=windows&priority_region=&referer=&region=NG&screen_height=864&screen_width=1536&tz_name=Africa/Lagos&user_is_login=false&webcast_language=en&msToken=SvbTYnDexjWQqGh5fr0wVUgjgQz1okDN6mn4hsyqSe2ytiN2iMayCZsjhMh4rQxFjNNArz1Wk5XN6H9aFl_sCYfx_o6W6RyLGNgIEX4whP9RTnGn8HFGghm7MmXUGBXYVuvCyw==&X-Bogus=DFSzsIVOCBkANe3ItkburqMHkvaH&_signature=_02B4Z6wo00001NDqxfQAAIDCaUVzfFmKM.jQ6MFAAFOcdf"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "www.tiktok.com",
        "Referer": "https://www.tiktok.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    }

    response = requests.get(fetch_url, headers=HEADERS)
    print(response.json())

# Reply to comments
def send_comment_reply(access_token, video_id, comment_id, reply_text):
    url = f"https://open.tiktokapis.com/v2/video/comment/reply/"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "video_id": video_id,
        "comment_id": comment_id,
        "text": reply_text
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("✅ Comment replied successfully")
    else:
        print("❌ Failed to reply to comment", response.json())


