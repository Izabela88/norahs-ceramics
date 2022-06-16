from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.forms import UpdatePersonalInformationForm


class CustomerProfileView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "account_login"

    def get(self, request: HttpRequest, id) -> HttpResponse:
        context = {
            "personal_info_form_errors": request.session.pop(
                "personal_info_form_errors", None
            ),
        }
        context["personal_information_form"] = UpdatePersonalInformationForm(
            instance=request.user
        )
        return render(request, "customer/customer_profile.html", context)

    def post(self, request, id):
        personal_info_form = UpdatePersonalInformationForm(
            instance=request.user, data=request.POST or None
        )

        if personal_info_form.is_valid() and personal_info_form.has_changed():
            personal_info_form.save()

        else:
            request.session[
                "personal_info_form_errors"
            ] = personal_info_form.errors

        return HttpResponseRedirect(
            reverse("customer_profile", kwargs={"id": id})
        )


class CustomerAddressView(View):
    def post(self, request):
        pass
