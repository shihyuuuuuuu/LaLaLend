# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import DemandForm, SupplyForm
from .models import Demand, Supply

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