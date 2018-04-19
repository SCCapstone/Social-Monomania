from django import forms

class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True, label= 'Email', max_length=20, widget=forms.TextInput(attrs={
                    'class': 'email_input', 'placeholder': 'Your email here' }))
    subject = forms.CharField(required=True,max_length=20, widget=forms.TextInput(attrs={
                    'class': 'subject_input', 'placeholder': 'Please keep your subject concise...'}))
    message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
                    'class': 'message_input', 'placeholder': 'Your message here...'}))
