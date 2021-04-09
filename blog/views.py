from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template import context
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.forms import CreatePostForm, UpdatePostForm, CreateCommentForm
from blog.models import Tag, Post
from .models import ReviewPost
from django.http import HttpResponseRedirect


def LikeView(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('detail', args=[str(slug)]))


def home_page(request):
    tags = Tag.objects.all()
    posts = Post.objects.all()
    return render(request, 'home.html', {'tags': tags, 'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.kwargs.get('slug')
        queryset = queryset.filter(tags__slug=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.kwargs.get('slug')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

class PostCreateView(CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = UpdatePostForm
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        from django.urls import reverse
        return reverse('home')


class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(name__icontains=q) | Q(body__icontains=q))
        return queryset


class ReviewIndexPage(ListView):
    model = ReviewPost
    template_name = 'list_comments.html'
    context_object_name = 'list_comments'


class ReviewPostCreateView(CreateView):
    model = ReviewPost
    template_name = 'comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        post = self.kwargs['slug']
        user = self.request.user
        post = Post.objects.get(slug=post)
        comment = form.save(commit=False)
        comment.post = post
        comment.user = user
        comment.save()
        return super().form_valid(form)

    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form(self.get_form_class())
        return context



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required
def cart_add(request, id):
    cart = Cart(request)
    post = Post.objects.get(id=id)
    cart.add(product=post)
    return redirect("cart_detail")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    post = Post.objects.get(id=id)
    cart.remove(post)
    return redirect("cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='/account/login/')
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
