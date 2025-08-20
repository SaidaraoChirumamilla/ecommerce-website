from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm, CustomLoginForm, ProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpView(CreateView):
    """View for user registration with enhanced validation"""
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        """Handle successful form submission"""
        try:
            response = super().form_valid(form)
            user = self.object
            messages.success(
                self.request, 
                f'Welcome {user.first_name}! Your account has been created successfully. Please sign in to continue.'
            )
            return response
        except Exception as e:
            messages.error(self.request, 'An error occurred while creating your account. Please try again.')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """Handle form validation errors"""
        # Add form errors to messages for better UX
        for field, errors in form.errors.items():
            for error in errors:
                if field == '__all__':
                    messages.error(self.request, error)
                else:
                    field_name = form.fields[field].label or field.replace('_', ' ').title()
                    messages.error(self.request, f"{field_name}: {error}")
        
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


def login_view(request):
    """Custom login view with enhanced validation and remember me functionality"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = form.cleaned_data.get('remember_me')
            
            # Set session expiry based on remember me
            if remember_me:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # Browser session
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to next page or profile
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('profile')
        else:
            # Add form errors to messages for better UX
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile_view(request):
    """View for displaying user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_update_view(request):
    """View for updating user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_update.html', {'form': form})


def home_view(request):
    """Home page view"""
    return render(request, 'home.html')
