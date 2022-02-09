from django import forms

# class ProjectBugForm(forms.ModelForm):
#
#     class Meta:
#         model = Bug
#         fields = ['description']
    #description = forms.CharField(widget=forms.Textarea(attrs={"cols":40, "rows":10, "maxlength":1000}))
class TrackTicketForm(forms.Form):
    ticket_number = forms.UUIDField()
