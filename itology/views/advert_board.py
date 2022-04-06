from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from itology.forms.advert_board import CommentForm
from itology.messages import SUCCESSFUL_CREATED_ADVERT, SUCCESSFUL_DELETED_ADVERT, SUCCESSFUL_UPDATED_ADVERT
from itology.models import Advert, Comment, Role, Section, Team
from itology.trello_manager import TrelloManager


class HomeView(ListView):
    template_name = 'advert_board/home.html'
    queryset = Advert.objects.all()
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['adverts'] = Advert.objects.all()
        context['sections'] = Section.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = super().get_queryset()
        context = self.get_context_data()

        adverts = context['adverts']
        section_title = request.GET.get('section')
        if section_title:
            section = get_object_or_404(Section, title=section_title)
            adverts = Advert.objects.filter(sections__parent=section) if not section.parent else section.advert.all()

        paginator = Paginator(adverts, self.paginate_by)
        try:
            adverts = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            adverts = paginator.page(1)
        except EmptyPage:
            adverts = paginator.page(paginator.num_pages)

        context['adverts'] = adverts
        return self.render_to_response(context=context)


class AdvertView(DetailView):
    model = Advert
    template_name = 'advert_board/advert_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advert = get_object_or_404(Advert, pk=self.kwargs['pk'])
        context['advert'] = advert
        context['roles'] = Role.objects.all()
        context['teams'] = Team.objects.filter(advert=advert).all()
        context['comments'] = advert.comment.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        advert = Advert.objects.filter(id=self.kwargs['pk']).first()
        context['advert'] = advert
        context['roles'] = Role.objects.all()
        context['teams'] = Team.objects.all()
        context['comments'] = advert.comment.all()
        context['comment_form'] = comment_form

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
        if 'Role' not in roles and 'Amount' not in amounts:
            for role, amount in zip(roles, amounts):
                Team.objects.create(
                    role=Role.objects.filter(title=role).first(),
                    advert=advert,
                    amount=int(amount),
                )
            advert.classify = True
            advert.save()

        occupied_role = request.POST.get('occupied_role')
        if occupied_role:
            teams = Team.objects.filter(advert=advert, role__title=occupied_role).first()
            teams.members.add(self.request.user)
            teams.amount = teams.amount - 1
            teams.save()

            teams = Team.objects.filter(advert=advert).all()
            for team in teams:
                if team.amount != 0:
                    return self.render_to_response(context=context)

            roles = [team.role.title for team in teams]
            members = []
            members.extend(team.members.all() for team in teams)
            emails = list(set(member.first().email for member in members))
            TrelloManager.create_team_environment(
                name=advert.title,
                roles=roles,
                description=advert.description,
                emails=emails,
            )

        return self.render_to_response(context=context)


class AdvertCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'advert_board/advert_profile.html'
    fields = ['title', 'description', 'sections']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()
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
