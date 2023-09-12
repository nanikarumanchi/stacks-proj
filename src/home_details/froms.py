from django import forms


class ContactForm(forms.Form):
    fullname = forms.CharField(label='Name',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control my-2',
                                   'placeholder': 'Enter fullname'
                               }))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control my-2',
                                 'placeholder': 'Enter Email'
                             }))
    content = forms.CharField(label='Ticket',
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control my-2',
                                  'rows': '3',
                                  'placeholder': 'Enter content'
                              }))
