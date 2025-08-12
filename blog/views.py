from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

from .models import Post
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after successful signup
    else:
        # form = UserCreationForm()
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('home')
        else:
            return redirect('login')
    else:
        form = PostForm()
    return render(request, 'blog/home.html', {'posts': posts,'form': form})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    #return render(request, 'blog/post_detail.html', {'post': post})
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', slug=slug)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
