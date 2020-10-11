from django import forms
from django.contrib.auth.models import User


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateTimeForm(forms.Form):
    from_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                    label="Дата отсчёта",
                                    widget=DateTimeInput(attrs={'class': 'form-control'},)
                                    )
    till_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                    label="Дата окончания",
                                    widget=DateTimeInput(attrs={'class': 'form-control'})
                                    )


class SendMailForm(forms.Form):
    send_mail_user = forms.ModelChoiceField(label='Кому отправлять письма?',
                                            queryset=User.objects.all(),
                                            to_field_name="id",
                                            empty_label="Выбрать...",
                                            required=False,
                                            )
    send_mail_user.widget.attrs.update({'class': 'form-control'})
