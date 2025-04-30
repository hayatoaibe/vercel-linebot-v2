from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WEBSITE_URL = os.getenv('VERCEL_PROJECT_PRODUCTION_URL')
LINE_ACCESS_TOKEN = os.getenv('LINE_API_TOKEN') # Vercel 環境変数 "LINE_API_TOKEN" (Enviromental Variables) にAPI トークンを設定
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

def imageURLs(preview, original):
    previewUrl = "https://" + WEBSITE_URL + "/images/" + preview
    originalUrl = "https://" + WEBSITE_URL + "/images/" + original
    return [{"type": "image", "previewImageUrl":previewUrl , "originalContentUrl":originalUrl}]
def replyText(string):
    return [{"type" :"text", "text": string}]

messages = {
    # "入力メッセージ":["text","text","内容"], #文字情報の場合
    # "画像メッセージ":["image"] + imageURLs("画像のプレビュー.jpg", "高解像度版.jpg") # imagesフォルダ内の画像を参照。

    "こんにちは":replyText("こんにちは!"),
    "はじめまして":replyText("はじめまして！私はチャットボットです。"),
    "テスト": replyText("チャットボットのテスト"),
    "website": replyText(WEBSITE_URL),
    "画像": imageURLs("img01-preview.jpg","img01-hq.jpg"),

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
        "messages": messages[text]
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
