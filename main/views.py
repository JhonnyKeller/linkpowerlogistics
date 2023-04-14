from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from geopy.geocoders import Nominatim
from .mixins import Directions
from .forms import quotationForm
from .models import information

# email imports
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.http import HttpResponseRedirect

'''
Basic view for routing
'''

def route(request):
    info = information.objects.all()
    geolocator = Nominatim(user_agent="myGeolocator", timeout=10)
    location = geolocator.geocode(info[0].business_location_zip_code, timeout=10)
    lat_a = location.latitude
    long_a = location.longitude
    location = geolocator.geocode(info[0].business_location_zip_code, timeout=10)
    lat_c = location.latitude
    long_c = location.longitude
    context = {
    "google_api_key": settings.API_KEY,
    "lat_a": lat_a,
    "long_a": long_a,
    "lat_c": lat_c,
    "long_c": long_c,
    }
    return render(request, 'home.html', context)


'''
Basic view for displaying a map
'''
def map(request):

    lat_a = request.GET.get("lat_a", None)
    long_a = request.GET.get("long_a", None)
    lat_b = request.GET.get("lat_b", None)
    long_b = request.GET.get("long_b", None)
    lat_c = request.GET.get("lat_c", None)
    long_c = request.GET.get("long_c", None)
    lat_d = request.GET.get("lat_d", None)
    long_d = request.GET.get("long_d", None)
    type = request.GET.get("type", None)
    pick_up_adress = request.GET.get("pick_up_adress", None)
    client_destination = request.GET.get("client_destination", None)
    string = request.GET.get("string",None)
    item_list = []
    stored_string = ''
    stored_value = 0

    #only call API if all 4 addresses are added
    if lat_a and lat_b and lat_c and lat_d:
        directions = Directions(
        lat_a=lat_a,
        long_a=long_a,
        lat_b=lat_b,
        long_b=long_b,
        lat_c=lat_c,
    	long_c=long_c,
        lat_d=lat_d,
        long_d=long_d,
        )
    else:
        return redirect(reverse('main:home'))
    if string != None:
        dic_list = {}
        items = string.split(";;")
        list_of_lists = []
        while len(items) > 0:
            x = 8
            list = []
            while x > 0:
                list.append(items[0])
                items.pop(0)
                x -= 1
            list_of_lists.append(list)
        stored_value = len(list_of_lists)
        for y in range(len(list_of_lists)):
            stored_string += str(y) + ","
            item_dic = {
            "name":list_of_lists[y][0],
            "quantity":list_of_lists[y][1],
            "width":list_of_lists[y][2] + list_of_lists[y][5],
            "height":list_of_lists[y][3] + list_of_lists[y][5],
            "depth":list_of_lists[y][4] + list_of_lists[y][5],
            "dimension":list_of_lists[y][5],
            "weight":list_of_lists[y][6] + list_of_lists[y][7],
            "weight_type":list_of_lists[y][7],
            "volume": int(list_of_lists[y][2]) * int(list_of_lists[y][3]) * int(list_of_lists[y][4]),
            "id": "id-" + str(y),
            "id_itemName": "id-itemName-" + str(y),
            "id_quantity": "id-quantity-" + str(y),
            "id_width": "id-width-" + str(y),
            "id_height": "id-height-" + str(y),
            "id_depth": "id-depth-" + str(y),
            "id_weight": "id-weight-" + str(y),
            "id_typemeasurement": "id-typemeasurement-" + str(y),
            "id_typeweight": "id-typeweight-" + str(y),
            "volume_id": "id-volume" + str(y),
            }
            item_list.append(item_dic)


    context = {
    	"google_api_key": settings.API_KEY,
    	"lat_a": lat_a,
    	"long_a": long_a,
    	"lat_b": lat_b,
    	"long_b": long_b,
    	"lat_c": lat_c,
    	"long_c": long_c,
    	"lat_d": lat_d,
    	"long_d": long_d,
    	"origin": f'{lat_b}, {long_b}',
    	"destination": f'{lat_d}, {long_d}',
    	"directions": directions,
        "type": type,
        "pick_up_adress":pick_up_adress,
        "client_destination":client_destination,
        "item_list":item_list,
        "stored_value":stored_value,
        "stored_string":stored_string,
	}
    return render(request, 'main/removals.html', context)

def quotation_forniture(request):
    info = information.objects.all()
    geolocator = Nominatim(user_agent="myGeolocator",timeout=10)
    location = geolocator.geocode(info[0].business_location_zip_code, timeout=10)
    lat_a = location.latitude
    long_a = location.longitude
    location = geolocator.geocode(info[0].business_location_zip_code, timeout=10)
    lat_c = location.latitude
    long_c = location.longitude
    string = request.GET.get("string", None)
    lat_b = request.GET.get("lat_b", None)
    long_b = request.GET.get("long_b", None)
    lat_d = request.GET.get("lat_d", None)
    long_d = request.GET.get("long_d", None)
    pick_up_adress = request.GET.get("pick_up_adress", None)
    client_destination = request.GET.get("client_destination", None)
    stage = request.POST.get("stage", '1')
    manpower = request.POST.get("manpower", '0')
    floor = request.POST.get("floor", '0')
    day = request.POST.get("day", '0')
    time = request.POST.get("time", '0')
    car_brand = request.POST.get("car_brand", '0')
    car_model = request.POST.get("car_model", '0')
    number_of_rooms = request.POST.get("number_of_rooms", '0')
    name = request.POST.get("name", '0')
    email = request.POST.get("email", '0')
    phone_number = request.POST.get("phone_number", '0')
    type = request.GET.get("type", '0')
    form = quotationForm()
    total_quotation = 0
    item_list = []
    if type == '0':
        type = 'cars'
    if type == 'cars' and stage == '1':
        stage = '4'
    if type == 'homeremovals' and stage == '1':
        stage = '7'
    directions = Directions(
    lat_a=lat_a,
    long_a=long_a,
    lat_b=lat_b,
    long_b=long_b,
    lat_c=lat_c,
    long_c=long_c,
    lat_d=lat_d,
    long_d=long_d,
    )
    total_volume = 0
    total_weight = 0

    if request.method == 'POST':
        if string != None:
            dic_list = {}
            total_volume = 0
            total_weight = 0

            items = string.split(";;")
            list_of_lists = []
            if info[0].activate_dimension_prices == True:
                while len(items) > 0:
                    x = 8
                    list = []
                    while x > 0:
                        list.append(items[0])
                        items.pop(0)
                        x -= 1
                    list_of_lists.append(list)
                for y in range(len(list_of_lists)):
                    md = list_of_lists[y][5]
                    w = int(list_of_lists[y][2])
                    h = int(list_of_lists[y][3])
                    d = int(list_of_lists[y][4])
                    weight_type = list_of_lists[y][7]
                    weight = int(list_of_lists[y][6])
                    if weight_type == 'Lbs':
                        weight = weight * 0,4536
                    if md == 'm':
                        w = w * 100
                        h = h * 100
                        d = d * 100
                    if md == 'in':
                        w = w * 2.54
                        h = h * 2.54
                        d = d * 2.54
                    if md == 'ft':
                        w = w * 30.48
                        h = h * 30.48
                        d = d * 30.48

                    v = w * h * d
                    item_dic = {
                    "item_name":list_of_lists[y][0],
                    "item_unity":list_of_lists[y][1],
                    "item_volume":str(v) + "cm3"
                    }
                    item_list.append(item_dic)
                    total_weight += weight*int(list_of_lists[y][1])
                    total_volume += v*int(list_of_lists[y][1])
        dimension_to_charge = 0
        if total_volume != 0:
            total_volume = total_volume * info[0].volume_price_per_cm_cubic
            total_weight = total_weight * info[0].weight_price_per_kg
            if total_volume > total_weight:
                dimension_to_charge = total_volume
            else:
                dimension_to_charge = total_weight
        if dimension_to_charge != 0:
            if dimension_to_charge + (float(directions['distance'])*info[0].price_per_mile) < info[0].minimum_price:
                total_quotation = dimension_to_charge + (float(directions['distance'])*info[0].price_per_mile) + info[0].minimum_price
            else:
                total_quotation = dimension_to_charge + (float(directions['distance'])*info[0].price_per_mile) + (info[0].minimum_price/2)
        else:
            if float(directions['distance'])*info[0].price_per_mile < info[0].minimum_price:
                total_quotation = float(directions['distance'])*info[0].price_per_mile + info[0].minimum_price
            else:
                total_quotation = float(directions['distance'])*info[0].price_per_mile + (info[0].minimum_price/2)

        if number_of_rooms != '0' and stage == '2':
            if int(number_of_rooms) == 1:
                total_quotation = (int(number_of_rooms) * info[0].price_per_room_one) + (float(directions['distance'])*info[0].price_per_mile)
            if int(number_of_rooms) == 2:
                total_quotation = (int(number_of_rooms) * info[0].price_per_room_two) + (float(directions['distance'])*info[0].price_per_mile) + info[0].price_per_room_one
            if int(number_of_rooms) > 2:
                total_quotation  = (int(number_of_rooms) * info[0].price_per_room_three_plus) + (float(directions['distance'])*info[0].price_per_mile) + info[0].price_per_room_one + info[0].price_per_room_two


        if stage == '5':
            stage = '6'

            if string != None:
                dic_list = {}
                items = string.split(";;")
                list_of_lists = []
                while len(items) > 0:
                    x = 8
                    list = []
                    while x > 0:
                        list.append(items[0])
                        items.pop(0)
                        x -= 1
                    list_of_lists.append(list)
                stored_value = len(list_of_lists)
                for y in range(len(list_of_lists)):
                    item_dic = {
                    "name":list_of_lists[y][0],
                    "quantity":list_of_lists[y][1],
                    "width":list_of_lists[y][2] + list_of_lists[y][5],
                    "height":list_of_lists[y][3] + list_of_lists[y][5],
                    "depth":list_of_lists[y][4] + list_of_lists[y][5],
                    "dimension":list_of_lists[y][5],
                    "weight":list_of_lists[y][6] + list_of_lists[y][7],
                    "weight_type":list_of_lists[y][7],
                    "id": "id-" + str(y),
                    "id_itemName": "id-itemName-" + str(y),
                    "id_quantity": "id-quantity-" + str(y),
                    "id_width": "id-width-" + str(y),
                    "id_height": "id-height-" + str(y),
                    "id_depth": "id-depth-" + str(y),
                    "id_weight": "id-weight-" + str(y),
                    "id_typemeasurement": "id-typemeasurement-" + str(y),
                    "id_typeweight": "id-typeweight-" + str(y),
                    }
                    item_list.append(item_dic)
            item_list_len = len(item_list)

            link_to_google_maps = "google.com/maps/dir/" + info[0].business_location_zip_code + "/" + pick_up_adress + "/" + client_destination
            template = loader.get_template('contact_form.txt')
            email_context = {
                'name' : name,
                'email': email,
                'day':day,
                'time':time,
                'phone_number' : phone_number,
                'total_quotation':int(total_quotation),
                "item_list": item_list,
                "item_list_len":item_list_len,
                "number_of_rooms":number_of_rooms,
            }
            message = template.render(email_context)
            email_forclient = EmailMultiAlternatives (
                "Link Power Logistics", message,
                'linkpowerlogistics@gmail.com',
                [email],
            )

            # Convert the html and css inside the [contact_form.txt] to HTML templete
            email_forclient.content_subtype = 'html'
            email_forclient.send()

            template = loader.get_template('quote_form.txt')
            email_context = {
                'name' : name,
                'email': email,
                'phone_number' : phone_number,
                'day':day,
                'time':time,
                'total_quotation':int(total_quotation),
                'link_to_google_maps':link_to_google_maps,
                "type": type,
                "item_list": item_list,
                "item_list_len":item_list_len,
                "number_of_rooms":number_of_rooms,
            }
            quote_message = template.render(email_context)
            quote_email = EmailMultiAlternatives (
                "Link Power Logistics",
                quote_message,
                'linkpowerlogistics@gmail.com',
                 [info[0].email]
            )

            # Convert the html and css inside the [contact_form.txt] to HTML templete
            quote_email.content_subtype = 'html'
            quote_email.send()


    context = {
        "day":day,
        "number_of_rooms":number_of_rooms,
        "time":time,
        "google_api_key": settings.API_KEY,
        "stage": stage,
        "type": type,
        "car_brand": car_brand,
        "car_model": car_model,
        "item_list": item_list,
        "total_quotation":int(total_quotation),
        "form": form,
        "lat_a":lat_a,
        "long_a":long_a,
        "lat_b":lat_b,
        "long_b":long_b,
        "lat_c":lat_c,
        "long_c":long_c,
        "lat_d":lat_d,
        "long_d":long_d,
        "origin": f'{lat_b}, {long_b}',
    	"destination": f'{lat_d}, {long_d}',
        "directions":directions,
        "pick_up_adress":pick_up_adress,
        "client_destination":client_destination,
        "string":string,
	}


    return render(request,'main/quotation_forniture.html', context)

def privacy(request):
    return render(request,'privacy.html')
