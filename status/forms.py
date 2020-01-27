import copy

from .models import ServicesHistory
from .models import ServicesStatus
from django import forms
from django.core.exceptions import ValidationError


class ServicesHistoryForm(forms.ModelForm):
    class Meta:
        model = ServicesHistory
        # exclude = ['name']
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        ticket_id = cleaned_data.get("ticket_id")

        # if ticket_id and ticket_id != "ITA0001513":
        #         #     msg = "There is some errors with the Ticket code."
        #         #     self.add_error('ticket_id', msg)

        print(cleaned_data)
        print("I am cleaning")
        # Validation goes here :)


class ServiceHistoryStatusInlineFormset(forms.models.BaseInlineFormSet):

    def clean(self):

        status_list = []
        form_list = []
        change_detected = False
        service_status = None

        for form in self.forms:

            status_list.append(form.cleaned_data['service_status'].status)
            service_status = form.cleaned_data['service_status']
            if form.has_changed():
                change_detected = True

            form_list.append(form)

            # print(form.clean())

        print("I am cleaning - 2")

        if change_detected:

            my_raises = False

            for form in form_list:
                if [item for item in set(status_list) if status_list.count(item) > 1].count('Completed'):
                    if form.cleaned_data['service_status'].status == 'Completed':
                        form.add_error("service_status", "You can not have {} status multiple times.".format(
                            form.cleaned_data["service_status"]))
                        my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

            for form in form_list:
                if service_status.status != 'Completed' and 'Completed' in status_list and \
                        form.cleaned_data['service_status'].status == 'Completed':
                    form.add_error("service_status", "{} is an status available only as a final stage.".format(
                        form.cleaned_data["service_status"]))
                    my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")
