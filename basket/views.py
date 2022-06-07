from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


class Basket(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, "basket/basket.html", context)
