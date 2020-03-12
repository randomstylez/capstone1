import copy
import secrets

from .models import Ticket
from .models import Service
from .models import Subscriber
from .models import DomainList
from status.mail_sender import MailSender

from django import forms
from django.core.exceptions import ValidationError
from validate_email import validate_email


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

    @staticmethod
    def notify_user(sub_service_id):
        # It gets all the users who belong to that Sub Service

        # It gets the list of services that has that Sub Service
        services = Service.objects.filter(subservice=sub_service_id)

        # It gets the list of Key ID ot those services
        users_mail = Subscriber.objects.filter(services__in=services)

        # Remove duplicates
        users_mail = list(dict.fromkeys(users_mail))

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

    def clean(self):
        cleaned_data = super().clean()

        begin = cleaned_data['begin'].strftime('%Y-%m-%d %H:%M:%S')
        end = cleaned_data['end'].strftime('%Y-%m-%d %H:%M:%S')

        if begin > end:
            self.add_error("begin", "The Begin date {} should follow a chronological order.".format(
                self.cleaned_data["begin"]))
            self.add_error("end", "The End date {} should follow a chronological order.".format(
                self.cleaned_data["end"]))
            raise ValidationError("There are some errors on the Ticket's dates.")

        self.notify_user(cleaned_data['sub_service'].pk)


class TicketHistoryInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):

        status_list = []
        form_list = []
        change_detected = False
        service_status = None

        main_begin = self.data['begin_0'] + ' ' + self.data['begin_1']

        for form in self.forms:

            service_status = form.cleaned_data.get('service_status')
            status_list.append(service_status.status_category_tag)

            if form.has_changed():
                change_detected = True

            form_list.append(form)

        if change_detected:

            my_raises = False

            for form in form_list:
                begin = form.cleaned_data['action_date'].strftime('%Y-%m-%d %H:%M:%S')
                if begin < main_begin:
                    form.add_error("action_date", "You can not have an action date "
                                                  "lower than the start day of the ticket {}.".format(
                        form.cleaned_data["action_date"]))
                    my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

            if not my_raises:
                for form in form_list:
                    if [item for item in set(status_list) if status_list.count(item) > 1].count('Completed'):
                        if form.cleaned_data['service_status'].status_category_tag == 'Completed':
                            form.add_error("service_status", "You can not have {} status multiple times.".format(
                                form.cleaned_data["service_status"]))
                            my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

            for form in form_list:
                if service_status.status_category_tag != 'Completed' and 'Completed' in status_list \
                        and form.cleaned_data['service_status'].status_category_tag == 'Completed':
                    form.add_error("service_status", "{} is an status available only as a final stage.".format(
                        form.cleaned_data["service_status"]))
                    my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data['email']

        # Verify email authenticity
        is_valid = validate_email(email)

        # # Check if the host has SMTP Server and the email really exists:
        # pip install pyDNS
        # is_valid = validate_email(email, verify=True)

        if not is_valid:
            self.add_error("email", "{} is an invalid email information.".format(
                self.cleaned_data["email"]))
            raise ValidationError("There are some errors on the Subscriber's information.")

        # Verify that the subscriber email belong to our domain list
        domain = email.split('@')[1]

        # It gets the list of services that has that Sub Service
        domain_exist = DomainList.objects.filter(domain_name=domain).count()

        if domain_exist == 0:
            self.add_error("email", "{} does not belong to our Users' domain.".format(
                self.cleaned_data["email"]))
            raise ValidationError("There are some errors on the Subscriber's information.")

        # Insert user and insert token
        if not self.instance.pk:
            # Create token
            token = secrets.token_hex(64)

            # Update User's token
            self.cleaned_data["token"] = token
