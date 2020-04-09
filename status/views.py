import secrets
from datetime import timedelta
from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .forms import SubscriberDataForm
from .forms import SubscriberForm
from .models import SubService, Ticket, StatusCategory, Service, TicketLog, SubServiceServices, Region, Subscriber


# Create your views here.

# Services Status Visualization page
class ServicesStatusView(View):

    template_name = "services_status.html"

    def get(self, request, *args, **kwargs):

        global services

        # Getting most recent 5 tickets
        queryset = Ticket.objects.all().order_by('begin').reverse()[:5]

        context = {
            "ticket_list": queryset,
            "service_active": True
        }

        # Getting list of status for legend
        queryset = StatusCategory.objects.all()
        context['category_list'] = queryset

        # Getting today's date
        today = timezone.now()
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

            # Getting checked regions
            regions = request.GET.getlist('regions')

            # Getting list of services
            services = []
            for region in regions:

                # Getting list of services
                queryset = Region.objects.filter(region_name=region)
                for e in queryset:
                    services = list(dict.fromkeys(chain(services, e.services.all())))
                context['services_list'] = services

            context['regions_checked'] = regions

        elif 'search_services' in request.GET:

            searchfor = request.GET['search']
            services_list = []
            for service in services:
                if searchfor.lower() in service.service_name.lower():
                    services_list.append(service)

            if not services_list:
                context['no_search_results'] = True

            context['services_list'] = services_list

        else:
            # Getting list of services
            services = []
            services = list(dict.fromkeys(chain(services, Service.objects.all())))
            context['services_list'] = services

        # Declaring an empty dictionary to store status per day for each service
        service_status = {}
        no_issues = StatusCategory()
        no_issues.status_category_tag = "No Issues"
        no_issues.status_category_color = "green"

        # Getting list of tickets associated with each service
        for service in services:

            sub_service_service = SubServiceServices.objects.filter(service=service)

            # Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for row in sub_service_service:
                queryset = Ticket.objects.filter(sub_service=row.subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            status_per_day = []
            for day in list_of_five_days:
                active_tickets_per_day = tickets_list.filter(begin__lte=day, end__gte=day-timedelta(1))

                if active_tickets_per_day:
                    # Separating tickets in groups by priority
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


# Subscription page
class SubscriptionView(View):

    template_name = "subscription.html"

    def get(self, request, id=None, *args, **kwargs):

        form = SubscriberDataForm()
        context = {"form": form, "subscription_active": True, 'subscribed': False}

        if id is not None:
            obj = get_object_or_404(Service, id=id)
            context['object'] = obj
            context['service_specific'] = True
        else:
            context['service_specific'] = False

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        generate_token = secrets.token_hex(16)

        form = SubscriberDataForm(request.POST, initial={'token': generate_token})

        context = {
            "form": form,
            "subscription_active": True
        }

        if 'subs_updates' in request.POST:

            if form.is_valid():
                # Getting email entered by user
                email = form.cleaned_data['email']

                if 'one_service' in request.POST:
                    id = request.POST['one_service']
                    service = get_object_or_404(Service, id=id)

                # If the user selected at least one service or subservice
                if len(form.cleaned_data['services']) or len(form.cleaned_data['subservices']) \
                        or ('one_service' in request.POST):
                    # If the user is not registered before save it
                    if not Subscriber.objects.filter(email=email).exists():
                        subscriber = form.save()
                        context['subscribed'] = True

                        if 'one_service' in request.POST:
                            subscriber.services.add(service)
                            subscriber.save()
                    else:  # Liz, can you check this?
                        context['user_exists'] = True
                        context['user_exists_email'] = email
                        context['updated_left'] = True

                else:
                    context['no_selection'] = True
                    context['subscribed'] = False

        elif 'update_subs' in request.POST:

            # Getting the email entered by the user
            user_email = request.POST.get('user_email', None)

            if user_email:

                # Check if this email is registered for notifications
                if Subscriber.objects.filter(email=user_email).exists():
                    # Send the email with the link to update subscription
                    SubscriberForm.send_link_by_user_email(str(user_email))

                    # Email has been sent, update template
                    context['updated_right'] = True
                else:
                    context['not_registered'] = True
            else:
                context['empty_email'] = True

        return render(request, self.template_name, context)


# Services Status History Visualization page
class ServiceHistoryView(View):

    template_name = "ss_history_visualization.html"

    def get(self, request, id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        searching = False

        if id is not None:
            obj = get_object_or_404(Service, id=id)
            context['object'] = obj

            # Getting all tickets affecting this service
            sub_service_service = SubServiceServices.objects.filter(service=obj)

            # Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for row in sub_service_service:
                queryset = Ticket.objects.filter(sub_service=row.subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            if 'search_tickets' in request.GET:
                searchfor = request.GET['search']
                aux_list = []

                if searchfor is not '':
                    for ticket in tickets_list:
                        if (searchfor.lower() in ticket.ticket_id.lower()
                                or searchfor.lower() in ticket.action_description.lower()
                                or searchfor.lower() in ticket.category_status.status_category_tag.lower()):
                            aux_list.append(ticket)

                    tickets_list = aux_list
                    searching = True

            context['tickets_list'] = tickets_list

            if not tickets_list and not searching:
                context['no_tickets'] = True

            if not tickets_list and searching:
                context['no_results'] = True

        return render(request, self.template_name, context)


# Services Status History Details page
class ServiceHistoryDetailsView(ListView):

    template_name = "sh_details.html"

    def get(self, request, id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        if id is not None:
            # Getting ticket instance
            obj = get_object_or_404(Ticket, id=id)
            context['object'] = obj

            # Getting list of ticket logs associated with this ticket
            queryset = TicketLog.objects.filter(service_history=obj)
            context['ticket_logs'] = queryset

            # Getting list of tickets associated with the service
            service_tickets = Ticket.objects.filter(sub_service=obj.sub_service).order_by('pk')
            context['service_tickets'] = list(service_tickets)

            # Getting number of tickets
            count = service_tickets.count()
            context['tickets_count'] = count

            # Getting index of this ticket
            index = service_tickets.filter(id__lt=obj.id).count()
            context['ticket_index'] = index

            # Getting previous ticket
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

    template_name = "modify_subscription.html"

    def get(self, request, email, token):

        # Getting user by token
        user = Subscriber.objects.filter(token=token)[:1].get()

        context = {
            'user': user
        }

        # Getting the services for this user
        user_services = user.services.all()

        if user_services:
            context['services'] = user_services
        else:
            context['no_services'] = True

        # Getting the subservices for this user
        user_sub_services = user.subservices.all()

        if user_sub_services:
            context['sub_services'] = user_sub_services
        else:
            context['no_subservices'] = True

        # Getting the services this user is not registered to

        queryset = Service.objects.all()
        services_not_registered = []

        for service in queryset:
            if service not in user_services:
                services_not_registered.append(service)

        if services_not_registered:
            context['services_toadd'] = services_not_registered
        else:
            context['no_services_toadd'] = True

        # Getting the sub-services this user is not registered to

        queryset = SubService.objects.all()
        sub_services_not_registered = []

        for sub_service in queryset:
            if sub_service not in user_sub_services:
                sub_services_not_registered.append(sub_service)

        if sub_services_not_registered:
            context['subservices_toadd'] = sub_services_not_registered
        else:
            context['no_subservices_toadd'] = True

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        # Getting user by userID
        user_id = request.POST.get('user_id')
        user = Subscriber.objects.get(id=user_id)

        # Getting list of services to delete
        service_list = request.POST.getlist('selected_services')

        if service_list:
            # Deleting the services
            for service in service_list:
                model_service = Service.objects.filter(service_name=service)[:1].get()
                user.services.remove(model_service)

        # Getting list of sub_services to delete
        subservices = request.POST.getlist('selected_subservices')

        if subservices:
            # Deleting the subservices
            for subservice in subservices:
                model_subservice = SubService.objects.filter(sub_service_name=subservice)[:1].get()
                user.subservices.remove(model_subservice)

        # Getting list of services to add
        services_add = request.POST.getlist('selected_services_toadd')

        if services_add:
            # Adding the services
            for service in services_add:
                model_service = Service.objects.filter(service_name=service)[:1].get()
                user.services.add(model_service)

        # Getting list of sub_services to add
        subservices_add = request.POST.getlist('selected_subservices_toadd')

        if subservices_add:
            # Adding the subservices
            for subservice in subservices_add:
                model_subservice = SubService.objects.filter(sub_service_name=subservice)[:1].get()
                user.subservices.add(model_subservice)

        context = {
            'user': user,
            'services_list': service_list,
            'subservices_list': subservices,
            'services_list_added': services_add,
            'subservices_list_added': subservices_add

        }

        # If no changes were selected
        if not (service_list or subservices or services_add or subservices_add):
            context['no_changes'] = True
        else:
            context['completed'] = True

        return render(request, self.template_name, context)
