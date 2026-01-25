from django.db import models

# Create your models here.




class Shop(models.Model):

    DAY_CHOICES = [
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
    ]

    name = models.CharField(max_length=200)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    order = models.PositiveIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ["order"]


    def __str__(self):
        return f"{self.name} ({self.day} - {self.order})"







class DailyReport(models.Model):
    date = models.DateField(auto_now_add=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_expense = models.DecimalField(max_digits=10, decimal_places=2)

    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Received", "Received"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def net_amount(self):
        return self.total_amount - self.fuel_expense

    def __str__(self):
        return f"{self.date} - {self.net_amount()}"
