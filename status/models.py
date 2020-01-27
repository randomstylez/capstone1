from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _


class BusinessService(models.Model):
    business_service_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    business_service_name = models.CharField(unique=True, max_length=100)  # Field name made lowercase.
    business_service_description = models.CharField(max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = _("Business Service")
        verbose_name_plural = _("Business Services")

    def __str__(self):
        return self.business_service_name


class ServicesDescriptions(models.Model):
    service_description_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    business_service = models.ForeignKey(BusinessService, models.DO_NOTHING, verbose_name='Business Service')  # Field name made lowercase.
    description = models.CharField(max_length=45)  # Field name made lowercase.

    class Meta:
        unique_together = (('business_service', 'description'),)
        verbose_name = _("Services Description")
        verbose_name_plural = _("Services Descriptions")

    def __str__(self):
        return self.description


class ServicesCategory(models.Model):
    service_category_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    tag = models.CharField(unique=True, max_length=45)  # Field name made lowercase.
    color = models.CharField(unique=True, max_length=7)  # Field name made lowercase.

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Services Category")

    def __str__(self):
        return self.tag


class ServicesStatus(models.Model):
    service_status_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    status = models.CharField(unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        verbose_name = _("Service Status")
        verbose_name_plural = _("Services Status")

    def __str__(self):
        return self.status


class ServicesHistory(models.Model):
    NO = False
    YES = True
    YES_NO_CHOICES = (
        (NO, 'No'),
        (YES, 'Yes')
    )

    service_history_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    ticket_id = models.CharField(unique=True, max_length=10)
    business_service = models.ForeignKey(BusinessService, models.DO_NOTHING, verbose_name='Business Service')  # Field name made lowercase.
    service_category = models.ForeignKey(ServicesCategory, models.DO_NOTHING, verbose_name='Service Category')  # Field name made lowercase.
    service_status = models.ForeignKey(ServicesStatus, models.DO_NOTHING, default=1, verbose_name='Service Status')  # Field name made lowercase.
    begin = models.DateTimeField()  # Field name made lowercase.
    end = models.DateTimeField()  # Field name made lowercase.
    action_description = models.TextField()  # Field name made lowercase.
    action_notes = models.TextField(blank=True, null=True)  # Field name made lowercase.
    # closing_notes = models.TextField(blank=True, null=True)  # Field name made lowercase.
    # notify_action = models.BooleanField(default=False, verbose_name='Ticket notified')  # Field name made lowercase.
    notify_action = models.BooleanField(
        default=NO,
        choices=YES_NO_CHOICES,
        verbose_name='Ticket notified')

    class Meta:
        verbose_name = _("Service History")
        verbose_name_plural = _("Services History")

    def __str__(self):
        # return "{0} in {1}".format(self.service_category, self.business_service)
        return self.ticket_id


class Subscribers(models.Model):
    subscribers_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)  # Field name made lowercase.
    email = models.CharField(max_length=45)  # Field name made lowercase.
    business_service = models.ManyToManyField(BusinessService)

    class Meta:
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return self.name


class SubscribersBusinessService(models.Model):
    subscription_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    subscribers = models.ForeignKey(Subscribers, models.DO_NOTHING)  # Field name made lowercase.
    business_service_key = models.ForeignKey(BusinessService, models.DO_NOTHING)  # Field name made lowercase.


class ServiceHistoryStatus(models.Model):
    service_history_status_id = models.AutoField(primary_key=True)
    service_history = models.ForeignKey(ServicesHistory, models.DO_NOTHING)
    service_status = models.ForeignKey(ServicesStatus, models.DO_NOTHING)
    action_date = models.DateTimeField()
    action_notes = models.TextField(blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    def __str__(self):
        return "{0} in {1}".format(self.service_history.business_service, self.service_history.ticket_id)
