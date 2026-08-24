import json

from src.models import GeneralInformation, About, FounderProfile, TeamMember
from src.site_data import build_site_data


def general_data(request):
    """
    Injected into every template's context automatically (see
    DjangoApp/settings.py TEMPLATES). Keeps the header, footer, About
    section, Founder profile and the full JS data blob available on every
    page without each view needing to fetch them individually.
    """
    return {
        "g_info": GeneralInformation.objects.first(),
        "about": About.objects.first(),
        "founder": FounderProfile.objects.first(),
        "team": TeamMember.objects.all(),
        "site_data_json": json.dumps(build_site_data()),
    }
