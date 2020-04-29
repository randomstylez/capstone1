from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from status.forms import *
from .models import ClientDomain
from .models import EmailDomain
# Register your models here.
from .models import Priority
from .models import Region
from .models import Status
from .models import SubService
from .models import SubServiceServices
from .models import TicketLog


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ['name', 'description', 'services__name']
    list_filter = (('client_domains__services__subservice__ticket__status__tag',
                    DropdownFilter),
                   ('client_domains__name',
                    DropdownFilter),
                   ('client_domains__services__name',
                    DropdownFilter),
                   ('client_domains__services__subservice__name',
                    DropdownFilter))
    ordering = ['name']


@admin.register(ClientDomain)
class ClientDomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ['name', 'description']
    list_filter = (('services__subservice__ticket__status__tag',
                    DropdownFilter),
                   ('region__name',
                    DropdownFilter),
                   ('services__name',
                    DropdownFilter),
                   ('services__subservice__name',
                    DropdownFilter))
    ordering = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ['name', 'service_description', 'subservice__name', 'clientdomain__region__name']
    list_filter = (('subservice__ticket__status__tag',
                    DropdownFilter),
                   ('clientdomain__region__name',
                    DropdownFilter),
                   ('clientdomain__name',
                    DropdownFilter),
                   ('subservice__name',
                    DropdownFilter))
    ordering = ['name']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ['name', 'description', 'services__name',
                     'services__clientdomain__region__name']
    list_filter = (('ticket__status__tag',
                    DropdownFilter),
                   ('services__clientdomain__region__name',
                    DropdownFilter),
                   ('services__clientdomain__name',
                    DropdownFilter),
                   ('services',
                    RelatedDropdownFilter))
    ordering = ['name']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('tag', 'color_name', 'color_hex', 'class_design')
    ordering = ['tag']


def notify_users(modeladmin, request, queryset):
    queryset.update(notify_action=True)


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
    list_display = ('ticket_id', 'sub_service', 'status', 'begin', 'end', 'notify_action',)

    fieldsets = [
        ('Sub-Service on process', {'fields': ['ticket_id', 'sub_service', 'status']}),
        ('Date information', {'fields': ['begin', 'end']}),
        ('Additional Information', {'fields': ['action_description', 'action_notes']}),
        (None, {'fields': ['notify_action']}),
    ]

    inlines = [TicketHistoryInline]

    # readonly_fields = ['notify_action']

    search_fields = ['ticket_id', 'sub_service__name', 'status__tag']
    list_filter = (('status',
                    RelatedDropdownFilter),
                   ('sub_service__services__clientdomain__region__name',
                    DropdownFilter),
                   ('sub_service__services__clientdomain__name',
                    DropdownFilter),
                   ('sub_service__services__name',
                    DropdownFilter),
                   ('sub_service',
                    RelatedDropdownFilter))
    ordering = ['end']

    actions = [notify_users]

    form = TicketForm

    def save_formset(self, request, form, formset, change):
        # If it is received data related to the ticket's events, the ticket
        # will update its status with the last status registered on the events
        if formset.cleaned_data:
            status = formset.cleaned_data[-1]['status']
            # If the last Ticket Log status is 'No Issues,' means that the problem has
            # updating the Ticket End Time to the value specified on the last Ticket Events
            if status.tag == 'No Issues':
                form.instance.end = formset.cleaned_data[-1]['action_date']
            status_category_id = Status.objects.get(tag=status)
            form.instance.category_status_id = status_category_id.pk
            form.instance.save()
        formset.save()


@admin.register(Subscriber)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']
    ordering = ['name']

    readonly_fields = ['token']

    form = SubscriberForm


@admin.register(SubServiceServices)
class SubServiceServicesAdmin(admin.ModelAdmin):
    list_display = ('service', 'subservice', 'priority',)
    list_filter = (('priority',
                    RelatedDropdownFilter),
                   ('subservice__ticket__status__tag',
                    DropdownFilter),
                   ('service__clientdomain__region__name',
                    DropdownFilter),
                   ('service__clientdomain__name',
                    DropdownFilter),
                   ('service',
                    RelatedDropdownFilter),
                   ('subservice',
                    RelatedDropdownFilter))
    search_fields = ['service', 'subservice', 'priority']
    ordering = ['service']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_tag', 'priority_color', 'priority_color_hex')
    ordering = ['priority_tag']


@admin.register(EmailDomain)
class EmailDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'description')
    search_fields = ['domain', 'description']
    ordering = ['domain']
