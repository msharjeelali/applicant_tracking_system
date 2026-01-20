from django import forms

ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('recruiter', 'Recruiter')
    )

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=15, 
                                 label="Enter First Name", 
                                 widget= forms.TextInput(attrs={
                                    'placeholder': 'John',
                                    'required': True
                                }))
    last_name = forms.CharField(max_length=15,
                                label='Enter Last Name',
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Doe',
                                    'required': True
                                }))
    email = forms.EmailField(label='Enter e-mail',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'abcdef@exmaple.com',
                                 'required': True
                             }))
    password = forms.CharField(min_length=8,
                               max_length=15,
                               label="Enter Password",
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': '********',
                                   'required': True
                               }))
    re_password = forms.CharField(min_length=8,
                                  max_length=15,
                                  label="Re-enter Password",
                                  widget=forms.PasswordInput(attrs={
                                      'placeholder': '********',
                                      'required': True
                                  }))
    
    role = forms.ChoiceField(choices=ROLE_CHOICES,
                             widget=forms.RadioSelect,
                             required=True
                             )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password and re_password and password != re_password:
            raise forms.ValidationError("Passwords donot match")
        
class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter e-mail',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'abcdef@exmaple.com',
                                 'required': True
                             }))
    password = forms.CharField(label = "Enter password",
                               widget=forms.PasswordInput(attrs={
                                    "placeholder": "********",
                                    "required": True
                                   }))