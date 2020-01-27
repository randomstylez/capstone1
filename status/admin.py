from django.contrib import admin
from django.core.exceptions import ValidationError

from status.mail_sender import MailSender

# Register your models here.
from .models import ServicesDescriptions
from .models import BusinessService
from .models import ServicesCategory
from .models import ServicesHistory
from .models import Subscribers
from .models import ServicesStatus
from .models import ServiceHistoryStatus

from status.forms import *


@admin.register(ServicesDescriptions)
class ServicesDescriptionsAdmin(admin.ModelAdmin):
    list_display = ('business_service', 'description')
    search_fields = ['business_service', 'description']
    list_filter = ('business_service',)
    ordering = ['business_service']


@admin.register(BusinessService)
class BusinessServicesAdmin(admin.ModelAdmin):
    list_display = ('business_service_name', 'business_service_description')
    ordering = ['business_service_name']


@admin.register(ServicesCategory)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('tag', 'color')
    ordering = ['tag']


def notify_users(modeladmin, request, queryset):
    queryset.update(notify_action=True)


notify_users.short_description = "Notify users about ticket"


def notify_action(obj):
    return obj


notify_action.short_description = 'Name'


class ServiceHistoryStatusInline(admin.StackedInline):
    model = ServiceHistoryStatus
    formset = ServiceHistoryStatusInlineFormset
    extra = 0
    ordering = ("action_date",)


@admin.register(ServicesStatus)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('status',)
    ordering = ['status']


@admin.register(ServicesHistory)
class ServicesHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'business_service', 'service_category', 'service_status', 'begin', 'end',
                    'notify_action')
    # fields = ['business_service', 'service_category', ('begin', 'end'), 'action_description', 'action_notes']

    fieldsets = [
        ('Service on process', {'fields': ['business_service', 'ticket_id', 'service_category', 'service_status']}),
        ('Date information', {'fields': ['begin', 'end']}),
        # ('Additional Information', {'fields': ['action_description', 'action_notes', 'closing_notes']}),
        ('Additional Information', {'fields': ['action_description', 'action_notes']}),
        (None, {'fields': ['notify_action']}),
    ]

    inlines = [ServiceHistoryStatusInline]

    readonly_fields = ['service_status', 'notify_action']

    search_fields = ['business_service', 'service_category', 'service_status']
    list_filter = ('business_service', 'service_category', 'service_status',)
    ordering = ['end']

    actions = [notify_users]

    form = ServicesHistoryForm

    @staticmethod
    def notify_user(business_service_id):

        # It gets all the users who belong to that Business Service
        users_mail = Subscribers.objects.filter(business_service=business_service_id)

        for user in users_mail:
            text = f"""\
                        Changes on the ticket:
                        """

            html = f"""\
                        <html>
                          <body>
                            <p>Changes on the ticket<br>
                            </p>
                          </body>
                        </html>
                        """

            mail_sender = MailSender(html, text, user.email)
            mail_sender.send_mail()

    # def save_related(self, request, obj, forms, change):
    def save_formset(self, request, form, formset, change):

        change_detected = False

        # Detect changes in the main form
        if form.changed_data:
            change_detected = True

        # Detect changes in the child forms (inline forms/Service Histories)
        my_list = []
        for _form in formset:
            my_list.append(_form.cleaned_data['service_status'].status)
            if _form.has_changed():
                change_detected = True

        good_to_save = True

        # Update the Service Status with the last value specified in the Service Status List
        if change_detected:

            # It checks for multiple 'Completed' status on the Service Status List
            # print(_form.cleaned_data['service_status'])
            # for result in _form.cleaned_data:
            #     print(result)
            # my_list = [_form.cleaned_data[result].status for result in _form.cleaned_data if result == 'service_status']

            # if [item for item in set(my_list) if my_list.count(item) > 1].count('Completed'):
            #     print("Error")
            #     good_to_save = False

            # It checks for the proper specification of a 'Completed' status. It must be at the last status object
            if good_to_save and formset.cleaned_data:

                # It gets the latest service's status specified on the Service Status List
                service_status = formset.cleaned_data[-1]['service_status']
                # It retrieves the service status' id given its value
                service_status_id = ServicesStatus.objects.get(status=service_status)

                # Check for errors in the Service Status List
                if service_status.status != 'Completed' and \
                        any('Completed' in result['service_status'].status for result in formset.cleaned_data):
                    print("Error")
                    good_to_save = False
                else:
                    print("Good to save")

                    # It modifies the ticket's status given the last service status history specified
                    # obj.instance.service_status_id = service_status_id.pk
                    form.instance.service_status_id = service_status_id.pk
                    # obj.save()
                    form.instance.save()

            if good_to_save:
                # super().save_related(request, obj, forms, change)
                formset.save()

                # It sends the Business Service's ID to notify all the users subscribed
                # self.notify_user(obj.cleaned_data['business_service'].pk)
                self.notify_user(form.cleaned_data['business_service'].pk)
            else:
                formset.save(commit=False)

        # # It calls the saving function but specifying that no changes has been made
        # print(change)
        # # super().save_related(request, obj, forms, change)
        formset.save(commit=False)


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']
    ordering = ['name']



