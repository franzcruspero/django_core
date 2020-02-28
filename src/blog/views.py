from django.http import HttpResponse, Http404, HttpResponseRedirect
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
    qs = PostModel.objects.all()
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
