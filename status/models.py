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

    name = models.CharField(unique=True, max_length=100, verbose_name='Service')
    service_description = models.TextField(blank=True, null=True, verbose_name='Description')

    # service_description = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['name']

    def __str__(self):
        return self.name


class ClientDomain(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Client Domain')
    description = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service)

    class Meta:
        verbose_name = _("Client Domain")
        verbose_name_plural = _("Client Domains")
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Region')
    description = models.TextField(blank=True, null=True)
    client_domains = models.ManyToManyField(ClientDomain)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['name']

    def __str__(self):
        return self.name


class SubService(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Sub-Service')
    # sub_service_description = HTMLField()
    description = models.TextField(blank=True, null=True)
    # services = models.ManyToManyField(Service, through='SubServiceServices', verbose_name='Service')

    class Meta:
        verbose_name = _("Sub-Service")
        verbose_name_plural = _("Sub-Services")
        ordering = ['name']

    def __str__(self):
        return self.name


class Priority(models.Model):
    tag = models.CharField(unique=True, max_length=25)
    color = models.CharField(unique=True, max_length=7)
    color_hex = ColorField(unique=True, default='#000000')

    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _("Priorities")
        ordering = ['tag']

    def __str__(self):
        return self.tag


class Topology(models.Model):
    service = models.ForeignKey(Service, models.CASCADE, verbose_name='Service')
    subservices = models.ManyToManyField(SubService, verbose_name='Sub - Service', blank=True)
    priority = models.ForeignKey(Priority, models.DO_NOTHING)

    class Meta:
        verbose_name = _("Topology")
        verbose_name_plural = _("Topologies")

    # def __str__(self):
    #     return "about {0} in {1}".format(self.subservice, self.service)


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


class Status(models.Model):
    tag = models.CharField(unique=True, max_length=45, verbose_name='Status')
    color_name = models.CharField(unique=True, max_length=7)
    color_hex = ColorField(default='#000000')
    class_design = models.CharField(unique=True, max_length=50)

    class Meta:
        verbose_name = _("Status Category")
        verbose_name_plural = _("Status Categories")

    def __str__(self):
        return self.tag


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
    status = models.ForeignKey(Status, models.DO_NOTHING, null=True, default=3, verbose_name='Status')
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
    status = models.ForeignKey(Status, models.DO_NOTHING)
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
