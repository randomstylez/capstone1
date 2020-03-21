from django.urls import path

from .views import (
    ServicesStatusView,
    SubscriptionView,
    ServiceHistoryView,
    ServiceHistoryDetailsView
)

urlpatterns = [
    path('', ServicesStatusView.as_view(), name='services_status_view'),
    path('subscription/', SubscriptionView.as_view(), name='subscription_view'),
    path('<int:id>/', ServiceHistoryView.as_view(), name='service_history_view'),
    path('subscription/<int:id>/', SubscriptionView.as_view(), name='subscription_view'),
    path('details/<int:id>/', ServiceHistoryDetailsView.as_view(), name='service_history_details_view'),

]