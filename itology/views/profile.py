from os import path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from itology.config import DOWNLOAD_FILE_LINK
from itology.forms.login import UpdateClientForm, UpdateUserForm
from itology.interfaces.team import TeamInterface
from itology.messages import SUCCESSFUL_UPDATED_PROFILE
from itology.models import Certificate


def download_certificate(request, uuid: str) -> HttpResponse:
    file_name = f'{uuid}.pdf'
    with open(path.join(DOWNLOAD_FILE_LINK, file_name), 'rb') as file:
        response = HttpResponse(file, content_type='pdf')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response


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

        confirmed_project = request.POST.get('confirmation')
        if confirmed_project:
            TeamInterface.confirm_execution(confirmed_project)

        certified_project = request.POST.get('download_certificate')
        if certified_project:
            certificate_uuid = Certificate.objects.filter(advert__title=certified_project, nominee=request.user).first()
            return redirect(to='download_certificate', uuid=certificate_uuid.uuid)

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateClientForm(instance=request.user.client)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'adverts': request.user.adverts.all(),
        'projects': set(team.advert for team in request.user.teams.all()),
        'roles': [team.role for team in request.user.teams.all()],
    }
    return render(request=request, template_name='login/profile.html', context=context)
