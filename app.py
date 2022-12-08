import openai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# APIキー
openai.api_key = ""

# 対話モデルを設定する
engine = "text-davinci-003"

# flaskのインスタンス
app = Flask(__name__)

# LINEアクセス関係
ACCESS_TOKEN = ""
CHANNEL_SECRET = ""
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


def make_reply(message):
    # 返信を作成
    response = openai.Completion.create(
        engine=engine,
        prompt="あなたはLINEチャットボットです。以下の質問に答えてください。「"+message+"」",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 対話結果を取得する
    result = ""
    for choice in response.choices:
        if str(choice.text) == "\n":
            continue
        if str(choice.text) == "":
            continue
        result += str(choice.text)
    print(result)
    
    #先頭の改行を削除し return
    return result.lstrip("\n")

# 動作確認用
@app.route("/")
def test():
    return "<h1>It Works!</h1>"

# LINEbot用
@app.route("/callback", methods=['POST'])
def callback():
		signature = request.headers['X-Line-Signature']

		body = request.get_data(as_text=True)
		app.logger.info("Request body: " + body)

		try:
			handler.handle(body, signature)
		except InvalidSignatureError:
			print("Invalid signature. Please check your channel access token/channel secret.")
		return 'OK'

# ヘッダーを設定
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=make_reply(event.message.text))
        )
