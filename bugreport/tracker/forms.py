from django import forms
from .models import Bug

class TrackTicketForm(forms.Form):

    # class Meta:
    #     model = Bug
    #     fields = ('ticket_number', )
    ticket_number = forms.UUIDField()
