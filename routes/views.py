

# Create your views here.

from django.http import JsonResponse
from .models import DailyReport
from datetime import date,timedelta
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import datetime
import pytz
from django.shortcuts import render ,redirect
from .models import Shop
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
# Find duplicates
duplicates = DailyReport.objects.values('date').annotate(count=Count('id')).filter(count__gt=1)

for d in duplicates:
    date_val = d['date']
    # Keep only the first row, delete others
    reports = DailyReport.objects.filter(date=date_val)
    first = reports.first()
    reports.exclude(id=first.id).delete()

print("Duplicates removed")


def today_routes(request):
    riyadh = pytz.timezone("Asia/Riyadh")
    today = datetime.now(riyadh).strftime("%A")

    # ✅ Friday Holiday
    if today == "Friday":
        return render(request, "routes/holiday.html", {
            "today": today
        })

    shops = Shop.objects.filter(
        day=today,
        is_active=True
    ).order_by("order")

    context = {
        "today": today,
        "shops": shops
    }

    return render(request, "routes/today.html", context)






def shop_map(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    return render(request, "routes/map.html", {"shop": shop})



def test_holiday(request):
    return render(request, "routes/holiday.html", {"today": "Friday"})


def daily_report(request):
    auto_create_missing_days()

    reports = DailyReport.objects.order_by("date")

    return render(request, "routes/daily_report.html", {
        "week_reports": reports
    })



def save_daily_report(request):
    if request.method == "POST":
        report_id = request.POST.get("id")   # 👈 NEW
        date_value = request.POST.get("date")  # 👈 NEW

        total = request.POST.get("total")
        fuel = request.POST.get("fuel")
        credit = request.POST.get("credit")
        status = request.POST.get("status")

        # 👉 If editing existing row
        if report_id:
            report = get_object_or_404(DailyReport, id=report_id)

        # 👉 If creating new row
        else:
            report, _ = DailyReport.objects.get_or_create(
                date=date_value
            )

        report.total_amount = total or 0
        report.fuel_expense = fuel or 0
        report.credit_amount = credit or 0
        report.status = status or "Pending"
        report.save()

        return JsonResponse({"success": True})




def add_shop(request):
    if request.method == "POST":
        Shop.objects.create(
            name=request.POST.get("name"),
            day=request.POST.get("day"),
            order=request.POST.get("order"),
            latitude=request.POST.get("lat"),
            longitude=request.POST.get("lng"),
            notes=request.POST.get("notes"),
            is_active=True
        )

        messages.success(request, "✅ Shop added successfully!")
        return redirect("today_routes")

    return render(request, "routes/add_shop.html")





# ✏️ Edit Shop
def edit_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == "POST":
        shop.name = request.POST.get("name")
        shop.day = request.POST.get("day")
        shop.order = request.POST.get("order")
        shop.latitude = request.POST.get("latitude")
        shop.longitude = request.POST.get("longitude")
        shop.is_active = True if request.POST.get("is_active") else False
        shop.save()
        return redirect("/")

    return render(request, "routes/edit_shop.html", {"shop": shop})


# 🗑 Delete Shop
def delete_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    shop.delete()
    return redirect("/")



from django.http import JsonResponse

def routes_by_day(request, day):
    day = day.lower()   # normalize
    shops = Shop.objects.filter(day__iexact=day)
    data = []

    for shop in shops:
        data.append({
            "id": shop.id,
            "name": shop.name,
            
        })

    return JsonResponse(data, safe=False)



def holiday(request):
    return render(request, "routes/holiday.html")



def delete_shop_ajax(request, shop_id):
    if request.method == "POST":
        shop = get_object_or_404(Shop, id=shop_id)
        shop.delete()
        return JsonResponse({
            "success": True,
            "message": "Shop deleted successfully"
        })

    return JsonResponse({"success": False}, status=400)




def auto_create_missing_days():
    today = date.today()

    for i in range(7):
        d = today - timedelta(days=i)

        DailyReport.objects.get_or_create(
            date=d,
            defaults={
                "total_amount": 0,
                "fuel_expense": 0,
                "credit_amount": 0,
                "status": "Pending"
            }
        )




