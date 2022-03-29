from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from itology.forms.advert_board import CommentForm
from itology.models import Advert, Comment


class HomeView(ListView):
    template_name = 'advert_board/home.html'
    queryset = Advert.objects.all()
    paginate_by = 10


class PostView(DetailView):
    model = Advert
    template_name = 'advert_board/advert_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']

        form = CommentForm()
        advert = get_object_or_404(Advert, pk=pk)
        comments = advert.comment.all()

        context['advert'] = advert
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        advert = Advert.objects.filter(id=self.kwargs['pk'])[0]
        comments = advert.comment.all()

        context['advert'] = advert
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            author = self.request.user
            content = form.cleaned_data['content']
            Comment.objects.create(author=author, content=content, advert=advert)
            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'subsections']

    def get_success_url(self):
        messages.success(
            self.request, 'Your advert has been created successfully.')
        return reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'subsections']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update
        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your advert has been updated successfully.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'advert_board/advert_confirm_delete.html'

    def get_success_url(self):
        messages.success(
            self.request, 'Your advert has been deleted successfully.')
        return reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)
