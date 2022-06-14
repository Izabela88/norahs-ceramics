from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def get_or_create_user_basket(self):
        from basket.models import Basket

        user_basket = (
            Basket.objects.filter(customer_id=self.id)
            .order_by("-created_at")
            .first()
        )
        if not user_basket:
            user_basket = Basket.objects.create(customer_id=self.id)
        return user_basket
