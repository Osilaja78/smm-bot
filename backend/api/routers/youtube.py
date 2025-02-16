from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from api.database import get_db
from api import models
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os

router = APIRouter(tags=['Youtube'])

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


@router.get("/youtube/get")
async def get_youtube_service():
    token_path='token.json'
    credentials_path='credentials.json'
    
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_local_server(port=8080)
    
    with open(token_path, 'w') as token:
        token.write(credentials.to_json())
    
    return build('youtube', 'v3', credentials=credentials)


def get_youtube_service():
    # Replace the following with your actual credentials retrieval logic.
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.force-ssl"])
    return build("youtube", "v3", credentials=creds)


@router.get("/youtube/videos")
async def get_user_videos(service=Depends(get_youtube_service), max_results=50):
    request = service.channels().list(
        part="contentDetails",
        mine=True
    )
    response = request.execute()
    
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(response)
    
    videos = []
    next_page_token = None
    
    while True:
        playlist_items = service.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=max_results,
            pageToken=next_page_token
        ).execute()
        
        videos.extend(playlist_items['items'])
        next_page_token = playlist_items.get('nextPageToken')
        
        if not next_page_token:
            break
    
    return videos