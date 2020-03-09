from django.contrib import admin

# Register your models here.
from .models import View
from .models import Service
from .models import SubService
from .models import StatusCategory
from .models import Ticket
from .models import TicketLog
from .models import Subscriber
from .models import SubServiceServices
from .models import Priority

from status.forms import *


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('view_name', 'view_description')
    search_fields = ['view_name', 'view_description', 'services__service_name']
    list_filter = ('services__subservice__ticket__category_status__status_category_tag',
                   'services__service_name', 'services__subservice__sub_service_name' )
    ordering = ['view_name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_description')
    search_fields = ['service_name', 'service_description', 'subservice__sub_service_name', 'view__view_name']
    list_filter = ('subservice__ticket__category_status__status_category_tag', 'view__view_name',
                   'subservice__sub_service_name', )
    ordering = ['service_name']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('sub_service_name', 'sub_service_description')
    search_fields = ['services__service_name', 'sub_service_description', 'sub_service_name']
    list_filter = ('ticket__category_status__status_category_tag', 'services__view__view_name', 'services',)
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

    search_fields = ['ticket_id', 'sub_service__sub_service_name', 'category_status__status_category_tag']
    list_filter = ('category_status', 'sub_service__services__view__view_name', 'sub_service__services__service_name', 'sub_service')
    ordering = ['end']

    actions = [notify_users]

    form = TicketForm

    def save_formset(self, request, form, formset, change):

        status_category = formset.cleaned_data[-1]['service_status']
        status_category_id = StatusCategory.objects.get(status_category_tag=status_category)
        form.instance.category_status_id = status_category_id.pk
        form.instance.save()
        formset.save()


@admin.register(Subscriber)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']
    ordering = ['name']


@admin.register(SubServiceServices)
class SubServiceServicesAdmin(admin.ModelAdmin):
    list_display = ('service', 'subservice', 'priority')
    list_filter = ('subservice__ticket__category_status__status_category_tag', 'priority',
                   'service__view__view_name', 'service', 'subservice')
    search_fields = ['service', 'subservice', 'priority']
    ordering = ['service']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_tag', 'priority_color')
    ordering = ['priority_tag']
