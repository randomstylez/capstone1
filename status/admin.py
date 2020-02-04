from django.contrib import admin

# Register your models here.
from .models import Service
from .models import SubService
from .models import StatusCategory
from .models import Ticket
from .models import TicketLog
from .models import Subscriber

from status.forms import *


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_description')
    search_fields = ['service_name', 'service_description']
    list_filter = ('service_name',)
    ordering = ['service_name']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('sub_service_name', 'sub_service_description')
    search_fields = ['services', 'service_name', 'service_description']
    list_filter = ('services',)
    ordering = ['sub_service_name']


@admin.register(StatusCategory)
class StatusCategoryAdmin(admin.ModelAdmin):
    list_display = ('status_category_tag', 'status_category_color')
    ordering = ['status_category_tag']


def notify_users(modeladmin, request, queryset):
    queryset.update(notify_action=True)
    # here we should call notify_user creating a query call with the ticket_id


notify_users.short_description = "Notify users about ticket"


def notify_action(obj):
    return obj


notify_action.short_description = 'Name'


class TicketHistoryInline(admin.StackedInline):
    model = TicketLog
    formset = TicketHistoryInlineFormset
    extra = 0
    ordering = ("action_date",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = ('ticket_id', 'sub_service', 'category_status', 'begin', 'end', 'notify_action')
    # fields = ['business_service', 'service_category', ('begin', 'end'), 'action_description', 'action_notes']

    fieldsets = [
        ('Sub-Service on process', {'fields': ['ticket_id', 'sub_service', 'category_status']}),
        ('Date information', {'fields': ['begin', 'end']}),
        ('Additional Information', {'fields': ['action_description', 'action_notes']}),
        (None, {'fields': ['notify_action']}),
    ]

    inlines = [TicketHistoryInline]

    readonly_fields = ['notify_action']

    search_fields = ['services', 'sub_service', 'category_status']
    list_filter = ('category_status',)
    ordering = ['end']

    actions = [notify_users]

    form = TicketForm

    def save_formset(self, request, form, formset, change):

        status_category = formset.cleaned_data[-1]['service_status']
        status_category_id = StatusCategory.objects.get(status_category_tag=status_category)
        form.instance.category_status_id = status_category_id.pk
        form.instance.save()
        formset.save()

    # def save_formset(self, request, form, formset, change):
    #
    #     change_detected = False
    #
    #     # Detect changes in the main form
    #     if form.changed_data:
    #         change_detected = True
    #
    #     # Detect changes in the child forms (inline forms/Service Histories)
    #     my_list = []
    #     for _form in formset:
    #         my_list.append(_form.cleaned_data['category_status'].status)
    #         if _form.has_changed():
    #             change_detected = True
    #
    #     good_to_save = True
    #
    #     # Update the Service Status with the last value specified in the Service Status List
    #     if change_detected:
    #
    #         # It checks for multiple 'Completed' status on the Service Status List
    #         # print(_form.cleaned_data['service_status'])
    #         # for result in _form.cleaned_data:
    #         #     print(result)
    #         # my_list = [_form.cleaned_data[result].status for result in _form.cleaned_data if result == 'service_status']
    #
    #         # if [item for item in set(my_list) if my_list.count(item) > 1].count('Completed'):
    #         #     print("Error")
    #         #     good_to_save = False
    #
    #         # It checks for the proper specification of a 'Completed' status. It must be at the last status object
    #         if good_to_save and formset.cleaned_data:
    #
    #             # It gets the latest service's status specified on the Service Status List
    #             category_status = formset.cleaned_data[-1]['category_status']
    #             # It retrieves the service status' id given its value
    #             category_status_id = StatusCategory.objects.get(status=category_status)
    #
    #             # Check for errors in the Service Status List
    #             if category_status.status != 'Completed' and \
    #                     any('Completed' in result['category_status'].status for result in formset.cleaned_data):
    #                 print("Error")
    #                 good_to_save = False
    #             else:
    #                 print("Good to save")
    #
    #                 # It modifies the ticket's status given the last service status history specified
    #                 # obj.instance.service_status_id = service_status_id.pk
    #                 form.instance.category_status = category_status_id.pk
    #                 # obj.save()
    #                 form.instance.save()
    #
    #         if good_to_save:
    #             # super().save_related(request, obj, forms, change)
    #             formset.save()
    #
    #             # It sends the Business Service's ID to notify all the users subscribed
    #             # self.notify_user(obj.cleaned_data['business_service'].pk)
    #             self.notify_user(form.cleaned_data['sub_service'].pk)
    #         else:
    #             formset.save(commit=False)
    #
    #     # # It calls the saving function but specifying that no changes has been made
    #     # print(change)
    #     # # super().save_related(request, obj, forms, change)
    #     formset.save(commit=False)


@admin.register(Subscriber)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']
    ordering = ['name']