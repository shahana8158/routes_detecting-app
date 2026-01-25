from django.contrib import admin

# Register your models here.


from .models import Shop, DailyReport


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "day", "order", "is_active")
    list_filter = ("day", "is_active")
    search_fields = ("name",)
    ordering = ("day", "order")





admin.site.register(DailyReport)



