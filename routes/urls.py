from django.urls import path
from .views import today_routes, shop_map,test_holiday, daily_report,save_daily_report, add_shop,delete_shop, edit_shop
from django.shortcuts import render




urlpatterns = [
    path("", today_routes, name="today_routes"),
    path("shop/<int:shop_id>/", shop_map, name="shop_map"),
    path("test-holiday/", test_holiday), 
     path("daily-report/", daily_report, name="daily_report"),
     path("save-report/", save_daily_report, name="save_report"),
    path("add-shop/", add_shop, name="add_shop"),
    path("shop/edit/<int:shop_id>/", edit_shop, name="edit_shop"),
    path("shop/delete/<int:shop_id>/", delete_shop, name="delete_shop"),

]
