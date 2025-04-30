from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

LINE_ACCESS_TOKEN = os.getenv('LINE_API_TOKEN') # Vercel 環境変数 "LINE_API_TOKEN" (Enviromental Variables) にAPI トークンを設定
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

messages = {
    # "入力メッセージ":"返信メッセージ",

    "こんにちは":"こんにちは!",
    "はじめまして":"はじめまして！私はチャットボットです。",
    "テスト": "チャットボットのテスト",

}

@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"

def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": messages[text]}]
    }
    requests.post(LINE_API_URL, headers=headers, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                reply_message(event["replyToken"], event["message"]["text"])
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run()
