from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def map(request):
    # TODO: handle case where lat/lng not supplied
    return render(request, 'map.html', {
        'lat': request.GET['lat'],
        'lng': request.GET['lng'],
    })
