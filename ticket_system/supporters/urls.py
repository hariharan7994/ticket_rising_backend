from django.urls import path
from .views import SupporterRegisterView, SupporterLoginView, SupporterProfileView, SupporterLogoutView, SupporterListView, SupporterDetailView, DesignationListCreateView, DesignationDetailView


urlpatterns = [
    path("register/", SupporterRegisterView.as_view(), name="supporter-register"),
    path("login/", SupporterLoginView.as_view(), name="supporter-login"),
    path("profile/", SupporterProfileView.as_view(), name="supporter-profile"),
     path("logout/", SupporterLogoutView.as_view(), name="supporter-logout"),

      path("all/", SupporterListView.as_view(), name="supporter-list"),
    path("<int:pk>/", SupporterDetailView.as_view(), name="supporter-detail"),

     path("designations/", DesignationListCreateView.as_view(), name="designation-list-create"),
    path("designations/<int:pk>/", DesignationDetailView.as_view(), name="designation-detail"),
]
