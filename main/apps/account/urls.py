from django.urls import path
from . import views


urlpatterns = [
    path("list", views.UserList.as_view(), name="userlist"),
    path("add", views.UserAdd.as_view(), name="useradd"),
    path("edit/<int:id>", views.UserEdit.as_view(), name="useredit"),
    path("delete/<int:id>", views.UserDelete.as_view(), name="userdelete"),

    path("changepassword/<int:id>", views.UserChangePassword.as_view(), name="userchangepassword")
]