from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.db import models
from django.utils.text import Truncator

# Create your models here.
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):

    @property
    def description(self):
        return Truncator(self.service_description).chars(55)

    service_name = models.CharField(unique=True, max_length=100, verbose_name='Service')
    service_description = models.TextField(blank=True, null=True)
    # service_description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['service_name']

    def __str__(self):
        return self.service_name


class ClientDomain(models.Model):
    client_domain_name = models.CharField(unique=True, max_length=100, verbose_name='Client Domain')
    client_domain_description = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service)

    class Meta:
        verbose_name = _("Client Domain")
        verbose_name_plural = _("Client Domains")
        ordering = ['client_domain_name']

    def __str__(self):
        return self.client_domain_name


class Region(models.Model):
    region_name = models.CharField(unique=True, max_length=100, verbose_name='Region')
    region_description = models.TextField(blank=True, null=True)
    # services = models.ManyToManyField(Service)
    client_domains = models.ManyToManyField(ClientDomain)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['region_name']

    def __str__(self):
        return self.region_name


class SubService(models.Model):
    sub_service_name = models.CharField(unique=True, max_length=100, verbose_name='Sub-Service')
    # sub_service_description = HTMLField()
    sub_service_description = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service, through='SubServiceServices', verbose_name='Service')

    class Meta:
        verbose_name = _("Sub-Service")
        verbose_name_plural = _("Sub-Services")
        ordering = ['sub_service_name']

    def __str__(self):
        return self.sub_service_name


class Priority(models.Model):
    priority_tag = models.CharField(unique=True, max_length=25)
    priority_color = models.CharField(unique=True, max_length=7)
    priority_color_hex = ColorField(unique=True, default='#000000')

    class Meta:
        verbose_name = _("Priority Tag")
        verbose_name_plural = _("Priority Tags")
        ordering = ['priority_tag']

    def __str__(self):
        return self.priority_tag


class SubServiceServices(models.Model):
    service = models.ForeignKey(Service, models.CASCADE, verbose_name='Service')
    subservice = models.ForeignKey(SubService, models.CASCADE, verbose_name='Sub-Service')
    priority = models.ForeignKey(Priority, models.DO_NOTHING)

    class Meta:
        unique_together = ('service', 'subservice')

        verbose_name = _("Topology")
        verbose_name_plural = _("Topologies")

    def __str__(self):
        return "about {0} in {1}".format(self.subservice, self.service)


class StatusCategory(models.Model):
    status_category_tag = models.CharField(unique=True, max_length=45, verbose_name='Status')
    status_category_color = models.CharField(unique=True, max_length=7)
    status_category_color_hex = ColorField(default='#000000')
    status_class_design = models.CharField(unique=True, max_length=50)

    class Meta:
        verbose_name = _("Status Category")
        verbose_name_plural = _("Status Categories")

    def __str__(self):
        return self.status_category_tag


class Ticket(models.Model):
    NO = False
    YES = True
    YES_NO_CHOICES = (
        (NO, 'No'),
        (YES, 'Yes')
    )

    ticket_id = models.CharField(unique=True, max_length=10)

    # This action will allow keeping tickets regardless of the deletion of the sub-service where they belong.
    # sub_service = models.ForeignKey(SubService, models.SET_NULL, null=True, verbose_name='Sub-Service')

    sub_service = models.ForeignKey(SubService, models.CASCADE, null=True, verbose_name='Sub-Service')
    status = models.ForeignKey(StatusCategory, models.DO_NOTHING, null=True, default=3, verbose_name='Status')
    begin = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    action_description = RichTextField()
    action_notes = RichTextField(blank=True, null=True)

    notify_action = models.BooleanField(
        default=YES,
        choices=YES_NO_CHOICES,
        verbose_name='Ticket notified')

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        # return "{0} in {1}".format(self.service_category, self.business_service)
        return self.ticket_id


class TicketLog(models.Model):
    ticket = models.ForeignKey(Ticket, models.CASCADE)
    event_status = models.ForeignKey(StatusCategory, models.DO_NOTHING)
    action_date = models.DateTimeField()
    # action_notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    action_notes = RichTextField(blank=True, null=True, verbose_name='Notes')

    def __str__(self):
        return "{0} in {1}".format(self.ticket.sub_service, self.ticket.ticket_id)


class Subscriber(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    token = models.CharField(max_length=128, null=True, blank=True)
    services = models.ManyToManyField(Service, verbose_name='Service', blank=True)
    subservices = models.ManyToManyField(SubService, verbose_name='Sub - Service', blank=True)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.name


class EmailDomain(models.Model):
    domain = models.CharField(unique=True, max_length=100, verbose_name='Domain Name')
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Email Domain")
        verbose_name_plural = _("Email Domains")

    def __str__(self):
        return self.domain
