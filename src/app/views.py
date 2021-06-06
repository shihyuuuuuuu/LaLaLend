# Create your views here.
import copy
import json

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, FlexSendMessage, ButtonsTemplate, URITemplateAction

from .forms import DemandForm, SupplyForm
from .models import Demand, Supply
from .schema import Category

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def get_flex_message(recommend):
    flex_message = json.load(open('app/recommend.json','r',encoding='utf-8'))
    product = flex_message["contents"][0]
    contents = []

    for rec in recommend:
        product["hero"]["url"] = f"https://6f61d26a6d4c.ngrok.io/media/{rec[0].photo.name}"
        product["body"]["contents"][0]["text"] = rec[0].item
        product["body"]["contents"][1]["contents"][1]["text"] = f"距離 {rec[2]}"
        product["body"]["contents"][2]["contents"][1]["text"] = f"${rec[0].price}"
        product["footer"]["contents"][0]["action"]["label"] = "聯絡賣家"
        contents.append(copy.deepcopy(product))
    flex_message["contents"] = contents

    return flex_message

def product_form(request):
    user_id = request.GET['user_id']
    mode = request.GET['mode']

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        geolocater = Nominatim(user_agent='lalalend')
        if mode == "demand":
            form = DemandForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                location = geolocater.geocode(f"{data['district']} {data['city']}")
                product = Demand(
                    user_id = user_id,
                    username = data["username"],
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
                line_bot_api.push_message(
                    to=user_id,
                    messages=FlexSendMessage(
                        alt_text="LaLaLEND 為您推薦",
                        contents=flex_message
                    )
                )
        elif mode == "supply":
            form = SupplyForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                location = geolocater.geocode(f"{data['district']} {data['city']}")
                product = Supply(
                    user_id = user_id,
                    username = data["username"],
                    item = data["item"],
                    category = data["category"],
                    location_long = location.longitude,
                    location_lat = location.latitude,
                    description = data["description"],
                    photo = data["photo"],
                    price = data["price"],
                    line_id = data["line_id"],
                    phone_num = data["phone_num"]
                )
                product.save()
                recommend = product.recommend()
        
        return HttpResponse("謝啦！")
    # If this is a GET (or any other method) create the default form.
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
                if event.message.text == "哈囉":
                    message = TemplateSendMessage(
                        alt_text = 'Buttons template',
                        template=ButtonsTemplate(
                            title='歡迎光臨 LaLaLEND 速速借!!',
                            text='請問你想要......',
                            actions=[
                                URITemplateAction(
                                    label = "我想要借用",
                                    uri = f"https://6f61d26a6d4c.ngrok.io/form?mode=demand&user_id={user_id}"
                                ),
                                URITemplateAction(
                                    label = "我想要出租",
                                    uri = f"https://6f61d26a6d4c.ngrok.io/form?mode=supply&user_id={user_id}"
                                )
                            ]   
                        )
                    )
                    line_bot_api.reply_message(
                        event.reply_token,
                        message
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="通關密語是「哈囉」")
                    )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
