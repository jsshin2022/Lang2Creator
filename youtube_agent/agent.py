
from flask import Flask, request, jsonify
import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Load static data
df = pd.read_csv("sample_data.csv")
df_views = pd.read_csv("daily_views.csv", parse_dates=["date"])

def get_latest_video(channel_id):
    res = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',
        maxResults=1
    ).execute()
    if not res['items']:
        return None
    item = res['items'][0]
    return {
        "title": item['snippet']['title'],
        "thumbnail": item['snippet']['thumbnails']['high']['url'],
        "video_id": item['id']['videoId']
    }

@app.route("/youtube", methods=["POST"])
def youtube_agent():
    data = request.json
    action = data.get("action")

    if action == "show_thumbnail":
        creator = data["creator_name"]
        row = df[df["channel_name"] == creator]
        if row.empty:
            return jsonify({"error": "Channel not found"})
        channel_id = row.iloc[0]["channel_id"]
        video = get_latest_video(channel_id)
        if not video:
            return jsonify({"error": "No video found"})
        return jsonify({
            "creator": creator,
            "title": video["title"],
            "thumbnail": video["thumbnail"],
            "url": f"https://youtube.com/watch?v={video['video_id']}"
        })

    elif action == "show_views":
        creator = data["creator_name"]
        start = pd.to_datetime(data["start_date"])
        end = pd.to_datetime(data["end_date"])
        subset = df_views[
            (df_views["channel_name"] == creator) &
            (df_views["date"] >= start) &
            (df_views["date"] <= end)
        ]
        if subset.empty:
            return jsonify({"creator": creator, "views": []})
        return jsonify({
            "creator": creator,
            "views": subset.to_dict(orient="records")
        })

    return jsonify({"error": "Unsupported action"})
