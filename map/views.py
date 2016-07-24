from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def map(request):
    return render(request, 'map.html', {
        'lat': request.GET['lat'],
        'lng': request.GET['lng'],
    })
