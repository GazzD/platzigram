"""" Post views. """

# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

# Forms
from posts.forms import PostForm

# Models
from posts.models import Post

class PostsFeedView(LoginRequiredMixin, ListView):
    """ Return all published posts. """
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    """ Return post detail. """
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """ Create new post. """
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        """ Add user profile to context. """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context



@login_required
def create_post(request):
    """ Create post view. """
    
    # Initialize form 
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')

    return render(
        request=request,
        template_name='posts/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile
        }
    )