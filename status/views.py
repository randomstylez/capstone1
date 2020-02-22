from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import SubService, Ticket, StatusCategory,Service,TicketLog
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator


# Create your views here.

#Services Status Visualization page
class ServicesStatusView(View):
    template_name = "status/services_status.html"
    def get(self, request, *args, **kwargs):
        queryset = Ticket.objects.all()
        context = {
            "ticket_list": queryset,
            "active_nav": 1
        }
        queryset = Service.objects.all()
        context['services_list'] = queryset

        queryset = StatusCategory.objects.all()
        context['category_list'] = queryset

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
class ServiceHistoryDetailsView(ListView):
    template_name = "status/sh_details.html"

    def get(self, request, id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        if id is not None:
            #Getting ticket instance
            obj = get_object_or_404(Ticket, id=id)
            context['object'] = obj

            #Getting list of ticket logs associated with this ticket
            queryset = TicketLog.objects.filter(service_history=obj)
            context['ticket_logs'] = queryset

            #Getting list of tickets associated with the service
            service_tickets = Ticket.objects.filter(sub_service=obj.sub_service)

            #Pagination
            paginator = Paginator(service_tickets, 1)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj

        return render(request, self.template_name, context)