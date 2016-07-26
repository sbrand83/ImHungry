from django.shortcuts import redirect, render
import math

def home_page(request):
    return render(request, 'home.html')

def map(request):
    lat = request.GET.get('lat', '200')
    lng = request.GET.get('lng', '200')

    try:
        lat = float(lat)
        lng = float(lng)
    except:
        return redirect('/')

    # TODO: send back error value or something so user can be made aware of error
    if abs(lat) > 90 or abs(lng) > 180 or math.isnan(lat) or math.isnan(lng):
        return redirect('/')

    return render(request, 'map.html', {
        'lat': lat,
        'lng': lng
    })
