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
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("richard OKOK")
    if (event.reply_token ==  '00000000000000000000000000000000'):#加這一條讓機器人被加好友時，不會回傳錯誤
	    return None
    text = event.message.text
    print(text)
    
    if text == 'profile':
        if isinstance(event.source, SourceUser):  #isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + str(profile.status_message))
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))


@handler.add(FollowEvent)
def handle_follow(event):
    print('In FollowEvent')
    print('event.source.type = '+event.source.type)
    print('event.source.user_id = '+event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))
    #follow event:當群組加入好友會收到此Message
    #可以reply message給使用者 You can reply to follow events.


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print('In UnfollowEvent')
    print('event.type = '+event.type)
    print('event.source.user_id = '+event.source.user_id)
    app.logger.info("Got Unfollow event")
    #使用者封鎖群組:會觸發此event!


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined event.source.type= ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
