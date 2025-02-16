"""
This module contains all logic for getting
user data.
"""

from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from api.database import get_db
from api import models
from dotenv import load_dotenv
from utils.tiktok_utils import send_comment_reply
from utils.transformers import gpt_reply
from uuid import uuid4
from utils.tiktok_utils import fetch_comments, fetch_recent_videos
import requests
import asyncio
import json
import os


router = APIRouter(tags=['Tiktok'])

load_dotenv()
TIKTOK_CLIENT_ID = os.getenv('TIKTOK_CLIENT_ID')
TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET')
REDIRECT_URI = "https://6f5f-197-211-63-108.ngrok-free.app/api/tiktok/callback"



# @router.post("/api/tiktok/webhook")
# async def tiktok_webhook(request: Request, db: Session = Depends(get_db)):
#     payload = await request.json()
#     print(payload)
    
#     # Ensure it's a comment event
#     if payload.get("event") == "video.comment.new":
#         comment_text = payload["data"]["text"]
#         video_id = payload["data"]["video_id"]
#         comment_id = payload["data"]["comment_id"]

#         # Fetch the latest access token from DB
#         token_entry = db.query(models.AccessToken).first()
#         if not token_entry:
#             return {"error": "No access token found"}

#         access_token = token_entry.access_token

#         # Auto-reply to the comment
#         reply_text = await gpt_reply(comment_text)
#         send_comment_reply(access_token, video_id, comment_id, reply_text)

#     return {"message": "Webhook received"}

@router.get("/get")
async def random_get_test(db: Session = Depends(get_db)):
    print("Inside random get test")
    try:
        print("Inside try")
        await fetch_recent_videos(db)
        # print("After gerring ids.")
        # print(f"IDs ==> {ids}")
        # # Fetch comments under each video
        # for id in ids:
        #     print(id)
        #     await fetch_comments(db, id)
    except Exception as e:
        return e

async def process_tiktok_event(payload):
    """
    Asynchronously process the TikTok webhook event to avoid blocking the response.
    """
    print(payload)
    try:
        event_type = payload.get("event", "")
        data = payload.get("data", {})

        if event_type == "video_comment.new":
            comment_text = data.get("text", "")
            video_id = data.get("video_id", "")
            user_id = data.get("user_id", "")
            print(f"New Comment: {comment_text} on Video: {video_id} by User: {user_id}")
            # ✅ Implement auto-reply logic here (e.g., reply_to_comment(video_id, comment_id, "Thanks!"))

        elif event_type == "video.like":
            print(f"Video {data.get('video_id')} got a like!")

        elif event_type == "video.mention":
            print(f"User {data.get('user_id')} was mentioned in a video!")

    except Exception as e:
        print(f"Error processing webhook event: {str(e)}")


# Webhook route to handle new comments
@router.post("/api/tiktok/webhook")
async def tiktok_webhook(request: Request):
    """
    TikTok Webhook Listener:
    - Immediately responds with 200 OK to acknowledge receipt.
    - Processes the webhook asynchronously to prevent timeouts.
    """

    try:
        # Parse incoming JSON request
        payload = await request.json()
        print(f"Received Webhook: {json.dumps(payload, indent=2)}")

        # ✅ Respond immediately to TikTok with 200 OK
        asyncio.create_task(process_tiktok_event(payload))
        return {"status": "success"}

    except Exception as e:
        print(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid webhook payload")


# Handle TikTok OAuth Callback
@router.get("/api/tiktok/callback")
async def tiktok_callback(request: Request, db: Session = Depends(get_db)):
    """
    Route to get user's tiktok access token
    """

    code = request.query_params.get("code")
    error_here = request.query_params.get("error")
    if error_here:
        print(error_here)
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Something went wrokg, please try again later!",
            )
    
    if not code:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Authorization code not received!",
            )

    # Delete the previous user token
    old_user_token = db.query(models.AccessToken).first()
    if old_user_token:
        db.delete(old_user_token)
        db.commit()
        db.close()

    # Exchange code for access token
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": TIKTOK_CLIENT_ID,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        user_access_token = token_data.get("access_token")
        user_refresh_token = token_data.get("refresh_token")
        if user_access_token and user_refresh_token:
            print(f"Access token => {user_access_token}, Refresh token => {user_refresh_token}")

            # ✅ Save tokens to database (for use in auto-reply bot)
            tokens = models.AccessToken(
                id=str(uuid4()),
                access_token=user_access_token,
                refresh_token=user_refresh_token
            )
            db.add(tokens)
            db.commit()
            db.refresh(tokens)
            db.close()
            return {"message": "TikTok connected!"}

    return {"error": "Failed to fetch access token"}

# @router.post("/api/tiktok/refresh_token")
def refresh_access_token(db: Session = Depends(get_db)):
    url = "https://open.tiktokapis.com/v2/oauth/token/"

    user_tokens = db.query(models.AccessToken).first()
    payload = {
        "client_key": TIKTOK_CLIENT_ID,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "refresh_token": user_tokens.refresh_token,
        "grant_type": "refresh_token"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        new_access_token = response.json().get("access_token")
        user_tokens.access_token = new_access_token
        db.commit()
        return {"access_token": new_access_token}
    
    return {"error": "Failed to refresh token"}

# Handle TikTok OAuth Callback
@router.get("/api/tiktok/check")
async def tiktok_check(db: Session = Depends(get_db)):
    """
    Route to check if user's access token exists
    """

    tokens = db.query(models.AccessToken).first()

    if tokens:
        if tokens.access_token and tokens.refresh_token:
            return {"status": 200, "message": "User is authenticated"}
    else:
        return {"status": 401, "message": "User is not authenticated"}