from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Tag

def blog_list(request):
    tag = request.GET.get('tag')
    posts = BlogPost.objects.filter(featured=False)
    featured_post = BlogPost.objects.filter(featured=True).first()
    tags = Tag.objects.all()
    if tag:
        posts = posts.filter(tags__name=tag)
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'featured_post': featured_post,
        'tags': tags,
        'active_tag': tag,
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    return render(request, 'blog/blog_detail.html', {'post': post})


