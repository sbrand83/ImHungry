from django.shortcuts import redirect, render

def home_page(request):
    return render(request, 'home.html')

def map(request):
    # TODO: handle case where lat/lng not supplied
    lat = float(request.GET.get('lat', '200'))
    lng = float(request.GET.get('lng', '200'))

    if abs(lat) > 90 or abs(lng) > 180:
        return redirect('/')

    return render(request, 'map.html', {
        'lat': lat,
        'lng': lng
    })
