from django.http import HttpResponse


def HomePageView(request, *args, **kwargs):
    return HttpResponse("<h1> Hello world </h1>")