from django.shortcuts import render
from .models import Guitars


def index(request):
    oldGuitars = Guitars.objects.all()
    guitars = []
    guitarTriple = []
    tripleCount = 0
    for guitar in oldGuitars:
        if tripleCount < 3:
            guitarTriple.append(guitar)
            tripleCount += 1
        if tripleCount == 3:
            guitars.append(guitarTriple)
            guitarTriple = []
            tripleCount = 0
    return render(request, 'index.html', context={'guitars': guitars})