from src.models import (
    Slider,
    About,
    FeatureCause,
    WhatWeDo,
    Trustee,
    Testimonie,
    Outlet,
    GeneralInformation,

)

def general_data(request):
    generalInformationObjects = GeneralInformation.objects.all().first()
    return {
        'g_info': generalInformationObjects,
    }