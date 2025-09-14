from django.contrib import admin
from src.models import (
    Slider,
    About,
    FeatureCause,
    WhatWeDo,
    Trustee,
    Testimonie,
    Outlet,
    GeneralInformation,
    Gallery,
    GalleryVideo,
    Picture,
    Paragraph,
)

# Register your models here.
admin.site.register(Slider)
admin.site.register(About)
admin.site.register(FeatureCause)
admin.site.register(WhatWeDo)
admin.site.register(Trustee)
admin.site.register(Testimonie)
admin.site.register(Outlet)
admin.site.register(GeneralInformation)
admin.site.register(Gallery)
admin.site.register(GalleryVideo)
admin.site.register(Picture)
admin.site.register(Paragraph)