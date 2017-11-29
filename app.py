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

line_bot_api = LineBotApi('GD2Npvmfyxm3V6NSbJ/zcDiuZHk/qgGrUZiTgWumMHDIRb66X+eB54rhf0HCXDgZXxHrDmj+Cu7d1gCSUbK7CqcsHUeJosi2QYPzn3mPaPl2lzYx+sefHW2kRJRs1nwER4SmO8ltGKn2GpTck3vHvQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('949cce0ad17b22f4616f9d3c2f025608')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()