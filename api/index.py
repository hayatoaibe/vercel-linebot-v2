from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WEBSITE_URL = os.getenv('VERCEL_URL')
LINE_ACCESS_TOKEN = os.getenv('LINE_API_TOKEN') # Vercel 環境変数 "LINE_API_TOKEN" (Enviromental Variables) にAPI トークンを設定
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

messages = {
    # "入力メッセージ":["text","メッセージの種類","内容"],

    "こんにちは":["text","text","こんにちは!"],
    "はじめまして":["text","text", "はじめまして！私はチャットボットです。"],
    "テスト": ["text","text","チャットボットのテスト"],
    "website": ["text","text", WEBSITE_URL],

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
        "messages": [{"type": messages[text][0], messages[text][1]: messages[text][2]}]
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
