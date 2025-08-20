from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
import re

User = get_user_model()

class SignUpForm(UserCreationForm):
    """Custom signup form with comprehensive validations"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        }),
        help_text="We'll never share your email with anyone else."
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your first name',
            'autocomplete': 'given-name'
        }),
        help_text="Enter your first name (letters only, 2-30 characters)."
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your last name',
            'autocomplete': 'family-name'
        }),
        help_text="Enter your last name (letters only, 2-30 characters)."
    )
    
    username = forms.CharField(
        max_length=30,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username',
            'autocomplete': 'username'
        }),
        help_text="3-30 characters. Letters, digits and @/./+/-/_ only."
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password'
        }),
        help_text="Password must be 8-12 characters with upper/lower case letters, at least one number, and one special character (@, #, $, &, *, -, +, ?, =, !). No spaces allowed."
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        }),
        help_text="Enter the same password as before, for verification."
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="I agree to the Terms of Service and Privacy Policy",
        error_messages={
            'required': 'You must accept the terms and conditions to register.'
        }
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'terms_accepted')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('username', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-3'),
                Column('password2', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('terms_accepted', css_class='form-group col-md-12 mb-3'),
            ),
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg w-100')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email address is required.")
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists.")
        
        # Check for disposable email domains
        disposable_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 
            'mailinator.com', 'yopmail.com', 'temp-mail.org'
        ]
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            raise ValidationError("Please use a permanent email address.")
        
        return email.lower()
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        if len(username) > 30:
            raise ValidationError("Username cannot be longer than 30 characters.")
        
        # Check for valid characters
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        
        # Check for reserved usernames
        reserved_usernames = [
            'admin', 'administrator', 'root', 'user', 'test', 'guest', 
            'api', 'www', 'mail', 'email', 'support', 'help', 'info'
        ]
        if username.lower() in reserved_usernames:
            raise ValidationError("This username is reserved. Please choose another.")
        
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError("First name is required.")
        
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")
        
        if not re.match(r'^[a-zA-Z\s\'-]+$', first_name):
            raise ValidationError("First name can only contain letters, spaces, hyphens, and apostrophes.")
        
        return first_name.title()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError("Last name is required.")
        
        if len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")
        
        if not re.match(r'^[a-zA-Z\s\'-]+$', last_name):
            raise ValidationError("Last name can only contain letters, spaces, hyphens, and apostrophes.")
        
        return last_name.title()
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise ValidationError("Password is required.")
        
        # Check length: between 8 to 12 characters
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        if len(password1) > 12:
            raise ValidationError("Password must be between 8 to 12 characters.")
        
        # Check for spaces
        if ' ' in password1:
            raise ValidationError("Password must not contain any spaces.")
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password1):
            raise ValidationError("Password must have upper and lower case letters.")
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password1):
            raise ValidationError("Password must have upper and lower case letters.")
        
        # Check for at least one digit
        if not re.search(r'\d', password1):
            raise ValidationError("Password must have at least one number.")
        
        # Check for at least one special character from the specified list
        if not re.search(r'[@#$&*\-+?=!]', password1):
            raise ValidationError("Password must have at least one special character (@, #, $, &, *, -, +, ?, =, !).")
        
        # Check for common passwords
        common_passwords = [
            'password', '12345678', 'qwerty', 'abc123', 'password123',
            'admin', 'letmein', 'welcome', 'password1'
        ]
        if password1.lower() in common_passwords:
            raise ValidationError("This password is too common. Please choose a more secure password.")
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        
        # Check if passwords match
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match.")
        
        # Check if password contains personal information
        if password1 and first_name and first_name.lower() in password1.lower():
            raise ValidationError("Password cannot contain your first name.")
        
        if password1 and last_name and last_name.lower() in password1.lower():
            raise ValidationError("Password cannot contain your last name.")
        
        if password1 and username and username.lower() in password1.lower():
            raise ValidationError("Password cannot contain your username.")
        
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    """Custom login form with comprehensive validations"""
    
    username = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'autofocus': True,
            'autocomplete': 'email'
        }),
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.'
        }
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        }),
        error_messages={
            'required': 'Password is required.'
        }
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Remember me for 30 days"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-group mb-3'),
            Field('password', css_class='form-group mb-3'),
            Field('remember_me', css_class='form-group mb-3'),
            Submit('submit', 'Sign In', css_class='btn btn-primary btn-lg w-100')
        )
        
        # Remove default error messages from parent class
        self.error_messages = {
            'invalid_login': 'Invalid email address or password. Please try again.',
            'inactive': 'This account has been deactivated. Please contact support.',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Email address is required.")
        
        try:
            validate_email(username)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        
        return username.lower()
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password is required.")
        
        if len(password) < 1:
            raise ValidationError("Password cannot be empty.")
        
        return password
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Check if user exists
            try:
                user = User.objects.get(email=username)
                if not user.is_active:
                    raise ValidationError("This account has been deactivated. Please contact support.")
            except User.DoesNotExist:
                raise ValidationError("No account found with this email address.")
            
            # Authenticate the user
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            
            if self.user_cache is None:
                raise ValidationError("Invalid email address or password. Please check your credentials and try again.")
            
            self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'address_line_1', 'address_line_2',
            'city', 'state', 'country', 'postal_code', 'profile_image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-3'),
                Column('profile_image', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('address_line_1', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('address_line_2', css_class='form-group col-md-12 mb-3'),
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-3'),
                Column('state', css_class='form-group col-md-4 mb-3'),
                Column('postal_code', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('country', css_class='form-group col-md-12 mb-3'),
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-primary btn-lg')
        ) 