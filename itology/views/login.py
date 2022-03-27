from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from itology.forms.login import LoginForm, RegisterForm, UpdateClientForm, UpdateUserForm
from itology.messages import ACCOUNT_CREATED, EMAILED_INSTRUCTIONS, SUCCESSFUL_CHANGED_PASS, SUCCESSFUL_UPDATED_PROFILE


def home(request):
    return render(request, 'login/home.html')


def landing(request):
    return render(request, 'login/landing.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'login/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, ACCOUNT_CREATED.format(username=username))
            return redirect(to='login')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('users-home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    subject_template_name = 'login/password_reset_subject'
    success_message = EMAILED_INSTRUCTIONS
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'login/change_password.html'
    success_message = SUCCESSFUL_CHANGED_PASS
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateClientForm(request.POST, request.FILES, instance=request.user.client)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, SUCCESSFUL_UPDATED_PROFILE)
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateClientForm(instance=request.user.client)

    return render(request, 'login/profile.html', {'user_form': user_form, 'profile_form': profile_form})
