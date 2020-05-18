# -*- coding: utf-8 -*-
"""
This module will define all the models and their
relationships to build up the Application logic.
"""
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.db import models
from django.utils.html import format_html
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    """
    Class to specify the Services model.
        - A Service name and description define its structure.
        - The Service name will be mandatory, but no the description field.
        - The name field could have a maximum of 100 characters.
        - The description field will store an HTML enriched text content.
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='Service')
    service_description = RichTextField(blank=True, null=True, verbose_name='Description')

    def description(self):
        """
        Method to truncate and render HTML content.
            - This action will allow visualizing a short
            description during the object listing process.
            - The HTML render process will help to visualize
            HTML rendered content on the listed object's stories.
        :return: No return
        """
        if self.service_description is not None:
            return format_html(Truncator(self.service_description).chars(250))
        return self.service_description

    description.allow_tags = True

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['name']

    def __str__(self):
        return self.name


class ClientDomain(models.Model):
    """
    Class to specify the Client Domain model.
        - A Client Domain name, a description, and a relationship
        to the Service module define its structure.
        - The Client Domain name will be mandatory, but no the description field.
        - The name field could have a maximum of 100 characters.
        - The description field will store an HTML enriched text content.
        - The relationship with Services will help to set a
        client domain to many services and vice versa.
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='Client Domain')
    domain_description = RichTextField(blank=True, null=True, verbose_name='Description')
    services = models.ManyToManyField(Service)

    def description(self):
        """
        Method to truncate and render HTML content.
            - This action will allow visualizing a short
            description during the object listing process.
            - The HTML render process will help to visualize
            HTML rendered content on the listed object's stories.
        :return: No return
        """
        if self.domain_description is not None:
            return format_html(self.domain_description)
        return self.domain_description
    description.allow_tags = True

    class Meta:
        verbose_name = _("Client Domain")
        verbose_name_plural = _("Client Domains")
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Region')
    region_description = RichTextField(blank=True, null=True, verbose_name='Description')
    client_domains = models.ManyToManyField(ClientDomain)

    def description(self):
        if self.region_description is not None:
            return format_html(self.region_description)
        return self.region_description
    description.allow_tags = True

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['name']

    def __str__(self):
        return self.name


class SubService(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Sub-Service')
    subservice_description = RichTextField(blank=True, null=True, verbose_name='Description')

    def description(self):
        if self.subservice_description is not None:
            return format_html(self.subservice_description)
        return self.subservice_description
    description.allow_tags = True

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
    subservices = models.ManyToManyField(SubService, verbose_name='Sub - Service')
    priority = models.ForeignKey(Priority, models.DO_NOTHING)

    class Meta:
        verbose_name = _("Topology")
        verbose_name_plural = _("Topologies")

    def subservices_list(self):
        return format_html("<br>".join([subservice.name for subservice in self.subservices.all()]))
    subservices_list.allow_tags = True

    def __str__(self):
        return "Topology {0}: about Service {1}, {2} " \
               "priority".format(self.pk, self.service, self.priority)


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

    # This action (models.SET_NULL) will allow keeping tickets regardless of
    # the deletion of the sub-service where they belong.
    sub_service = models.ForeignKey(SubService, models.SET_NULL,
                                    null=True, verbose_name='Sub-Service')
    status = models.ForeignKey(Status, models.DO_NOTHING,
                               null=True, default=3, verbose_name='Status')
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
    domain_description = RichTextField(blank=True, null=True, verbose_name='Description')

    def description(self):
        if self.domain_description is not None:
            return format_html(self.domain_description)
        return self.domain_description
    description.allow_tags = True

    class Meta:
        verbose_name = _("Email Domain")
        verbose_name_plural = _("Email Domains")

    def __str__(self):
        return self.domain
