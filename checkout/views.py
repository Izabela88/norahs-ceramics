from django.shortcuts import render
from django.views import View


class CheckoutView(View):

    def get(self, request):
        context = {}
        return render(request, "checkout/checkout.html", context)
