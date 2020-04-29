import secrets
from datetime import timedelta
from itertools import chain

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .forms import SubscriberDataForm
from .forms import SubscriberForm
from .models import SubService, Ticket, Status, Service, TicketLog, Region, Subscriber, \
    EmailDomain


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
        status_list = Status.objects.all()
        context['status_list'] = status_list

        # Getting today's date
        today = timezone.now()
        list_of_five_days = [today]

        counter = 1
        while counter < 5:
            list_of_five_days.append(today - timedelta(days=counter))
            counter = counter + 1

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
                queryset = Region.objects.filter(name=region)
                for e in queryset:
                    client_domain_services = e.client_domains.all().exclude(services__name=None). \
                        values('services__name')
                    services = list(set(chain(services, client_domain_services.all().exclude(services__name=None).
                                              values_list('services__name', flat=True))))
                services.sort()
                context['services_list'] = services

            context['regions_checked'] = regions

        elif 'search_services' in request.GET:

            search_value = request.GET['search']
            services_list = []
            for service in services:
                if search_value.lower() in service.name.lower():
                    services_list.append(service)

            if not services_list:
                context['no_search_results'] = True

            context['services_list'] = services_list
            context['search_value'] = search_value

        else:
            # Getting list of services
            services = []
            services = list(dict.fromkeys(chain(services, Service.objects.all())))
            context['services_list'] = services

        # Declaring an empty dictionary to store status per day for each service
        service_status = {}
        no_issues = Status.objects.filter(tag='No Issues')[0]

        # Getting list of tickets associated with each service
        for service in services:

            subservices = SubService.objects.filter(topology__service__name=service)

            # Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            for subservice in subservices:
                queryset = Ticket.objects.filter(sub_service=subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            status_per_day = []
            for day in list_of_five_days:
                active_tickets_per_day = tickets_list.filter(begin__lte=day).exclude(end__lte=day)

                if active_tickets_per_day:

                    # Separating tickets in groups by priority
                    priority_tickets = []
                    medium_priority_tickets = []
                    low_priority = []

                    for ticket in active_tickets_per_day:

                        status = ticket.status.tag
                        if status == "In Process" or status == "Alert" or status == "Outage":
                            priority_tickets.append(ticket)
                        elif status == "Planned":
                            medium_priority_tickets.append(ticket)
                        else:
                            low_priority.append(ticket)

                    if priority_tickets:
                        status_per_day.append(priority_tickets[0].status)
                    elif medium_priority_tickets:
                        status_per_day.append(medium_priority_tickets[0].status)
                    elif low_priority:
                        status_per_day.append(low_priority[0].status)
                    else:
                        status_per_day.append(no_issues)

                else:
                    status_per_day.append(no_issues)

            status_per_day.reverse()
            service_status[service] = status_per_day

        context['status'] = service_status

        return render(request, self.template_name, context)


# Subscription page
class SubscriptionView(View):

    template_name = "subscription.html"

    def get(self, request, service_id=None, *args, **kwargs):
        """
        Method to:
        - update a process in case a user requested a
        subscription without selecting any services or sub-services
        - update a subscription given a service
        (coming from the service status history page and taking a service value by default)
        :param request:
        :param _id:
        :param args:
        :param kwargs:
        :return:
        """
        # Getting values previously entered by user if any
        user_name = request.GET.get('user_name')
        user_email = request.GET.get('subscriber_email')

        # If the user did a registration attempt before show entered values
        if user_email:
            form = SubscriberDataForm(initial={'name': user_name, 'email': user_email})
        else:
            form = SubscriberDataForm()

        context = {"form": form, "subscription_active": True, 'subscribed': False}

        if service_id is not None:
            obj = get_object_or_404(Service, id=service_id)
            context['object'] = obj
            context['service_specific'] = True
        else:
            service_specific = request.GET.get('service_specific')

            if service_specific:
                if service_specific == "False":
                    context['service_specific'] = False
                else:
                    context['service_specific'] = True
            else:
                context['service_specific'] = False

            context['object_passed'] = request.GET.get('object')

            # If an update was requested but the user did not enter a valid email
            update_email = request.GET.get('email')

            context['update_email'] = update_email

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Method to support the creation of a subscription.
        Here it will done all the verifications related to a new subscription
        1.0 - No service or sub-service selected
        2.0 - New subscriber, wrong email domain
        3.0 - Existing subscriber (existing email)
        3.1.- Existing subscriber (existing email, wrong Name) ## This one is not developed
        4.0 - New subscriber, proper information

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        generate_token = secrets.token_hex(16)

        form = SubscriberDataForm(request.POST, initial={'token': generate_token})

        context = {"form": form,  "subscription_active": True}

        service_specific = request.POST.get('service_specific')

        if 'one_service' in request.POST:
            context['one_service'] = request.POST.get('one_service')

        if 'subs_updates' in request.POST:
            context['subs_updates'] = request.POST.get('subs_updates')

        context['service_specific'] = False
        if service_specific == 'True':
            context['service_specific'] = True

        object_passed = request.POST.get('object')
        if object_passed:
            context['object_passed'] = object_passed

        # It requests to create a subscription
        if 'subs_updates' in request.POST:

            if form.is_valid():

                # Getting email entered by user
                email = form.cleaned_data['email']

                # Passing email to template
                context["subscriber_email"] = email

                # Getting name entered by the user
                name = form.cleaned_data['name']

                # Passing user name to template
                context["user_name"] = name

                # It verifies if the email belongs to the Email Domain list
                if not form.check_mail_domain():
                    context['email_domain_forbidden'] = True

                    # Getting list of approved domains
                    email_domain_list = EmailDomain.objects.all()

                    # Passing list ot template
                    context['email_domain_list'] = email_domain_list

                else:
                    if 'one_service' in request.POST:
                        _id = request.POST['one_service']
                        service = get_object_or_404(Service, id=_id)

                        # If the user is not registered before save it
                        if not Subscriber.objects.filter(email=email).exists():

                            # ************HERE WE NEED TO VERIFY USER EMAIL FIRST*******************
                            subscriber = form.save()
                            # Add service to the user account
                            subscriber.services.add(service)
                            subscriber.save()

                        else:
                            # If the user is already registered we just need to add the selected
                            # services and sub-services to the subscription
                            # Get user from database
                            user = Subscriber.objects.filter(email=email)[:1].get()

                            # Get user subservices
                            user_subservices = user.subservices.all()

                            # Get list of subservices to add
                            subservices_to_add = form.cleaned_data["subservices"]

                            # Add service to the user account
                            user.services.add(service)
                            user.save()

                            # Add subservices to the user account
                            for subservice_to_add in subservices_to_add:
                                if subservice_to_add not in user_subservices:
                                    user.subservices.add(subservice_to_add)
                                    user.save()

                        context['subscribed'] = True

                    else:
                        # If the user selected at least one service or subservice
                        if len(form.cleaned_data['services']) or len(form.cleaned_data['subservices']):
                            # If the user is not registered before save it
                            if not Subscriber.objects.filter(email=email).exists():
                                # ************HERE WE NEED TO VERIFY USER EMAIL FIRST*******************
                                # subscriber = form.save()
                                form.save()
                                SubscriberDataForm.notify_user_email(form)
                                context['subscribed'] = True
                            else:
                                # Here we know that the email exist,
                                # but we have not verified the username
                                context['user_exists'] = True
                                context['user_exists_email'] = email
                                context['updated_left'] = True

                        else:
                            context['no_selection'] = True
                            context['subscribed'] = False

        # It requests to update the subscription information
        # after having requested a subscription
        elif 'update_subs' in request.POST:

            # Getting the email entered by the user
            user_email = request.POST.get('user_email', None)

            if user_email:
                # Check if this email is registered for notifications
                if Subscriber.objects.filter(email=user_email).exists():

                    # Send the email with the link to update subscription
                    SubscriberForm.send_link_by_user_email(str(user_email))

                    # Email has been sent, update template
                    if request.POST.get('updated_left', None):
                        context['updated_left'] = True
                    else:
                        context['updated_right'] = True
                else:
                    context['not_registered'] = True
                    context['email_entered'] = user_email
            else:
                context['empty_email'] = True

        return render(request, self.template_name, context)


# Services Status History Visualization page
class ServiceHistoryView(View):
    template_name = "ss_history_visualization.html"

    def get(self, request, service_id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        searching = False

        if service_id is not None:
            obj = get_object_or_404(Service, id=service_id)
            context['object'] = obj

            # Getting all tickets affecting this service
            subservices = SubService.objects.filter(topology__service__name=obj.name)

            # Initializing queryset to empty
            tickets_list = Ticket.objects.none()

            # for every subservice:
            for subservice in subservices:
                queryset = Ticket.objects.filter(sub_service=subservice)
                if queryset:
                    tickets_list = tickets_list | queryset

            if 'search_tickets' in request.GET:
                search_value = request.GET['search']
                aux_list = []

                if search_value is not '':
                    for ticket in tickets_list:
                        if (search_value.lower() in ticket.ticket_id.lower()
                                or search_value.lower() in ticket.action_description.lower()
                                or search_value.lower() in ticket.status.tag.lower()):
                            aux_list.append(ticket)

                    tickets_list = aux_list
                    searching = True
                    context['search_value'] = search_value

            context['tickets_list'] = tickets_list

            if not tickets_list and not searching:
                context['no_tickets'] = True

            if not tickets_list and searching:
                context['no_results'] = True

        return render(request, self.template_name, context)


# Services Status History Details page
class ServiceHistoryDetailsView(ListView):
    template_name = "sh_details.html"

    def get(self, request, ticket_id=None, *args, **kwargs):

        context = {
            "active_nav": 1
        }

        if ticket_id is not None:
            # Getting ticket instance
            obj = get_object_or_404(Ticket, id=ticket_id)
            context['object'] = obj

            # Getting list of events associated with this ticket
            ticket_events = TicketLog.objects.filter(ticket=obj)
            context['ticket_events'] = ticket_events

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
            prev = index - 1

            if prev >= 0:
                ticket = service_tickets[prev]
                context['prev_ticket'] = ticket

            # Getting index of previous ticket
            _next = index + 1

            if _next <= count - 1:
                ticket = service_tickets[_next]
                context['next_ticket'] = ticket

        return render(request, self.template_name, context)


class ModifyUserSubscription(ListView):
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
            context['services_to_add'] = services_not_registered
        else:
            context['no_services_to_add'] = True

        # Getting the sub-services this user is not registered to
        queryset = SubService.objects.all()
        sub_services_not_registered = []

        for sub_service in queryset:
            if sub_service not in user_sub_services:
                sub_services_not_registered.append(sub_service)

        if sub_services_not_registered:
            context['subservices_to_add'] = sub_services_not_registered
        else:
            context['no_subservices_to_add'] = True

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Method to modify subscription.
        This will allow to add and remove services and sub-services
        """

        # Getting user by userID
        user_id = request.POST.get('user_id')
        user = Subscriber.objects.get(id=user_id)

        # Getting list of services to delete
        services_deleted = request.POST.getlist('selected_services')

        if services_deleted:
            # Deleting the services
            for service in services_deleted:
                model_service = Service.objects.filter(name=service)[:1].get()
                user.services.remove(model_service)

        # Getting list of sub_services to delete
        subservices_deleted = request.POST.getlist('selected_subservices')

        if subservices_deleted:
            # Deleting the subservices
            for subservice in subservices_deleted:
                model_subservice = SubService.objects.filter(name=subservice)[:1].get()
                user.subservices.remove(model_subservice)

        # Getting list of services to add
        services_added = request.POST.getlist('selected_services_to_add')

        if services_added:
            # Adding the services
            for service in services_added:
                model_service = Service.objects.filter(name=service)[:1].get()
                user.services.add(model_service)

        # Getting list of sub_services to add
        subservices_added = request.POST.getlist('selected_subservices_to_add')

        if subservices_added:
            # Adding the subservices
            for subservice in subservices_added:
                model_subservice = SubService.objects.filter(name=subservice)[:1].get()
                user.subservices.add(model_subservice)

        context = {
            'user': user,
            'services_list': services_deleted,
            'subservices_list': subservices_deleted,
            'services_list_added': services_added,
            'subservices_list_added': subservices_added
        }

        # If no changes were selected
        if not (services_deleted or subservices_deleted or services_added or subservices_added):
            context['no_changes'] = True
        else:
            context['completed'] = True

        return render(request, self.template_name, context)
