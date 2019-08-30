# encoding: utf-8
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

# 填入你的 message api 資訊
line_bot_api = LineBotApi('fITuFYiubGcdypB96vW35Bgz/AmTxvIC+5OTy9DHO85r0ukpGT4P6y83qYHT+nRw/zlSCQMS0d00o9WHVTqr07hrQ3YfOZ1gTbb9w5T7lpLuY/CI73Qk8fKknPBZWrWVNDMG6AbwsRD/R8e0PQMZ3AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fe25752be6177c2e9ba42ef05fc963f8')

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])