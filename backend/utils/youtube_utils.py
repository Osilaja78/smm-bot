


def get_user_videos(service, max_results=50):
    request = service.channels().list(
        part="contentDetails",
        mine=True
    )
    response = request.execute()
    
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
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


def get_video_comments(service, video_id, max_results=100):
    comments = []
    next_page_token = None
    
    while True:
        results = service.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            pageToken=next_page_token,
            textFormat="plainText"
        ).execute()
        
        for item in results['items']:
            comment = item['snippet']['topLevelComment']
            comments.append({
                'id': comment['id'],
                'text': comment['snippet']['textDisplay'],
                'author': comment['snippet']['authorDisplayName'],
                'published': comment['snippet']['publishedAt']
            })
        
        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break
    
    return comments


def post_reply(service, comment_id, text):
    response = service.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": comment_id,
                "textOriginal": text
            }
        }
    ).execute()
    return response

get_youtube_service()