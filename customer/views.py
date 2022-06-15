from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse


class CustomerProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        return render(request, "customer/user_profile.html", context)


class CustomerAddressView(View):
    def post(self, request):
        pass
