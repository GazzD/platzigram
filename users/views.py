""" User views """

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

#Models
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Post

# Exceptions
from django.db.utils import IntegrityError

# Forms
from users.forms import ProfileForm
from users.forms import SignupForm

class LoginView(auth_views.LoginView):
    """ Login view """
    template_name = 'users/login.html'

class UserDetailView(LoginRequiredMixin, DetailView):
    """ User detail view. """
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    # Override method to add data to context
    def get_context_data(self, **kwargs):
        """ Add posts to context. """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class SignupView(FormView):
    """ Users signup view. """
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """ Save form data. """
        form.save()
        return super().form_valid(form) 

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """ Upddate profile view. """
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """ Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """ Return tyo user's profile"""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """ Logout view. """
    template_name = 'users/logged_out.html'

def login_view(request):
    """ Login view. """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})    
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    """ Logout view """
    logout(request)
    return redirect('users:login')

def signup(request):
    """Sign up view."""
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        
    return render(
        request=request, 
        template_name='users/signup.html',
        context={
            'form': form
        }
    )


@login_required
def update_profile(request):
    """ Update user's profile view. """

    # Initialize profile form
    profile_form = ProfileForm()

    # Get profile from user
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            data = profile_form.cleaned_data
            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            if 'picture' in data:
                profile.picture = data['picture']
            profile.save()
            
            return redirect(reverse('users:detail ', kwargs={'username': request.user.username}))

    return render(
        request=request,
        template_name='users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': profile_form
        }
        
    )