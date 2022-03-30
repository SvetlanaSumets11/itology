from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from itology.forms.advert_board import CommentForm
from itology.messages import SUCCESSFUL_CREATED_ADVERT, SUCCESSFUL_DELETED_ADVERT, SUCCESSFUL_UPDATED_ADVERT
from itology.models import Advert, Comment


class HomeView(ListView):
    template_name = 'advert_board/home.html'
    queryset = Advert.objects.all()
    paginate_by = 10


class AdvertView(DetailView):
    model = Advert
    template_name = 'advert_board/advert_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advert = get_object_or_404(Advert, pk=self.kwargs['pk'])
        context['advert'] = advert
        context['comments'] = advert.comment.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        advert = Advert.objects.filter(id=self.kwargs['pk'])[0]
        context['advert'] = advert
        context['comments'] = advert.comment.all()
        context['form'] = form

        if form.is_valid():
            Comment.objects.create(author=self.request.user, content=form.cleaned_data['content'], advert=advert)
            context['form'] = CommentForm()
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


class AdvertCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'subsections']

    def get_success_url(self):
        messages.success(self.request, SUCCESSFUL_CREATED_ADVERT)
        return reverse_lazy('users-home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        return super().form_valid(form)


class AdvertUpdateView(LoginRequiredMixin, UpdateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'subsections']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, SUCCESSFUL_UPDATED_ADVERT)
        return reverse_lazy('users-home')

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)


class AdvertDeleteView(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'advert_board/advert_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, SUCCESSFUL_DELETED_ADVERT)
        return reverse_lazy('users-home')

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)
