import secrets

from django import forms
from django.core.exceptions import ValidationError
from validate_email import validate_email

from status.mail_sender import MailSender
from .models import EmailDomain
from .models import Region
from .models import Service
from .models import SubService
from .models import SubServiceServices
from .models import Subscriber
from .models import Ticket


class TicketForm(forms.ModelForm):
    NO = False
    YES = True
    YES_NO_CHOICES = (
        (NO, 'No'),
        (YES, 'Yes')
    )

    cleaned_data = None

    class Meta:
        model = Ticket
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['notify_action'] = forms.ChoiceField(choices=self.YES_NO_CHOICES)

    def notify_user(self, sub_service_id):
        # It gets all the users who belong to that Sub Service

        # It gets the list of services that has that Sub Service
        services = Service.objects.filter(subservice=sub_service_id)
        subservices = SubService.objects.filter(id=sub_service_id)

        # Information to use in the email Body
        # region = Region.objects.filter(services__subservice__in=subservices)
        region = Region.objects.filter(client_domains__services__subservice__in=subservices)
        topology = SubServiceServices.objects.filter(subservice__in=subservices)

        changed_data = self.changed_data
        # print(self.cleaned_data)

        users_mail1 = []
        users_mail2 = []

        if services.count() != 0:
            # It gets the list of Key ID ot those services
            users_mail1 = Subscriber.objects.filter(services__in=services)

            # Remove duplicates
            users_mail1 = list(dict.fromkeys(users_mail1))

        if subservices.count() != 0:
            users_mail2 = Subscriber.objects.filter(subservices__in=subservices)

            # Remove duplicates
            users_mail2 = list(dict.fromkeys(users_mail2))

        users = list(set(users_mail1) | set(users_mail2))

        data = dict()
        data['ticket_id'] = self.cleaned_data['ticket_id']
        data['region'] = 'None'
        if region.count() != 0:
            data['region'] = region[0].name
        data['priority'] = 'None'
        if topology.count() != 0:
            data['priority'] = topology[0].priority
        data['service'] = None
        if services.count() != 0:
            data['service'] = services[0].name
        data['subservice'] = 'None'
        if subservices.count() != 0:
            data['subservice'] = subservices[0].name

        for user in users:
            text = f"""\
                            Changes on the ticket {data['ticket_id']}:
                            Region: {data['region']}
                            Priority: {data['priority']}
                            Service: {data['service']}
                            Sub-Service: {data['subservice']}
                            """

            html = f"""\
                            <html>
                              <body>
                                <p>Changes on the ticket 
                                    <span style="font-weight: bold;">{data['ticket_id']}</span>:
                                    <br>
                                    <ul>
                                        <li>
                                            <span style="font-weight: bold;">Region:</span> {data['region']}
                                        </li>
                                        <li>
                                            <span style="font-weight: bold;">Priority:</span> {data['priority']}
                                        </li>
                                        <li>
                                            <span style="font-weight: bold;">Service:</span> {data['service']}
                                        </li>
                                        <li>
                                            <span style="font-weight: bold;">Sub-Service:</span> {data['subservice']}
                                        </li>
                                    </ul>
                                </p>
                              </body>
                            </html>
                            """

            subject = "Changes detected!"

            mail_sender = MailSender(html, subject, text, user.email)
            mail_sender.send_mail()

    def clean(self):
        self.cleaned_data = super().clean()

        begin = self.cleaned_data['begin'].strftime('%Y-%m-%d %H:%M:%S')

        if self.cleaned_data['end']:
            end = self.cleaned_data['end'].strftime('%Y-%m-%d %H:%M:%S')

            if begin > end:
                self.add_error("begin", "The Begin date {} should follow a chronological order.".format(
                    self.cleaned_data["begin"]))
                self.add_error("end", "The End date {} should follow a chronological order.".format(
                    self.cleaned_data["end"]))
                raise ValidationError("There are some errors on the Ticket's dates.")

        if self.changed_data:
            if self.changed_data == ['notify_action'] and not self.instance.notify_action and \
                    self.cleaned_data['notify_action'] == 'True':
                self.instance.notify_action = True
                self.notify_user(self.cleaned_data['sub_service'].pk)
            elif self.changed_data != ['notify_action'] and \
                    (self.cleaned_data['notify_action'] is True or self.cleaned_data['notify_action'] == 'True'):
                self.instance.notify_action = True
                try:
                    self.notify_user(self.cleaned_data['sub_service'].pk)
                except Exception as e:
                    print(e)  # we should log this as an error


class TicketHistoryInlineFormset(forms.models.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(TicketHistoryInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):

        status_list = []
        form_list = []
        change_detected = False
        status = None
        main_begin = None

        if self.data['begin_0'] and self.data['begin_1']:
            main_begin = self.data['begin_0'] + ' ' + self.data['begin_1']

        for form in self.forms:
            if form.cleaned_data != {}:
                if main_begin is None:
                    main_begin = form.cleaned_data.get('begin').strftime('%Y-%m-%d %H:%M:%S')

                status = form.cleaned_data.get('status')
                if status is not None:
                    status_list.append(status.tag)
                else:
                    break

                if form.has_changed():
                    change_detected = True

                form_list.append(form)

        if change_detected:

            my_raises = False

            for form in form_list:
                begin = form.cleaned_data['action_date'].strftime('%Y-%m-%d %H:%M:%S')
                if begin < main_begin:
                    form.add_error("action_date", "You can not have an action date "
                                                  "lower than the start day of the ticket {}.".
                                   format(form.cleaned_data["action_date"]))
                    my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

            if not my_raises:
                for form in form_list:
                    if [item for item in set(status_list) if status_list.count(item) > 1].count('No Issues'):
                        if form.cleaned_data['status'].tag == 'No Issues':
                            form.add_error("status", "You can not have {} status multiple times.".format(
                                form.cleaned_data["status"]))
                            my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

            for form in form_list:
                if status.tag != 'No Issues' and 'No Issues' in status_list \
                        and form.cleaned_data['status'].tag == 'No Issues':
                    form.add_error("status", "{} is an status available only as a final stage.".format(
                        form.cleaned_data["status"]))
                    my_raises = True

            if my_raises:
                raise ValidationError("There are some errors on the Service's Status.")

        # return self.cleaned_data


class EmailActions:

    @staticmethod
    def check_email_domain(domain):

        # It verifies the existence or not of that email domain
        domain_exist = EmailDomain.objects.filter(domain=domain).count()

        if domain_exist == 0:
            return False

        return True

    @staticmethod
    def notify_subscription_to_user_email(email, services, subservices):

        service_list = ''
        service_list_html = ''

        subservice_list = ''
        subservice_list_html = ''

        if len(services):
            service_list += '<br>'
            service_list_html += '<ul>'
            for service in services:
                service_list += f"""{service}<br>"""
                service_list_html += f"""<li>{service}</li>"""
            service_list += '<br>'
            service_list_html += '</ul>'
        else:
            service_list += '<br>None selected<br>'
            service_list_html += '<ul><li>None selected</li></ul>'

        if len(subservices):
            subservice_list += '<br>'
            subservice_list_html += '<ul>'
            for subservice in subservices:
                subservice_list += f"""{subservice}<br>"""
                subservice_list_html += f"""<li>{subservice}</li>"""
            subservice_list += '<br'
            subservice_list_html += '</ul>'
        else:
            subservice_list += '<br>None selected<br>'
            subservice_list_html += '<ul><li>None selected</li></ul>'

        # Email content
        text = f"""\
            You have subscribed to receive notifications from the following services:
            <br>
            {service_list}
            You have subscribed to receive notifications from the following sub-services:
            {subservice_list}"""

        html = f"""\
        <html>
            <body>
                <p>You have subscribed to receive notifications from the following Service(s)</p>
                {service_list_html}
                <p>You have subscribed to receive notifications from the following Sub-service(s)</p>
                {subservice_list_html}
            </body>
        </html>"""

        subject = "Subscription requested!"

        mail_sender = MailSender(html, subject, text, email)
        mail_sender.send_mail()

    @staticmethod
    def send_subscription_notification(email, token):

        hostname = 'https://status2.amlight.net'
        view_path = '/subscriber'

        link = hostname + view_path + '/' + email + '/' + token

        # Email content
        text = f"""\
                                Link to modify your subscription:
                                {link}
                                """

        html = f"""\
                                <html>
                                  <body>
                                    <p>Link to modify your subscription<br>
                                    </p>
                                    <a href="{link}">Modify your subscription</a>
                                  </body>
                                </html>
                                """

        subject = "Modification requested on Subscription!"

        mail_sender = MailSender(html, subject, text, email)
        mail_sender.send_mail()


class SubscriberDataForm(forms.ModelForm):

    services = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=Service.objects.all(), required=False)
    subservices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 queryset=SubService.objects.all(), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name", "class": "form-control"}),
                           max_length=40, required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
                             required=True)

    def check_mail_domain(self):
        """
        Method to check if the email provided belong to
        the list of user domains registered on the system
        """
        # Verify that the subscriber email belong to our domain list
        domain = self.cleaned_data["email"].split('@')[1]

        return EmailActions.check_email_domain(domain)

        # # It verifies the existence or not of that email domain
        # domain_exist = EmailDomainList.objects.filter(email_domain_name=domain).count()
        #
        # if domain_exist == 0:
        #     return False
        #
        # return True

    def notify_user_email(self):
        """
        Method to send a mail notification
        about the subscription requested
        """
        email = self.cleaned_data["email"]
        services = self.cleaned_data["services"]
        subservices = self.cleaned_data["subservices"]

        EmailActions.notify_subscription_to_user_email(email, services, subservices)

        # email = self.cleaned_data["email"]
        #
        # service_list = ''
        # service_list_html = ''
        #
        # subservice_list = ''
        # subservice_list_html = ''
        #
        # services = self.cleaned_data["services"]
        # subservices = self.cleaned_data["subservices"]
        #
        # if len(services):
        #     service_list += '<br>'
        #     service_list_html += '<ul>'
        #     for service in services:
        #         service_list += f"""{service}<br>"""
        #         service_list_html += f"""<li>{service}</li>"""
        #     service_list += '<br>'
        #     service_list_html += '</ul>'
        # else:
        #     service_list += '<br>None selected<br>'
        #     service_list_html += '<ul><li>None selected</li></ul>'
        #
        # if len(subservices):
        #     subservice_list += '<br>'
        #     subservice_list_html += '<ul>'
        #     for subservice in subservices:
        #         subservice_list += f"""{subservice}<br>"""
        #         subservice_list_html += f"""<li>{subservice}</li>"""
        #     subservice_list += '<br'
        #     subservice_list_html += '</ul>'
        # else:
        #     subservice_list += '<br>None selected<br>'
        #     subservice_list_html += '<ul><li>None selected</li></ul>'
        #
        # # Email content
        # text = f"""\
        #                         You have subscribed to receive notifications from the following services:
        #                         <br>
        #                         {service_list}
        #                         You have subscribed to receive notifications from the following sub-services:
        #                         {subservice_list}
        #                         """
        #
        # html = f"""\
        #                         <html>
        #                           <body>
        #                             <p>You have subscribed to receive notifications from the following Service(s)
        #                             <br>
        #                             </p>
        #                             {service_list_html}
        #                             <p>You have subscribed to receive notifications from the following Sub-service(s)
        #                             <br>
        #                             </p>
        #                             {subservice_list_html}
        #                           </body>
        #                         </html>
        #                         """
        #
        # subject = "Subscription requested!"
        #
        # mail_sender = MailSender(html, subject, text, email)
        # mail_sender.send_mail()

    def clean(self):
        # Create token
        token = secrets.token_hex(64)

        # Update User's token
        self.cleaned_data["token"] = token

        # if self.check_mail_domain():
        #     self.notify_user_email()

    class Meta:
        model = Subscriber
        fields = [
            'name',
            'email',
            'services',
            'subservices',
            'token'
        ]


class SubscriberForm(forms.ModelForm):
    """
    This methods is related with the insertion and update process that belong to the admin
    """
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

        # It verifies the existence or not of that email domain
        domain_exist = EmailDomain.objects.filter(domain=domain).count()

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
        else:
            self.update_user_token_by_user_id(self.instance.pk)

        return self.cleaned_data

    @staticmethod
    def send_link_by_user_id(user_id):
        """
        Method to send a notification link given the User ID
        :param user_id:
        :return:
        """
        # It gets the user's email and token given its ID
        user = Subscriber.objects.filter(pk=user_id).values('email', 'token')

        email = user[0]['email']
        token = user[0]['token']

        EmailActions.send_subscription_notification(email, token)
        # # hostname = 'http://127.0.0.1:8000'
        # hostname = 'https://status2.amlight.net'
        #
        # # we should create a mechanism to get the hostname. This option works on views request
        # # print(HttpRequest.get_host(self))
        #
        # view_path = '/subscriber'
        #
        # link = hostname + view_path + '/' + email + '/' + token
        #
        # # Email content
        # text = f"""\
        #                 Link to modify your subscription:
        #                 {link}
        #                 """
        #
        # html = f"""\
        #                 <html>
        #                   <body>
        #                     <p>Link to modify your subscription<br>
        #                     </p>
        #                     <a href="{link}">Modify your subscription</a>
        #                   </body>
        #                 </html>
        #                 """
        #
        # subject = "Modification requested on Subscription!"
        #
        # mail_sender = MailSender(html, subject, text, email)
        # mail_sender.send_mail()

    @staticmethod
    def send_link_by_user_email(_email):
        """
        Method to send a notification link given the User email
        :param _email:
        :return:
        """
        # It gets the user's token given its email
        user = Subscriber.objects.filter(email=_email).values('token')
        _token = str(user[0]['token'])  # Need to cast, otherwise it will have a nontype error

        EmailActions.send_subscription_notification(_email, _token)

        # # hostname = 'http://127.0.0.1:8000'
        # hostname = 'https://status2.amlight.net'
        #
        # # we should create a mechanism to get the hostname. This option works on views request
        # # print(HttpRequest.get_host(self))
        #
        # view_path = '/subscriber'  # email and toke
        #
        # link = hostname + view_path + '/' + _email + '/' + token
        #
        # # Email content
        # text = f"""\
        #                     Link to modify your subscription:
        #                     {link}
        #                     """
        #
        # html = f"""\
        #                     <html>
        #                       <body>
        #                         <p>Link to modify your subscription<br>
        #                         </p>
        #                         <a href="{link}">Modify your subscription</a>
        #                       </body>
        #                     </html>
        #                     """
        #
        # subject = "Modification requested on Subscription!"
        #
        # mail_sender = MailSender(html, subject, text, _email)
        # mail_sender.send_mail()

    @staticmethod
    def get_user_data(_email, _token):
        """
        Method to get the services and sub-services associated
        with a user(subscriber) given its email and token
        :param _email:
        :param _token:
        :return:
        """
        # It collect the services and subservices associated to an user
        services_subservices = Subscriber.objects.filter(email=_email, token=_token).values('services', 'subservices')
        services = list()
        sub_services = list()

        # It creates the list of services and subservices
        # avoiding repeated items on the list
        for service_subservice in services_subservices:
            services.append(service_subservice['services']) \
                if service_subservice['services'] not in services else services
            sub_services.append(service_subservice['subservices']) \
                if service_subservice['subservices'] not in sub_services else sub_services

        if len(services_subservices) == 0:
            print("Errors on the information provided")

    def update_user_token_by_user_id(self, user_id):
        """
        Method to update the user token after submitting its information
        This function was thought to be used considering the User ID as a reference
        :param user_id:
        :return:
        """
        _token = secrets.token_hex(64)

        # It will be used on read only cases
        self.instance.token = _token

        # It will be used on no read only cases
        # self.cleaned_data["token"] = _token

        # Or
        # Subscriber.objects.filter(pk=user_id).update(token=_token)

        # Or
        # obj = Subscriber.objects.get(pk=user_id)
        # obj.token = _token
        # obj.save()

    def update_user_token_by_user_email(self, _email):
        """
        Method to update the user token after submitting its information
        This function was thought to be used considering the User email as a reference
        :param _email:
        :return:
        """
        _token = secrets.token_hex(64)

        # It will be used on read only cases
        self.instance.token = _token

        # It will be used on no read only cases
        # self.cleaned_data["token"] = _token

        # Or
        # Subscriber.objects.filter(email=_email).update(token=_token)

        # Or
        # obj = Subscriber.objects.get(email=_email)
        # obj.token = _token
        # obj.save()
