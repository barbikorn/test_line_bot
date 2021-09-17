from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('4ZRY55GSeHgOzU/hB7MCzsm/un0vV+ANAx1k1zncpC0OHDvgGfsrp4nXuh8Yq18qZcK2MEwapt5hwBc6hkbSbR4QsRpmtj+MPDQIBvqJPkM66kqbH6ni3Vb+xiIJg4OCx58U+PKlozCplb9EWNWLowdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('287b0045c745bcf8c42894e649e8a7c3')

to_user_id = 'U6fb7d7a01a602d8c251674bc529ff211'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='%s: %s' % (event.source.user_id , event.message.text)))

@app.route("/push", methods=['GET'])
def push_noti():
    line_bot_api.push_message(
        to_user_id,
        TextSendMessage('Test Ja')
    )


if __name__ == "__main__":
    app.run()