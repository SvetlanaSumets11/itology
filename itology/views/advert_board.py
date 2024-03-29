from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from itology.config import PROJECT_NOT_ACTIVE
from itology.forms.advert_board import CommentForm
from itology.interfaces.advert import AdvertInterface
from itology.interfaces.team import TeamInterface
from itology.messages import SUCCESSFUL_CREATED_ADVERT, SUCCESSFUL_DELETED_ADVERT, SUCCESSFUL_UPDATED_ADVERT
from itology.models import Advert, Comment, Role, Section, Team


class HomeView(ListView):
    template_name = 'advert_board/home.html'
    context_object_name = 'adverts'
    paginate_by = 2

    def get_queryset(self):
        section_title = self.request.GET.get('section')
        if section_title:
            return AdvertInterface.get_adverts_in_section(section_title)
        return Advert.objects.filter(status=PROJECT_NOT_ACTIVE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.get_all()
        return context


class AdvertView(DetailView):
    model = Advert
    template_name = 'advert_board/advert_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advert = get_object_or_404(Advert, pk=self.kwargs['pk'])
        context['advert'] = advert
        context['roles'] = Role.get_all()
        context['teams'] = Team.objects.filter(advert=advert).all()
        context['comments'] = advert.comments.all()
        context['form'] = CommentForm()
        context['my_roles'] = advert.get_user_roles(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        advert = Advert.objects.filter(id=self.kwargs['pk']).first()
        context['advert'] = advert
        context['roles'] = Role.get_all()
        context['teams'] = Team.objects.filter(advert=advert).all()
        context['comments'] = advert.comments.all()
        context['comment_form'] = comment_form
        context['my_roles'] = advert.get_user_roles(user=request.user)

        if comment_form.is_valid():
            Comment.objects.create(
                author=self.request.user,
                content=comment_form.cleaned_data.get('content'),
                advert=advert,
            )
            context['comment_form'] = CommentForm()
            return self.render_to_response(context=context)

        roles = request.POST.getlist('role')
        amounts = request.POST.getlist('amount')
        if TeamInterface.has_selected_role(roles, amounts):
            TeamInterface.create_team_of_role(advert, roles, amounts)

        occupied_role = request.POST.get('occupied_role')
        if occupied_role:
            TeamInterface.enroll_in_team(advert, occupied_role, user=self.request.user)

        completed_role = request.POST.get('completed_role')
        if completed_role:
            TeamInterface.complete_role(advert, completed_role, user=self.request.user)

        context['my_roles'] = advert.get_user_roles(user=request.user)
        return self.render_to_response(context=context)


class AdvertCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'sections']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.get_all()
        return context

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
    fields = ['title', 'description', 'sections']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.get_all()
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
