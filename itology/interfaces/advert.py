from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404

from itology.config import PROJECT_NOT_ACTIVE
from itology.models import Advert, Section


class AdvertInterface:
    @staticmethod
    def get_adverts_in_section(section: str) -> list[Advert]:
        section = get_object_or_404(Section, title=section)
        if not section.parent:
            adverts = list(set(Advert.objects.filter(sections__parent=section, status=PROJECT_NOT_ACTIVE)))
        else:
            adverts = section.adverts.filter(status=PROJECT_NOT_ACTIVE)
        return adverts

    @staticmethod
    def get_adverts_in_page(paginator: Paginator, page: str) -> list[Advert]:
        try:
            adverts = paginator.page(page)
        except PageNotAnInteger:
            adverts = paginator.page(1)
        except EmptyPage:
            adverts = paginator.page(paginator.num_pages)
        return adverts
