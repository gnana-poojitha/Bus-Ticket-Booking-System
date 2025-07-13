
# from django.urls import path
# from .views import create_checkout_session
# from .views import RegisterView, LoginView, BusListCreateView, UserBookingView, BookingView, BusDetailView

# urlpatterns = [
#     path('buses/', BusListCreateView.as_view(), name='buslist'),
#     path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),
#     path('register/', RegisterView.as_view(), name = 'register'),
#     path('login/', LoginView.as_view(), name = 'login'),
#     path('user/<int:user_id>/bookings/', UserBookingView.as_view(), name="user-bookings"),
#     path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
#     path('booking/', BookingView.as_view(), name="booking")
# ]
# from .views import ConfirmBookingAfterPayment

# urlpatterns += [
#     path('confirm-booking/', ConfirmBookingAfterPayment.as_view(), name='confirm-booking'),
# ]










from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    BusListCreateView,
    BusDetailView,
    UserBookingView,
    BookingView,
    create_checkout_session,
    ConfirmBookingAfterPayment,
)

urlpatterns = [
    path('buses/', BusListCreateView.as_view(), name='buslist'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:user_id>/bookings/', UserBookingView.as_view(), name="user-bookings"),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('booking/', BookingView.as_view(), name="booking"),
    path('confirm-booking/', ConfirmBookingAfterPayment.as_view(), name='confirm-booking'),
]
