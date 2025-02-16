"""This module contains logic for accessing AI features"""

# from fastapi import APIRouter
# from api import schemas
from g4f.client import Client
from g4f.Provider import You


personality = "You are a professional social media manager for a marketing, reply this persons comment with a friendly and not so official tone. Make your comment short and straight to the point."

def gpt_reply(comment):

    messages = []

    prompt = f"{personality} \n\n {comment}"
    messages.append({"role": "assistant", "content": prompt})

    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            provider=You,
            messages=messages,
        )
        reply = response.choices[0].message.content

        return reply
    except Exception:
        return None