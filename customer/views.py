from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.forms import UpdatePersonalInformationForm, AddressForm
from django.contrib import messages
from customer.models import User
from django.views.generic.edit import DeleteView
from django.views.generic import ListView, DetailView

import sweetify
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from order.models import Order, OrderProduct


class CustomerProfileView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "account_login"

    def get(self, request: HttpRequest, id) -> HttpResponse:
        context = {
            "personal_info_form_errors": request.session.pop(
                "personal_info_form_errors", None
            ),
            "address_form_errors": request.session.pop(
                "address_form_errors", None
            ),
            "personal_information_form": UpdatePersonalInformationForm(
                instance=request.user
            ),
            "address_information_form": AddressForm(
                instance=request.user.address_details
            ),
        }
        return render(request, "customer/customer_profile.html", context)

    def post(self, request, id):
        personal_info_form = UpdatePersonalInformationForm(
            instance=request.user, data=request.POST or None
        )

        if personal_info_form.is_valid() and personal_info_form.has_changed():
            sweetify.toast(
                self.request,
                "your personal information has been updated successfully!",
                position="top",
                timer=3000,
            )
            personal_info_form.save()

        else:
            request.session[
                "personal_info_form_errors"
            ] = personal_info_form.errors

        return HttpResponseRedirect(
            reverse("customer_profile", kwargs={"id": id})
        )


class CustomerAddressView(View):
    def post(self, request, id):
        address_form = AddressForm(
            instance=request.user.address_details, data=request.POST or None
        )
        if address_form.is_valid() and address_form.has_changed():
            address_form.save(commit=True)
            if request.user.address_details_id != address_form.instance.id:
                # Update existed address
                request.user.address_details_id = address_form.instance.id
                request.user.save()
            sweetify.toast(
                self.request,
                "your address information has been updated successfully!",
                position="top",
                timer=3000,
            )
        else:
            request.session["address_form_errors"] = address_form.errors

        return HttpResponseRedirect(
            reverse("customer_profile", kwargs={"id": id})
        )


class DeleteCustomerProfile(DeleteView):
    model = User
    template_name = "confirm_delete_profile.html"

    def get_success_url(self):
        sweetify.toast(
            self.request,
            "your account has been deleted successfully",
            icon="info",
        )
        return reverse("home")


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    model = User
    template_name = "change_password.html"
    success_message = "your password has been changed successfully"
    success_url = reverse_lazy("home")


class CustomerOrderHistoryListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login/"
    redirect_field_name = "account_login"
    model = Order
    paginate_by = 3
    template_name = "customer/customer_orders.html"

    def get_queryset(self):
        user_order = Order.objects.filter(user=self.request.user).all()
        return user_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()
        context["orders_data"] = {}
        for order in orders:
            products_with_qty = {}
            for order_product in order.order_products.all():
                if order_product.product_id in products_with_qty:
                    products_with_qty[order_product.product_id]["qty"] += 1
                    products_with_qty[order_product.product_id][
                        "name"
                    ] = order_product.product.name
                else:
                    products_with_qty[order_product.product_id] = {
                        "qty": 1,
                        "name": order_product.product.name,
                    }
            context["orders_data"][order.id] = [
                v for _, v in products_with_qty.items()
            ]

        return context
