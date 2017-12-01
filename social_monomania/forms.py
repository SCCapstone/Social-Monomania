from django import forms

class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True, label= 'Email', widget=forms.TextInput(attrs={
                    'class': 'email_input', 'placeholder': 'Your email here'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'subject_input', 'placeholder': 'Please keep your subject concise...'}))
    message = forms.CharField(widget=forms.Textarea(attrs={
                    'class': 'message_input', 'placeholder': 'Your message here...'}))
