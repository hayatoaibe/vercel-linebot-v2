from flask import Flask, request, jsonify
import requests
import os
import csv

WEBSITE_URL = os.getenv('VERCEL_PROJECT_PRODUCTION_URL') # (アプリ名).vercel.app
LINE_ACCESS_TOKEN = os.getenv('LINE_API_TOKEN') # Vercel 環境変数 "LINE_API_TOKEN" (Enviromental Variables) にAPI トークンを設定
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

app = Flask(__name__)

def postImage(preview, original):
    previewUrl = "https://" + WEBSITE_URL + "/images/" + preview
    originalUrl = "https://" + WEBSITE_URL + "/images/" + original
    return [{"type": "image", "previewImageUrl":previewUrl , "originalContentUrl":originalUrl}]

def replyText(string):
    return [{"type" :"text", "text": string}]

messages = { 

    # ------------------------------チャットボットのメッセージ部分------------------------------
    
    # "入力メッセージ":replyText("こんにちは"), #文字情報の場合
    # "画像メッセージ":postImage("画像のプレビュー.jpg", "高解像度版.jpg"), # public/imagesフォルダ内の画像を参照。
    # "テスト": replyText("チャットボットのテスト"),
    # "website": replyText(WEBSITE_URL),
    "こんにちは":replyText("こんにちは!"),
    "はじめまして":replyText("はじめまして！私はチャットボットです。"),
    "画像": postImage("img01-preview.jpg","img01-hq.jpg"),

}

GENERAL_MESSAGE = ["すみません、うまく理解できませんでした。"] # 言葉に対応した返事ができない場合の文を書く

# CSVのメッセージを読み込み
with open('replies.csv',encoding="utf_8") as file:
  csv_reader = csv.reader(file)
  header = next(csv_reader) # 最初の1行は無視
  for row in csv_reader:
    messages.update({row[0] : replyText(row[1])})

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
        "messages": messages.get(text,GENERAL_MESSAGE)
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
