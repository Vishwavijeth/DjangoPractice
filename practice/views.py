from django.http import HttpResponse
from pathlib import Path
from templates import 'home.html'

this_dir = Path(__file__).resolve().parent

def HomePageView(request, *args, **kwargs):
    return HttpResponse("<h1> Hello world </h1>")