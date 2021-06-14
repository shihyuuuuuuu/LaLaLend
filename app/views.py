# Create your views here.
import copy
import json
import os
import random

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, FlexSendMessage, ButtonsTemplate, URITemplateAction

if os.environ.get('DJANGO_PROD'):
    from src.production import DOMAIN, MEDIA_DOMAIN
else:
    from src.settings import DOMAIN, MEDIA_DOMAIN

from .forms import DemandForm, SupplyForm
from .models import Demand, Supply
from .schema import Category

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def confirm_data(user_id, data):
    mapping = {
        "item": "商品",
        "city": "縣市",
        "district": "鄉鎮市區",
        "category": "商品分類",
        "price_low": "價錢（低）",
        "price_high": "價錢（高）"
    }

    message = [f"{mapping[i]}: {data[i]}" for i in data]
    message[3] = f"商品分類: {data['category'].value}"
    message = ["您剛剛提交的表單："] + message
    message = "\n".join(message)

    line_bot_api.push_message(
        to=user_id,
        messages=TextSendMessage(text=message)
    )

def get_flex_message(recommend):
    flex_message = json.load(open('app/recommend.json','r',encoding='utf-8'))
    product = flex_message["contents"][0]
    contents = []

    for rec in recommend:
        photo = rec[0].photo.name
        product["hero"]["url"] = f"{MEDIA_DOMAIN}{photo}"
        product["body"]["contents"][0]["text"] = rec[0].item
        product["body"]["contents"][1]["contents"][1]["text"] = f"距離 {rec[2]}"
        product["body"]["contents"][2]["contents"][1]["text"] = f"${rec[0].price}"
        product["footer"]["contents"][0]["contents"][0]["text"] = f"Line ID: {rec[0].line_id}"
        product["footer"]["contents"][1]["contents"][0]["text"] = f"電話： {rec[0].phone_num}"
        contents.append(copy.deepcopy(product))
    flex_message["contents"] = contents

    return flex_message

def home(request):
    if request.method == "GET":
        products = Supply.objects.all()
        randomlist = []
        result = []

        for i in range(0,30):
            n = random.randint(0,len(products)-1)
            randomlist.append(n)

        for i in randomlist:
            p = {
                "photo": products[i].photo.url,
                "name": products[i].item if len(products[i].item) < 35 else products[i].item[:35] + "...",
                "price": products[i].price,
                "date": products[i].created_at,
                "description": products[i].description if len(products[i].description) < 70 else products[i].description[:70] + "...",
            }
            result.append(p)

        context = {
            "item_list": result,
        }
        
    return render(request, '../templates/home.html', context=context)

def product_form(request):
    user_id = request.GET['user_id']
    mode = request.GET['mode']

    if request.method == 'POST':
        geolocater = Nominatim(user_agent='lalalend')
        if mode == "demand":
            form = DemandForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                confirm_data(user_id, data)
                location = geolocater.geocode(f"{data['district']} {data['city']}")
                product = Demand(
                    user_id = user_id,
                    item = data["item"],
                    category = data["category"],
                    location_long = location.longitude,
                    location_lat = location.latitude,
                    price_low = data["price_low"],
                    price_high = data["price_high"],
                )
                product.save()
                recommend = product.recommend()
                flex_message = get_flex_message(recommend)
                if flex_message["contents"]:
                    line_bot_api.push_message(
                        to=user_id,
                        messages=TextSendMessage(text="你可能感興趣的商品：")
                    )
                    line_bot_api.push_message(
                        to=user_id,
                        messages=FlexSendMessage(
                            alt_text="LaLaLEND 為您推薦",
                            contents=flex_message
                        )
                    )
                else:
                    line_bot_api.push_message(
                        to=user_id,
                        messages=TextSendMessage(text="抱歉，目前沒有您想要的商品QQ")
                    )
        elif mode == "supply":
            form = SupplyForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                location = geolocater.geocode(f"{data['district']} {data['city']}")
                product = Supply(
                    user_id = user_id,
                    item = data["item"],
                    category = data["category"],
                    location_long = location.longitude,
                    location_lat = location.latitude,
                    description = data["description"] or "這個商品沒有描述",
                    photo = data["photo"],
                    price = data["price"],
                    line_id = data["line_id"],
                    phone_num = data["phone_num"]
                )
                product.save()
                recommend = product.recommend()
                user_ids = {i[0].user_id for i in recommend}
                flex_message = get_flex_message([[product, 0, "5~10 公里"]])
                for id in user_ids:
                    line_bot_api.push_message(
                        to=id,
                        messages=TextSendMessage(text="你可能感興趣的商品：")
                    )
                    line_bot_api.push_message(
                        to=id,
                        messages=FlexSendMessage(
                            alt_text="LaLa LEND 為您推薦",
                            contents=flex_message
                        )
                    )
        return render(request, '../templates/thank_u.html')
    else:
        category = [tag.value for tag in Category]
        if mode == "demand":
            context = {'form': DemandForm(), 'category': category}
            page = "demand"
        elif mode == "supply":
            context = {'form': SupplyForm(), 'category': category}
            page = "supply"
        return render(request, f'../templates/{page}.html', context)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                print(event.message.text)
                user_id = event.source.user_id
                if event.message.text == "我想要借用":
                    message = TemplateSendMessage(
                        alt_text = 'Buttons template',
                        template=ButtonsTemplate(
                            title='歡迎光臨 LaLaLEND 速速借!!',
                            text='快來告訴我們你想借用什麼？',
                            actions=[
                                URITemplateAction(
                                    label = "填寫借用表單",
                                    uri = f"{DOMAIN}/form?mode=demand&user_id={user_id}"
                                ),
                                URITemplateAction(
                                    label = "看看平台上的商品",
                                    uri = f"{DOMAIN}"
                                ),
                            ]
                        )
                    )
                elif event.message.text == "我想要出租":
                    message = TemplateSendMessage(
                        alt_text = 'Buttons template',
                        template=ButtonsTemplate(
                            title='歡迎光臨 LaLaLEND 速速借!!',
                            text='快來告訴我們你想出租什麼？',
                            actions=[
                                URITemplateAction(
                                    label = "填寫出租表單",
                                    uri = f"{DOMAIN}/form?mode=supply&user_id={user_id}"
                                ),
                                URITemplateAction(
                                    label = "看看平台上的商品",
                                    uri = f"{DOMAIN}"
                                ),
                            ]
                        )
                    )
                else:
                    message = TextSendMessage(text="請點選下方按鈕")
                line_bot_api.reply_message(
                    event.reply_token,
                    message
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
