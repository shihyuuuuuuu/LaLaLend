# Create your views here.
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from .forms import DemandForm, SupplyForm
from .models import Demand, Supply

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def fill_in_product(request):
    user_id = request.GET['user_id']
    mode = request.GET['mode']

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        if mode == "demand":
            form = DemandForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                product = Demand(
                    user_id = user_id,
                    username = data["username"],
                    item = data["item"],
                    location_long = data["location_long"],
                    location_lat = data["location_lat"],
                    price_low = data["price_low"],
                    price_high = data["price_high"],
                )
                product.save()
        elif mode == "supply":
            form = SupplyForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                product = Supply(
                    user_id = data["user_id"],
                    username = data["username"],
                    item = data["item"],
                    location_long = data["location_long"],
                    location_lat = data["location_lat"],
                    price_low = data["price_low"],
                    price_high = data["price_high"],
                )
                product.save()
        
        #     # redirect to a new URL:
        #     return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        if mode == "demand":
            form = DemandForm()
        elif mode == "supply":
            form = SupplyForm()

    context = {
        'form': form,
    }

    return render(request, '../templates/product_form.html', context)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()