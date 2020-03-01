from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import PostModel
from .forms import PostModelForm

@login_required
def post_model_create_view(request):
    # if request.method == "POST":
    #     form = PostModelForm(request.POST)
    #     if form.is_valid:
    #         form.save(commit=False)
    #         print(form.cleaned_data)
    form = PostModelForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Created a new blog post!")
        context = {
            "form": PostModelForm()
        }
    template = "blog/create-view.html"
    return render(request, template, context)

def post_model_detail_view(request, slug):
    obj = get_object_or_404(PostModel, slug=slug)
    template = "blog/detail-view.html"
    context = {
        "object": obj
    }
    return render(request, template, context)

def post_model_list_view(request):
    search_query = request.GET.get("q", None)
    qs = PostModel.objects.all()
    if search_query is not None:
        qs = qs.filter(
            Q(title__icontains=search_query) |
            Q(slug__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    template = "blog/list-view.html"
    context = {
        "object": qs,
    }
    return render(request, template, context)

@login_required
def post_model_update_view(request, slug):
    obj = get_object_or_404(PostModel, slug=slug)
    form = PostModelForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated blog post!")
        return HttpResponseRedirect(f"/blog/{obj.slug}/")
    template = "blog/update-view.html"
    return render(request, template, context)

@login_required
def post_model_delete_view(request, slug):
    obj = get_object_or_404(PostModel, slug=slug)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Deleted blog post!")
        return HttpResponseRedirect(f"/blog/")
    template = "blog/delete-view.html"
    context = {
        "object": obj
    }
    return render(request, template, context)


# @login_required(login_url="/login/")
# def login_required_view(request):
#     qs = PostModel.objects.all()
#     context = {"object": qs}
#     if request.user.is_authenticated:
#         template = "blog/list-view.html"
#     else:
#         template = "blog/list-view-public.html"
#         # raise Http404
#         return HttpResponseRedirect("/login/")

#   return render(request, template, context)

def post_model_robust_view(request, slug=None):
    obj = None
    context = {}
    success_message = "A new post was created!"
    template = "blog/detail-view.html"

    if slug is None:
        print('flag')
        template = "blog/create-view.html"

    if slug is not None:
        obj = get_object_or_404(PostModel, slug=slug)
        print(f"if slug is not none ----->{obj}")
        context["object"] = obj
        template = "blog/detail-view.html"
        if "edit" in request.get_full_path():
            template = "blog/update-view.html"
        elif "delete" in request.get_full_path():
            template = "blog/delete-view.html"
            if request.method == "POST":
                obj.delete()
                messages.success(request, "Deleted blog post!")
                return HttpResponseRedirect(f"/blog/")

    form = PostModelForm(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        obj2 = form.save(commit=False)
        print(f"------>{obj}<------")
        obj2.save()
        # messages.success("request", success_message)
        if obj is not None:
            return HttpResponseRedirect(f"/blog/{obj.slug}")
        context["form"] = PostModelForm()

    return render(request, template, context)