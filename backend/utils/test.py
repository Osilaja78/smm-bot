import requests, json, time

def fetch_comments():    
    cursor = 0
    video_id = "7469170137950735671"

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
    index = 1
    while True:
        fetch_url = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime=1739433993&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={video_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20(Windows)&channel=tiktok_web&cookie_enabled=true&count=50&cursor={cursor}&data_collection_enabled=false&device_id=7470812063988860471&device_platform=web_pc&focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&odinId=7470811911627310086&os=windows&priority_region=&referer=&region=NG&screen_height=864&screen_width=1536&tz_name=Africa/Lagos&user_is_login=false&webcast_language=en&msToken=SvbTYnDexjWQqGh5fr0wVUgjgQz1okDN6mn4hsyqSe2ytiN2iMayCZsjhMh4rQxFjNNArz1Wk5XN6H9aFl_sCYfx_o6W6RyLGNgIEX4whP9RTnGn8HFGghm7MmXUGBXYVuvCyw==&X-Bogus=DFSzsIVOCBkANe3ItkburqMHkvaH&_signature=_02B4Z6wo00001NDqxfQAAIDCaUVzfFmKM.jQ6MFAAFOcdf"
        response = requests.get(fetch_url, headers=HEADERS)
        print(response)
        data = response.json()
        print()
        
        comments = data['comments']
        for da in comments:
            if da['share_info']['desc'] != "":
                print(f"{index} : ID => {da['cid']}, Text ==> {da['share_info']['desc']}")
                index += 1
                # print(f"Replying comment {index}")
                # reply_comment(video_id, da['cid'], "Text from ai")
                # print("Reply sent")
        
        if data['has_more'] == 1:
            print("Has more....................................................................................")
            cursor += 20
            time.sleep(5)
        else:
            break


def reply_comment(video_id, comment_id, text):
    # Define the request URL
    # url = "https://www.tiktok.com/api/comment/publish/"
    url = f"https://www.tiktok.com/api/comment/publish/?WebIdLastTime=1723576196&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={video_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Linux%3B%20Android%206.0%3B%20Nexus%205%20Build%2FMRA58N%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F132.0.0.0%20Mobile%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&data_collection_enabled=true&device_id=7402703318315615750&device_platform=web_mobile&focus_state=true&from_page=video&history_len=9&is_fullscreen=false&is_page_visible=true&odinId=6795633426169332741&os=android&priority_region=NG&referer=https%3A%2F%2Fwww.tiktok.com%2F%40nexusdomains360&region=NG&reply_id={comment_id}&reply_to_reply_id=0&root_referer=https%3A%2F%2Fwww.tiktok.com%2F%40nexusdomains360&screen_height=1834&screen_width=2730&text={text}&text_extra=%5B%5D&tz_name=Africa%2FLagos&user_is_login=true&verifyFp=verify_m73be4n4_GQ3LaRYH_Qpb0_49xY_ASuC_5Kd1K2rNfUnj&webcast_language=en&msToken=WSP8bGkcKS1W3DC4FiQGKg3KlV3WeBpIUWhiWTzeYFV2GyUV1uHyC_5Jv-PabwU6WeNIBSyeTiyGBtv7oXHLFcPEky9MDpvJWF4QHrF432J16j359CiV8mSrLj1kbiwn4Uk9O_uj3rL0pwpi0BBB44bt&X-Bogus=DFSzswGLCC2ANC1DtkPK1ShPmkfg&_signature=_02B4Z6wo00001OIFn1QAAIDAkdjd96avR3DiJZvAAF811e"

    # Headers required for authentication
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "referer": "https://www.tiktok.com/@nexusdomains360/video/7469170137950735671",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "tt-csrf-token": "DwtbK8Hs-nJ9-dK_uTavQjYqCYa1rt0CHoHA",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
        "x-secsdk-csrf-token": "DOWNGRADE"
    }

    # Payload containing the reply details
    payload = {
        "WebIdLastTime": "1723576196",
        "aid": "1988",
        "app_language": "en",
        "app_name": "tiktok_web",
        "aweme_id": video_id,  # Video ID
        "browser_language": "en-US",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "Win32",
        "device_id": "7402703318315615750",
        "device_platform": "web_mobile",
        "focus_state": "true",
        "from_page": "video",
        "is_fullscreen": "false",
        "is_page_visible": "true",
        "odinId": "7469142193010476087",
        "os": "android",
        "region": "NG",
        "reply_id": comment_id,  # Comment ID you are replying to
        "reply_to_reply_id": "0",
        "text": text,  # Your reply text
        "text_extra": "[]",
        "tz_name": "Africa/Lagos",
        "user_is_login": "true",
        "verifyFp": "verify_m73be4n4_GQ3LaRYH_Qpb0_49xY_ASuC_5Kd1K2rNfUnj",
        "webcast_language": "en",
        "msToken": "a5tZVARJcQAjaAiIvIRs-SZ-J004Bv_zcYzF16cRV6MmUuLR6gRuh5LTA0qqK4ATdB-yMiW3514kgUjFECkX_9eA6fGitMK3kJYSlHckkzh1sbg8LSzIegbfXLulL3BQWcDJuJGyBvtfcf3CJlvKl_j51Ug=",
        "X-Bogus": "DFSzKwGLF5vANJTAtD3Ws8hPmkf6",
        "_signature": "_02B4Z6wo00001INvIOwAAIDA8LJiTvRq80CDTyRAAEdw94"
    }

    # Send the request
    response = requests.post(url, headers=headers, data=payload)

    # Print response
    print(response.status_code)
    print(response)

fetch_comments()