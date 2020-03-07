from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _


class Service(models.Model):
    service_name = models.CharField(unique=True, max_length=100)  # Field name made lowercase.
    service_description = models.CharField(max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['service_name']

    def __str__(self):
        return self.service_name


class View(models.Model):
    view_name = models.CharField(unique=True, max_length=100, verbose_name='Regions')  # Field name made lowercase.
    view_description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    services = models.ManyToManyField(Service)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['view_name']

    def __str__(self):
        return self.view_name


class SubService(models.Model):
    sub_service_name = models.CharField(unique=True, max_length=100, verbose_name='Sub-Service')  # Field name made lowercase.
    sub_service_description = models.CharField(max_length=100, blank=True, null=True)  # Field name made lowercase.
    services = models.ManyToManyField(Service, through='SubServiceServices', verbose_name='Service')

    class Meta:
        verbose_name = _("Sub-Service")
        verbose_name_plural = _("Sub-Services")
        ordering = ['sub_service_name']

    def __str__(self):
        return self.sub_service_name


class Priority(models.Model):
    priority_tag = models.CharField(unique=True, max_length=25)  # Field name made lowercase.
    priority_color = models.CharField(unique=True, max_length=7)  # Field name made lowercase.

    class Meta:
        verbose_name = _("Priority Tag")
        verbose_name_plural = _("Priority Tags")
        ordering = ['priority_tag']

    def __str__(self):
        return self.priority_tag


class SubServiceServices(models.Model):
    service = models.ForeignKey(Service, models.CASCADE)
    subservice = models.ForeignKey(SubService, models.CASCADE, verbose_name='Sub-Service')
    priority = models.ForeignKey(Priority, models.DO_NOTHING)

    class Meta:
        unique_together = ('service', 'subservice')

        verbose_name = _("Topology")
        verbose_name_plural = _("Topology")

    def __str__(self):
        return "about {0} in {1}".format(self.subservice, self.service)


class StatusCategory(models.Model):
    status_category_tag = models.CharField(unique=True, max_length=45)  # Field name made lowercase.
    status_category_color = models.CharField(unique=True, max_length=7)  # Field name made lowercase.

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
    sub_service = models.ForeignKey(SubService, models.DO_NOTHING, verbose_name='Sub-Service')  # Field name made lowercase.
    category_status = models.ForeignKey(StatusCategory, models.DO_NOTHING, default=3, verbose_name='Status')  # Field name made lowercase.
    begin = models.DateTimeField()  # Field name made lowercase.
    end = models.DateTimeField()  # Field name made lowercase.
    action_description = models.TextField()  # Field name made lowercase.
    action_notes = models.TextField(blank=True, null=True)  # Field name made lowercase.

    notify_action = models.BooleanField(
        default=NO,
        choices=YES_NO_CHOICES,
        verbose_name='Ticket notified')

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

    def __str__(self):
        # return "{0} in {1}".format(self.service_category, self.business_service)
        return self.ticket_id


class TicketLog(models.Model):
    service_history = models.ForeignKey(Ticket, models.DO_NOTHING)
    service_status = models.ForeignKey(StatusCategory, models.DO_NOTHING)
    action_date = models.DateTimeField()
    action_notes = models.TextField(blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    def __str__(self):
        return "{0} in {1}".format(self.service_history.sub_service, self.service_history.ticket_id)


class Subscriber(models.Model):
    name = models.CharField(max_length=45)      # Field name made lowercase.
    email = models.CharField(max_length=45)     # Field name made lowercase.
    services = models.ManyToManyField(Service, verbose_name='Services')
    subservices = models.ManyToManyField(SubService, verbose_name='Sub - Services')

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.name
