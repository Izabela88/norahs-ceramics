from django.views.generic import TemplateView

# Create your views here.
class Home(TemplateView):
    """Render about page"""

    template_name = "home/home.html"