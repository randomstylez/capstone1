import secrets

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import SubService, Ticket, StatusCategory,Service,TicketLog,SubServiceServices,Region,Subscriber
from django.views import View
from django.views.generic import ListView
from datetime import datetime, timedelta
from .forms import SubscriberForm
from .forms import SubscriberDataForm
from itertools import chain
from django.shortcuts import redirect
from status.mail_sender import MailSender

# Create your views here.

#Services Status Visualization page
class ServicesStatusView(View):

    template_name = "status/services_status.html"

    def get(self, request, *args, **kwargs):

        global services

        # Getting most recent 5 tickets
        queryset = Ticket.objects.all().order_by('begin').reverse()[:5]

        context = {
            "ticket_list": queryset,
            "active_nav": 1
        }

        # Getting list of status for legend
        queryset = StatusCategory.objects.all()
        context['category_list'] = queryset

        # Getting today's date
        today = datetime.now()
        list_of_five_days = [today]

        counter = 1
        while counter < 5:
            list_of_five_days.append(today-timedelta(days=counter))
            counter = counter+1


        context['days'] = list_of_five_days

        # Getting list of regions
        regions = Region.objects.all()
        context['region_list'] = regions


        if 'regions_select' in request.GET:

            #Getting checked regions
            regions = request.GET.getlist('regions')

            # Getting list of services
            services = []
            for region in regions:

                #Getting checked status to true
                context['checked_regions'] = regions

                #Getting list of services
                queryset = Region.objects.filter(region_name=region)
                for e in queryset:
                    services = list(dict.fromkeys(chain(services, e.services.all())))
                context['services_list'] = services

        elif 'search_services' in request.GET:

            searchfor = request.GET['search']
            services_list = []
            for service in services:
                if searchfor.lower() in service.service_name.lower():
                    services_list.append(service)

            context['services_list'] = services_list

        else:
            # Getting list of services
            services = []
            for region in regions:
                services = list(dict.fromkeys(chain(services, region.services.all())))

            context['services_list'] = services

        #Declaring an empty dictionary to store status per day for each service
        service_status = {}
        no_issues = StatusCategory()
        no_issues.status_category_tag = "No Issues"
        no_issues.status_category_color = "green"

        # Getting list of tickets associated with each service
        for service in services:

            sub_service_service = SubServiceServices.objects.filter(service=service)

            #Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for row in sub_service_service:
                queryset = Ticket.objects.filter(sub_service=row.subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            status_per_day = []
            for day in list_of_five_days:
                active_tickets_per_day = tickets_list.filter(begin__lte=day, end__gte=day-timedelta(1))

                if active_tickets_per_day:
                    #Separating tickets in groups by priority
                    priority_tickets = []
                    medium_priority_tickets = []
                    low_priority = []
                    for ticket in active_tickets_per_day:
                        status = ticket.category_status.status_category_tag
                        if status == "In Process" or status == "Alert" or status == "Outage":
                            priority_tickets.append(ticket)
                        elif status == "Planned":
                            medium_priority_tickets.append(ticket)
                        else:
                            low_priority.append(ticket)

                    if priority_tickets:
                        status_per_day.append(priority_tickets[0].category_status)
                    elif medium_priority_tickets:
                        status_per_day.append(medium_priority_tickets[0].category_status)
                    elif low_priority:
                        status_per_day.append(low_priority[0].category_status)
                    else:
                        status_per_day.append(no_issues)
                else:
                    status_per_day.append(no_issues)

            status_per_day.reverse()
            service_status[service] = status_per_day

        context['service_status'] = service_status

        return render(request, self.template_name, context)

#Subscription page
class SubscriptionView(View):
    template_name = "status/subscription.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {
            "active_nav": 2
        }

        form = SubscriberDataForm()
        context = {"form": form}

        context['subscribed'] = False

        if id is not None:
            obj = get_object_or_404(Service, id=id)
            context['object'] = obj
            context['service_specific'] = True
        else:
            context['service_specific'] = False

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        context = {
            "active_nav": 2
        }

        generate_token = secrets.token_hex(16)

        form = SubscriberDataForm(request.POST, initial={'token': generate_token})
        context = {"form": form}

        if 'subs_updates' in request.POST:

            if form.is_valid():
                subscriber = form.save()
                context['subscribed'] = True

            if 'one_service' in request.POST:
                id = request.POST['one_service']
                service = get_object_or_404(Service, id=id)
                subscriber.services.add(service)
                subscriber.save()

        elif 'update_subs' in request.POST:

            #Getting the email entered by the user
            user_email = request.POST.get('user_email', None)

            #Send the email with the link to update subscription
            SubscriberForm.send_link_by_user_email(str(user_email))

            #Email has been sent, update template
            context['updated'] = True

        return render(request, self.template_name, context)





#Services Status History Visualization page
class ServiceHistoryView(View):
    template_name = "status/ss_history_visualization.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {
            "active_nav": 1
        }
        if id is not None:
            obj = get_object_or_404(Service, id=id)
            context['object'] = obj

            #Getting all tickets affecting this service
            sub_service_service = SubServiceServices.objects.filter(service=obj)

            #Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for row in sub_service_service:
                queryset = Ticket.objects.filter(sub_service=row.subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            if 'search_tickets' in request.GET:
                searchfor = request.GET['search']
                aux_list = []

                for ticket in tickets_list:
                    if (searchfor.lower() in ticket.ticket_id.lower()
                            or searchfor.lower() in ticket.action_description.lower()
                            or searchfor.lower() in ticket.category_status.status_category_tag.lower()):
                        aux_list.append(ticket)

                tickets_list = aux_list


            context['tickets_list'] = tickets_list

            if not(tickets_list):
                context['no_tickets'] = True


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
            service_tickets = Ticket.objects.filter(sub_service=obj.sub_service).order_by('pk')
            context['service_tickets'] = list(service_tickets)

            #Getting number of tickets
            count = service_tickets.count()
            context['tickets_count'] = count

            #Getting index of this ticket
            index = service_tickets.filter(id__lt = obj.id).count()
            context['ticket_index'] = index

            #Getting previous ticket
            prev = index-1

            if prev >= 0:
                ticket = service_tickets[prev]
                context['prev_ticket'] = ticket

            # Getting index of previous ticket
            next = index + 1

            if next <= count-1:
                ticket = service_tickets[next]
                context['next_ticket'] = ticket

        return render(request, self.template_name, context)


class ModifyUserSubscription (ListView):

    template_name = "status/modify_subscription.html"

    def get(self, request, email, token):

        #Getting user by token
        user = Subscriber.objects.filter(token=token)[:1].get()

        context = {
            'user': user
        }

        #Getting the services for this user
        services = user.services.all()

        if services:
            context['services'] = services
        else:
            context['no_services'] = True

        # Getting the subservices for this user
        sub_services = user.subservices.all()

        if sub_services:
            context['sub_services'] = sub_services
        else:
            context['no_subservices'] = True

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        #Getting user by userID
        user_id = request.POST.get('user_id')
        user = Subscriber.objects.get(id=user_id)

        #Getting list of services to delete
        services = request.POST.getlist('selected_services')

        #Deleting the services
        for service in services:
            model_service = Service.objects.filter(service_name=service)[:1].get()
            user.services.remove(model_service)

        # Getting list of sub_services to delete
        subservices = request.POST.getlist('selected_subservices')

        # Deleting the subservices
        for subservice in subservices:
            model_subservice = SubService.objects.filter(sub_service_name=subservice)[:1].get()
            user.subservices.remove(model_subservice)

        context = {
            'completed' : True,
            'user': user,
            'services_list': services,
            'subservices_list': subservices
        }
        return render(request, self.template_name, context)