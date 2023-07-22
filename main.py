import os
from dotenv import load_dotenv
from flask import Flask, request, abort

app = Flask(__name__)

# 從環境變數中取得LINE的Channel Access Token
line_channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
print (os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
if line_channel_access_token is None:
  print("請設定LINE的Channel Access Token！")
  exit(1)


@app.route("/", methods=["POST"])
def line_webhook():
  # 確認請求是來自LINE的
  if request.headers["User-Agent"] != "LineBot":
    abort(400)

  # 取得LINE的請求內容
  body = request.get_json()

  # 處理接收到的訊息
  for event in body["events"]:
    reply_token = event["replyToken"]
    message_type = event["message"]["type"]
    user_id = event["source"]["userId"]

    if message_type == "text":
      # 回覆用戶的訊息（這裡直接回傳相同訊息）
      send_text_message(reply_token, event["message"]["text"])

  return "OK"


def send_text_message(reply_token, text):
  # 呼叫LINE的回覆訊息API
  headers = {
    "Authorization": "Bearer " + line_channel_access_token,
    "Content-Type": "application/json"
  }
  data = {
    "replyToken": reply_token,
    "messages": [{
      "type": "text",
      "text": text
    }]
  }
  response = request.post("https://api.line.me/v2/bot/message/reply",
                          headers=headers,
                          json=data)
  if response.status_code != 200:
    print("回覆訊息失敗:", response.status_code, response.text)


if __name__ == "__main__":
  app.run()
