from django import forms

class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True, label= 'Email', widget=forms.TextInput(attrs={
                    'class': 'email_input', 'placeholder': 'email'}))
    subject = forms.CharField(required=True, margin_top=20px, widget=forms.TextInput(attrs={
                    'class': 'subject_input', 'placeholder': 'subject'}))
    message = forms.CharField(margin_top=20px,widget=forms.Textarea(attrs={
                    'class': 'message_input', 'placeholder': 'Your message here...'}))