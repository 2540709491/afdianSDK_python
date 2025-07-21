import hashlib
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

class OrderInfo:
    def __init__(self, out_trade_no, user_id, plan_id, month, total_amount, show_amount,
                 status, remark, redeem_id, product_type, discount, sku_detail,
                 create_time, user_name, plan_title, user_private_id,
                 address_person, address_phone, address_address):
        """
        订单信息类，用于封装从爱发电平台返回的订单数据。

        参数说明：
            out_trade_no         订单号
            custom_order_id      自定义信息（若存在）
            user_id              下单用户ID
            plan_id              方案ID，如为自选方案则为空
            title                订单描述
            month                赞助月份
            total_amount         真实付款金额，如有兑换码，则为 0.00
            show_amount          显示金额，如有折扣则为折扣前金额
            status               订单状态，2 表示交易成功
            remark               订单留言
            redeem_id            兑换码ID
            product_type         商品类型，0 表示常规方案，1 表示售卖方案
            discount             折扣金额
            sku_detail           如果为售卖类型，以数组形式表示具体型号
            create_time          创建时间，秒级时间戳
            user_name            下单用户名
            plan_title           对应方案的标题
            user_private_id      用户私有ID，可用于标识唯一用户
            address_person       收件人姓名
            address_phone        收件人电话
            address_address      收件人地址

        返回值：
            初始化一个 OrderInfo 实例，包含完整的订单信息。
        """

        # 订单号
        self.out_trade_no = out_trade_no

        # 下单用户ID
        self.user_id = user_id

        # 方案ID，如为自选方案则为空
        self.plan_id = plan_id

        # 赞助月份
        self.month = month

        # 真实付款金额，如有兑换码，则为 0.00
        self.total_amount = total_amount

        # 显示金额，如有折扣则为折扣前金额
        self.show_amount = show_amount

        # 订单状态，2 表示交易成功
        self.status = status

        # 订单留言
        self.remark = remark

        # 兑换码ID
        self.redeem_id = redeem_id

        # 商品类型，0 表示常规方案，1 表示售卖方案
        self.product_type = product_type

        # 折扣金额
        self.discount = discount

        # 如果为售卖类型，以数组形式表示具体型号
        self.sku_detail = sku_detail

        # 创建时间，秒级时间戳
        self.create_time = create_time

        # 下单用户名
        self.user_name = user_name

        # 对应方案的标题
        self.plan_title = plan_title

        # 用户私有ID，可用于标识唯一用户
        self.user_private_id = user_private_id

        # 收件人姓名
        self.address_person = address_person

        # 收件人电话
        self.address_phone = address_phone

        # 收件人地址
        self.address_address = address_address

    def __repr__(self):
        return f"<OrderInfo(out_trade_no='{self.out_trade_no}', user_name='{self.user_name}', plan_title='{self.plan_title}', total_amount='{self.total_amount}')>"
class CheckInfo:
    def __init__(self, ec, em, has_new_msg, unread_message_num, comment_unread, like_unread, message_unread,
                 unread_post_num, notice_bar_key, polling_interval, ip, country, province, city, county, area,
                 isp, is_abroad, is_gui, debug_uid, debug_ua):
        self.ec = ec
        self.em = em
        self.has_new_msg = has_new_msg
        self.unread_message_num = unread_message_num
        self.unread_count = {
            "comment": comment_unread,
            "like": like_unread,
            "message": message_unread
        }
        self.unread_post_num = unread_post_num
        self.notice_bar_key = notice_bar_key
        self.config = {
            "polling_interval": polling_interval
        }
        self.ip_info = {
            "ip": ip,
            "country": country,
            "province": province,
            "city": city,
            "county": county,
            "area": area,
            "isp": isp,
            "is_abroad": is_abroad,
            "is_gui": is_gui
        }
        self.debug = {
            "uid": debug_uid,
            "ua": debug_ua
        }

    @staticmethod
    def from_json(json_data):
        data = json_data.get("data", {})
        unread_count = data.get("unread_count", {})

        return CheckInfo(
            ec=json_data.get("ec"),
            em=json_data.get("em"),
            has_new_msg=data.get("has_new_msg"),
            unread_message_num=data.get("unread_message_num", 0),
            comment_unread=unread_count.get("comment", 0),
            like_unread=unread_count.get("like", 0),
            message_unread=unread_count.get("message", 0),
            unread_post_num=data.get("unread_post_num", 0),
            notice_bar_key=data.get("notice_bar_key", ""),
            polling_interval=data.get("config", {}).get("polling_interval", 0),
            ip=data.get("ip_info", {}).get("ip", ""),
            country=data.get("ip_info", {}).get("country", ""),
            province=data.get("ip_info", {}).get("province", ""),
            city=data.get("ip_info", {}).get("city", ""),
            county=data.get("ip_info", {}).get("county", ""),
            area=data.get("ip_info", {}).get("area", ""),
            isp=data.get("ip_info", {}).get("isp", ""),
            is_abroad=data.get("ip_info", {}).get("is_abroad", 0),
            is_gui=data.get("ip_info", {}).get("is_gui", 0),
            debug_uid=data.get("debug", {}).get("uid", ""),
            debug_ua=data.get("debug", {}).get("ua", "")
        )

    def __repr__(self):
        return f"<CheckInfo(ec={self.ec}, em='{self.em}', has_new_msg={self.has_new_msg}, " \
               f"unread_message_num={self.unread_message_num}, unread_post_num={self.unread_post_num})>"
class AddressInfo:
    def __init__(self, name: str, phone: str, address: str, address_id: str,
                 province: List[str], city: List[str], area: List[str],
                 street: List[str], exact_address: str, area_type: str):
        self.name = name
        self.phone = phone
        self.address = address
        self.address_id = address_id
        self.province = province
        self.city = city
        self.area = area
        self.street = street
        self.exact_address = exact_address
        self.area_type = area_type
class ShippingFeeConfig:
    def __init__(self, id: int, name: str, user_id: str, status: int,
                 template_type: int, fee_type: int, base_fee: str,
                 base_fee_count: int, addup_fee: str, addup_count: int,
                 create_time: int, update_time: int):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.status = status
        self.template_type = template_type
        self.fee_type = fee_type
        self.base_fee = base_fee
        self.base_fee_count = base_fee_count
        self.addup_fee = addup_fee
        self.addup_count = addup_count
        self.create_time = create_time
        self.update_time = update_time
class SkuDetail:
    def __init__(self, sku_id: str, price: str, count: int, name: str,
                 album_id: str, pic: str, stock: int, post_id: str):
        self.sku_id = sku_id
        self.price = price
        self.count = count
        self.name = name
        self.album_id = album_id
        self.pic = pic
        self.stock = stock
        self.post_id = post_id
class PlanInfo:
    def __init__(self, plan_id: str, rank: int, user_id: str, status: int,
                 name: str, pic: str, desc: str, price: str, update_time: int,
                 timing_on: int, timing_off: int, timing_sell_on: int,
                 timing_sell_off: int, pay_month: int, show_price: str,
                 show_price_after_adjust: str, favorable_price: float,
                 independent: int, permanent: int, can_buy_hide: int,
                 need_address: int, product_type: int, sale_limit_count: int,
                 need_invite_code: bool, bundle_stock: int,
                 bundle_sku_select_count: int, config: List[Any],
                 has_plan_config: int, shipping_fee_info: Dict[str, Any]):
        self.plan_id = plan_id
        self.rank = rank
        self.user_id = user_id
        self.status = status
        self.name = name
        self.pic = pic
        self.desc = desc
        self.price = price
        self.update_time = update_time
        self.timing = {
            "timing_on": timing_on,
            "timing_off": timing_off,
            "timing_sell_on": timing_sell_on,
            "timing_sell_off": timing_sell_off
        }
        self.pay_month = pay_month
        self.show_price = show_price
        self.show_price_after_adjust = show_price_after_adjust
        self.favorable_price = favorable_price
        self.independent = independent
        self.permanent = permanent
        self.can_buy_hide = can_buy_hide
        self.need_address = need_address
        self.product_type = product_type
        self.sale_limit_count = sale_limit_count
        self.need_invite_code = need_invite_code
        self.bundle_stock = bundle_stock
        self.bundle_sku_select_count = bundle_sku_select_count
        self.config = config
        self.has_plan_config = has_plan_config
        self.shipping_fee_info = shipping_fee_info
class ExtInfo:
    def __init__(self, address: AddressInfo, shipping_fee: int,
                 shipping_fee_config: ShippingFeeConfig, agreement_npp: int,
                 free_shipping_set: List[Any], card_id_list: List[Any],
                 ticket_session_id: str, cmid: str, custom_order_id: str,
                 sku_detail: str, sku_count: int, product_type: int):
        self.address = address
        self.shipping_fee = shipping_fee
        self.shipping_fee_config = shipping_fee_config
        self.agreement_npp = agreement_npp
        self.free_shipping_set = free_shipping_set
        self.card_id_list = card_id_list
        self.ticket_session_id = ticket_session_id
        self.cmid = cmid
        self.custom_order_id = custom_order_id
        self.sku_detail = sku_detail
        self.sku_count = sku_count
        self.product_type = product_type
class OrderContent:
    def __init__(self, cart_order_no: str, out_trade_no: str, show_amount: str,
                 total_amount: str, per_month: str, month: int, discount: str,
                 is_upgrade: int, remark: str, ext: ExtInfo, product_type: int,
                 sku_detail: List[SkuDetail], sku_count: int, time_range: Dict[str, int],
                 py_type: int):
        self.cart_order_no = cart_order_no
        self.out_trade_no = out_trade_no
        self.show_amount = show_amount
        self.total_amount = total_amount
        self.per_month = per_month
        self.month = month
        self.discount = discount
        self.is_upgrade = is_upgrade
        self.remark = remark
        self.ext = ext
        self.product_type = product_type
        self.sku_detail = sku_detail
        self.sku_count = sku_count
        self.time_range = time_range
        self.py_type = py_type
class MessageContent:
    def __init__(self, content_type: int, content_data: Any):
        self.type = content_type
        self.content = content_data

        # 处理不同类型的内容
        if content_type == 2:  # 订单类型
            self.order_info = self._parse_order_info(content_data)
        elif content_type == 4 or content_type == 5:  # 文本类型
            self.text = str(content_data)
        else:
            self.raw_content = content_data

    def _parse_order_info(self, order_data: Dict[str, Any]) -> OrderContent:
        """解析订单信息"""
        # 解析地址信息
        ext_data = order_data.get("ext", {})
        address_info = AddressInfo(
            name=ext_data.get("address", {}).get("name", ""),
            phone=ext_data.get("address", {}).get("phone", ""),
            address=ext_data.get("address", {}).get("address", ""),
            address_id=ext_data.get("address", {}).get("address_id", ""),
            province=ext_data.get("address", {}).get("province", []),
            city=ext_data.get("address", {}).get("city", []),
            area=ext_data.get("address", {}).get("area", []),
            street=ext_data.get("address", {}).get("street", []),
            exact_address=ext_data.get("address", {}).get("exact_address", ""),
            area_type=ext_data.get("address", {}).get("area_type", "")
        )

        # 解析运费配置
        shipping_fee_config = ShippingFeeConfig(
            id=ext_data.get("shipping_fee_config", {}).get("id", 0),
            name=ext_data.get("shipping_fee_config", {}).get("name", ""),
            user_id=ext_data.get("shipping_fee_config", {}).get("user_id", ""),
            status=ext_data.get("shipping_fee_config", {}).get("status", 0),
            template_type=ext_data.get("shipping_fee_config", {}).get("template_type", 0),
            fee_type=ext_data.get("shipping_fee_config", {}).get("fee_type", 0),
            base_fee=ext_data.get("shipping_fee_config", {}).get("base_fee", "0.00"),
            base_fee_count=ext_data.get("shipping_fee_config", {}).get("base_fee_count", 0),
            addup_fee=ext_data.get("shipping_fee_config", {}).get("addup_fee", "0.00"),
            addup_count=ext_data.get("shipping_fee_config", {}).get("addup_count", 0),
            create_time=ext_data.get("shipping_fee_config", {}).get("create_time", 0),
            update_time=ext_data.get("shipping_fee_config", {}).get("update_time", 0)
        )

        # 解析SKU详情
        sku_details = []
        for sku_data in order_data.get("sku_detail", []):
            sku_details.append(SkuDetail(
                sku_id=sku_data.get("sku_id", ""),
                price=sku_data.get("price", "0.00"),
                count=sku_data.get("count", 0),
                name=sku_data.get("name", ""),
                album_id=sku_data.get("album_id", ""),
                pic=sku_data.get("pic", ""),
                stock=sku_data.get("stock", 0),
                post_id=sku_data.get("post_id", "")
            ))

        # 解析Plan信息
        plan_data = order_data.get("plan", {})
        plan_info = PlanInfo(
            plan_id=plan_data.get("plan_id", ""),
            rank=plan_data.get("rank", 0),
            user_id=plan_data.get("user_id", ""),
            status=plan_data.get("status", 0),
            name=plan_data.get("name", ""),
            pic=plan_data.get("pic", ""),
            desc=plan_data.get("desc", ""),
            price=plan_data.get("price", "0.00"),
            update_time=plan_data.get("update_time", 0),
            timing_on=plan_data.get("timing", {}).get("timing_on", 0),
            timing_off=plan_data.get("timing", {}).get("timing_off", 0),
            timing_sell_on=plan_data.get("timing", {}).get("timing_sell_on", 0),
            timing_sell_off=plan_data.get("timing", {}).get("timing_sell_off", 0),
            pay_month=plan_data.get("pay_month", 0),
            show_price=plan_data.get("show_price", "0.00"),
            show_price_after_adjust=plan_data.get("show_price_after_adjust", "0.00"),
            favorable_price=plan_data.get("favorable_price", -1.0),
            independent=plan_data.get("independent", 0),
            permanent=plan_data.get("permanent", 0),
            can_buy_hide=plan_data.get("can_buy_hide", 0),
            need_address=plan_data.get("need_address", 0),
            product_type=plan_data.get("product_type", 0),
            sale_limit_count=plan_data.get("sale_limit_count", -1),
            need_invite_code=plan_data.get("need_invite_code", False),
            bundle_stock=plan_data.get("bundle_stock", 0),
            bundle_sku_select_count=plan_data.get("bundle_sku_select_count", 0),
            config=plan_data.get("config", []),
            has_plan_config=plan_data.get("has_plan_config", 0),
            shipping_fee_info=plan_data.get("shipping_fee_info", {})
        )

        return OrderContent(
            cart_order_no=order_data.get("cart_order_no", ""),
            out_trade_no=order_data.get("out_trade_no", ""),
            show_amount=order_data.get("show_amount", "0.00"),
            total_amount=order_data.get("total_amount", "0.00"),
            per_month=order_data.get("per_month", "0.00"),
            month=order_data.get("month", 0),
            discount=order_data.get("discount", "0.00"),
            is_upgrade=order_data.get("is_upgrade", 0),
            remark=order_data.get("remark", ""),
            ext=ExtInfo(
                address=address_info,
                shipping_fee=ext_data.get("shipping_fee", 0),
                shipping_fee_config=shipping_fee_config,
                agreement_npp=ext_data.get("agreement_npp", 0),
                free_shipping_set=ext_data.get("free_shipping_set", []),
                card_id_list=ext_data.get("card_id_list", []),
                ticket_session_id=ext_data.get("ticket_session_id", ""),
                cmid=ext_data.get("cmid", ""),
                custom_order_id=ext_data.get("custom_order_id", ""),
                sku_detail=ext_data.get("sku_detail", ""),
                sku_count=ext_data.get("sku_count", 0),
                product_type=ext_data.get("product_type", 0)
            ),
            product_type=order_data.get("product_type", 0),
            sku_detail=sku_details,
            sku_count=order_data.get("sku_count", 0),
            time_range=order_data.get("time_range", {}),
            py_type=order_data.get("py_type", 0)
        )
class MessageInfo:
    def __init__(self,msg_id: int, message_id: int, sender: str,
                 receive_status: int, msg_type: int, content: MessageContent,
                 send_time: int, message_type: str = "send"):
        self.msg_id = msg_id
        self.message_id = message_id
        self.sender = sender
        self.receive_status = receive_status  # 2表示已读
        self.type = msg_type  # 2表示订单，4表示文本，5表示激活码等
        self.content = content
        self.send_time = send_time
        self.send_time_str = datetime.fromtimestamp(send_time).strftime('%Y-%m-%d %H:%M:%S')
        self.message_type = message_type  # "send" 或 "receive"

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> List['MessageInfo']:
        """从JSON数据中解析创建MessageInfo实例"""
        messages = []
        # 获取消息列表
        message_list = json_data.get("data", {}).get("list", [])
        for item in message_list:
            # 跳过非消息项
            if "message" not in item:
                continue

            msg_data = item["message"]

            # 创建MessageContent实例
            content = MessageContent(
                content_type=msg_data.get("type", 0),
                content_data=msg_data.get("content", {})
            )

            # 创建MessageInfo实例
            message_info = MessageInfo(
                msg_id=msg_data.get("msg_id", 0),
                message_id=msg_data.get("id", 0),
                sender=msg_data.get("sender", ""),
                receive_status=msg_data.get("r_status", 0),
                msg_type=msg_data.get("type", 0),
                content=content,
                send_time=msg_data.get("send_time", 0),
                message_type=item.get("type", "send")
            )

            messages.append(message_info)

        return messages

    def __repr__(self):
        return f"<MessageInfo(msg_id={self.msg_id}, sender='{self.sender}', " \
               f"type={self.type}, send_time='{self.send_time_str}', message_type='{self.message_type}')>"
class SendMsgInfo:
    def __init__(self,ec:int,em:str, msg_id: str, message_id: int, sender: str,
                 receive_status: int, msg_type: str, content: str,
                 send_time: int):
        self.ec=ec
        self.em=em
        self.msg_id = msg_id
        self.message_id = message_id
        self.sender = sender
        self.receive_status = receive_status  # 1表示未读，2表示已读
        self.msg_type = msg_type  # 消息类型，如"1"表示文本消息
        self.content = content  # 消息内容
        self.send_time = send_time
        self.send_time_str = f"{send_time}"  # 可以根据需要格式化时间

    @staticmethod
    def from_json(json_data: dict) -> 'SendMsgInfo':
        """从JSON数据中解析创建SendMsgInfo实例"""
        data = json_data.get("data", {})
        message_data = data.get("message", {})

        return SendMsgInfo(
            ec=json_data.get("ec"),
            em=json_data.get("em"),
            msg_id=message_data.get("msg_id", ""),
            message_id=message_data.get("id", 0),
            sender=message_data.get("sender", ""),
            receive_status=message_data.get("r_status", 0),
            msg_type=message_data.get("type", ""),
            content=message_data.get("content", ""),
            send_time=message_data.get("send_time", 0)
        )

    def __repr__(self):
        return f"<SendMsgInfo(msg_id='{self.msg_id}', sender='{self.sender}', " \
               f"msg_type='{self.msg_type}', send_time='{self.send_time_str}')>"


def generate_sign(token, user_id, params, ts):
    # 将参数按签名规则拼接

    params_json = json.dumps(params)
    kv_string = f'params{params_json}ts{ts}user_id{user_id}'
    # 计算 MD5 签名
    sign = hashlib.md5((token + kv_string).encode('utf-8')).hexdigest()
    return sign
def send_request(user_id, token, api_url,params):
    # 获取当前时间戳（秒级）
    ts = int(time.time())



    # 生成 sign
    sign = generate_sign(token, user_id, params, ts)

    # 构造请求体
    payload = {
        "user_id": user_id,
        "params": json.dumps(params),
        "ts": ts,
        "sign": sign
    }

    # 发送 POST 请求
    response = requests.post(api_url, json=payload)

    return response.json()
def 获取订单信息():
    nowpage=1
    limitpage=1
    order_objects: List[OrderInfo] = []
    while nowpage<=limitpage:
        params = {"page": nowpage}
        result = send_request(user_id, token, order_api, params)

        limitpage=int(result.get('data',{}).get("total_page"))
        nowpage+=1
        # 解析订单数据
        orders_data = result.get("data", {}).get("list", [])
        for item in orders_data:
            order = OrderInfo(
                out_trade_no=item.get("out_trade_no"),
                user_id=item.get("user_id"),
                plan_id=item.get("plan_id"),
                month=item.get("month"),
                total_amount=item.get("total_amount"),
                show_amount=item.get("show_amount"),
                status=item.get("status"),
                remark=item.get("remark"),
                redeem_id=item.get("redeem_id"),
                product_type=item.get("product_type"),
                discount=item.get("discount"),
                sku_detail=item.get("sku_detail", []),
                create_time=item.get("create_time"),
                user_name=item.get("user_name"),
                plan_title=item.get("plan_title"),
                user_private_id=item.get("user_private_id"),
                address_person=item.get("address_person"),
                address_phone=item.get("address_phone"),
                address_address=item.get("address_address")
            )
            order_objects.append(order)
    return order_objects
def check(user_id ="",local_new_msg_id = ""):
    ts = int(time.time())
    params = {
        "local_new_msg_id": local_new_msg_id
    }
    sign = generate_sign(token, user_id, params, ts)
    payload = {
        "user_id": user_id,
        "params": json.dumps(params),
        "ts": ts,
        "sign": sign
    }
    headers = {
        "Referer": f"https://afdian.com/u/{user_id}/message",
        "Cookie": f"auth_token={auth_token}"
    }
    response = requests.post(f"{check_api}?local_new_msg_id={local_new_msg_id}", json=payload, headers=headers)
    return CheckInfo.from_json(response.json())
def messages(user_id, type="old", message_id=""):
    """
    获取消息列表

    参数:
        user_id: 用户ID
        type: 请求类型，可选值为"old"或""
        message_id: 消息ID，可选

    返回:
        返回从服务器获取的消息列表的JSON数据
    """
    ts = int(time.time())

    params = {
        "user_id": user_id,
        "type": type,
        "message_id":message_id
    }
    if message_id:
        params["message_id"] = message_id
    sign = generate_sign(token, user_id, params, ts)

    payload = {
        "user_id": user_id,
        "params": json.dumps(params),
        "ts": ts,
        "sign": sign
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Referer": f"https://afdian.com/message/{user_id}?is_keyboard_up=1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    cookie = f"auth_token={auth_token}"

    headers["Cookie"] = cookie
    response = requests.get(f"{messages_api}?user_id={user_id}&type={type}&message_id={message_id}",json=payload, headers=headers)
    print(response.json())
    return MessageInfo.from_json(response.json())
def send_message(user_id="",type="1",content=""):
    """
    发送消息

    参数:
        user_id: 接收者用户ID
        msg_type: 消息类型，如"1"表示文本消息
        content: 消息内容

    返回:
        返回从服务器获取的响应JSON数据
    """
    ts = int(time.time())
    params = {
        "user_id": user_id,
        "type": type,
        "content": content
    }
    sign = generate_sign(token, user_id, params, ts)
    payload = {
        "user_id": user_id,
        "params": json.dumps(params),
        "ts": ts,
        "sign": sign
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://afdian.com",
        "Referer": f"https://afdian.com/message/{user_id}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "locale-lang": "zh-CN"
    }

    cookie = f"auth_token={auth_token}"

    headers["Cookie"] = cookie

    json_data = f'{{\"user_id\":\"{user_id}\",\"type\":\"{type}\",\"content\":\"{content}\"}}'
    response = requests.post(send_message_api,data=json_data,json=payload, headers=headers)
    print(json_data)
    print(response.json())
    return SendMsgInfo.from_json(response.json())
# 配置信息
#user_id:从爱发电开发者后台获取::https://afdian.com/dashboard/dev
user_id = ""
#token:从爱发电开发者后台获取
token = ""
#auth_token:从cookie里获取
auth_token=""

order_api = "https://afdian.com/api/open/query-order"
check_api="https://afdian.com/api/my/check"
messages_api="https://afdian.com/api/message/messages"
send_message_api="https://afdian.com/api/message/send"
#获取订单信息()
#获取check信息
aaa=check("")
bbb=messages("","old")
ccc=send_message("","1","自动回复测试1")
print("111")
