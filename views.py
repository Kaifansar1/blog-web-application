from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import BlogPost
from .forms import BlogPostForm

def home(request):
    post_list = BlogPost.objects.select_related('author').order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'blog/post_delete.html', {'post': post})
