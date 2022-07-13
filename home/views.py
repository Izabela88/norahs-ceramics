from django.views.generic import TemplateView
from product.models import Product
from order.models import OrderProduct
from django.db.models import Count
from newsletter.forms import NewsletterUserForm
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from newsletter.models import NewsletterUser
from django.urls import reverse
from django.contrib import messages
from newsletter.mailchimp_utils import subscribe
from django.utils import timezone
import datetime


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["new_arrivals"] = Product.objects.all().order_by(
            "-created_at"
        )[:10]

        context["best_sellers"] = OrderProduct.objects.annotate(
            count=Count("product_id")
        ).order_by("-count")[:3]

        context["newsletter_email"] = NewsletterUserForm()
        return context


class NewsletterView(View):
    def post(self, request) -> HttpResponse:
        """Subscribe email address"""
        email_form = NewsletterUserForm(data=request.POST or None)
        if email_form.is_valid():
            email = email_form.cleaned_data["newsletter_email"]
            newsletter = NewsletterUser.objects.filter(email=email).first()
            if newsletter:
                newsletter.subscribe()
            else:
                data = NewsletterUser()
                data.email = email
                data.created_at = datetime.datetime.now(tz=timezone.utc)
                data.save()
            subscribe(email)
            messages.success(
                request,
                (
                    "Thank you for subscribe to our newsletter!"
                    " You will soon receive a notification on your e-mail."
                ),
            )
            return HttpResponseRedirect(reverse("home"))
        else:
            display_key_map = {
                "newsletter_email": "Newsletter Email",
            }
            for key, value in email_form.errors.items():
                display_key = display_key_map.get(key) or key
                messages.error(request, f"{display_key}: {value[0]}")

        return HttpResponseRedirect(reverse("home"))
