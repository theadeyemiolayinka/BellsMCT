from django import forms

from .models import Enquiry

class EnquiryFormSetFactory(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Enquiry.objects.all() 

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'subject', 'message']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)