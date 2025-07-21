# afdianSDK_python
基于python的爱发电SDK,支持订单获取,新消息检查,消息列表获取,发送信息&nbsp;
# 配置信息

#user_id:从爱发电开发者后台获取---><a href="https://afdian.com/dashboard/dev">爱发电开发者后台</a>&nbsp;
参数配置:&nbsp;
user_id = ""

#token:从爱发电开发者后台获取---><a href="https://afdian.com/dashboard/dev">爱发电开发者后台</a>&nbsp;

token = ""

#auth_token:从cookie里获取

auth_token=""

order_api = "https://afdian.com/api/open/query-order"&nbsp;

check_api="https://afdian.com/api/my/check"&nbsp;

messages_api="https://afdian.com/api/message/messages"&nbsp;

send_message_api="https://afdian.com/api/message/send"&nbsp;

示例调用:&nbsp;

获取订单信息()&nbsp;

aaa=check("userid")&nbsp;

bbb=messages("userid","type(old/new)")&nbsp;

ccc=send_message("userid","1","content")&nbsp;
