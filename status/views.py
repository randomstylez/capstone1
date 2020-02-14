from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import SubService, Ticket
from django.views import View


# Create your views here.

#Services Status Visualization page
class ServicesStatusView(View):
    template_name = "status/services_status.html"
    def get(self, request, *args, **kwargs):
        context = {
            "active_nav": 1
        }
        return render(request, self.template_name, context)

#Subscription page
class SubscriptionView(View):
    template_name = "status/subscription.html"
    def get(self, request, *args, **kwargs):
        context = {
            "active_nav": 2
        }
        return render(request, self.template_name, context)

#Services Status History Visualization page
class ServiceHistoryView(View):
    template_name = "status/ss_history_visualization.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {
            "active_nav": 1
        }
        if id is not None:
            obj = get_object_or_404(SubService, id=id)
            context['object'] = obj
        return render(request, self.template_name, context)

#Services Status History Details page
class ServiceHistoryDetails(View):
    template_name = "status/details.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {
            "active_nav": 1
        }
        if id is not None:
            obj = get_object_or_404(Ticket, id=id)
            context['object'] = obj
        return render(request, self.template_name, context)