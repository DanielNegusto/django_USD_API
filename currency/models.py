from django.db import models


class ExchangeRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"1 USD = {self.rate} RUB"
