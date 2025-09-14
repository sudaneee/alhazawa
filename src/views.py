from django.shortcuts import render
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
    Picture,
    Paragraph,
    GalleryVideo,
)
# Create your views here.

def home(request):
    aboutObject = About.objects.all().first()
    sliderObjects = Slider.objects.all()[:2]
    causeObjects = FeatureCause.objects.all()[:2]
    trusteeObjects = Trustee.objects.all()
    testimonieObjects = Testimonie.objects.all()[:3]
    galleryObjects = Gallery.objects.all().order_by('-id')

    # Safe lookups (avoid breaking if not found)
    picture = Picture.objects.filter(tag="Founder").first()
    welcome_note = Paragraph.objects.filter(tag__icontains="welcome").first()
    appreciation_video = GalleryVideo.objects.filter(tag__icontains="appreciation").first()

    # Long Vacation
    long_vacation_images = Gallery.objects.filter(tag="long_vacation")
    long_vacation_videos = GalleryVideo.objects.filter(tag="long_vacation")
    long_vacation_paragraph = Paragraph.objects.filter(tag="long_vacation").first()

    # Classroom
    classroom_images = Gallery.objects.filter(tag="classroom")
    classroom_videos = GalleryVideo.objects.filter(tag="classroom")
    classroom_paragraph = Paragraph.objects.filter(tag="classroom").first()

    # Feeding
    feeding_images = Gallery.objects.filter(tag="feeding")
    feeding_videos = GalleryVideo.objects.filter(tag="feeding")
    feeding_paragraph = Paragraph.objects.filter(tag="feeding").first()

    context = {
        'sliders': sliderObjects,
        'about': aboutObject,
        'causes': causeObjects,
        'trustee': trusteeObjects,
        'testimoinies': testimonieObjects,
        'galleries': galleryObjects,
        'picture': picture,
        'welcome_note': welcome_note,
        'appreciation_video': appreciation_video,

        # New programme sections
        'long_vacation_images': long_vacation_images,
        'long_vacation_videos': long_vacation_videos,
        'long_vacation_paragraph': long_vacation_paragraph,

        'classroom_images': classroom_images,
        'classroom_videos': classroom_videos,
        'classroom_paragraph': classroom_paragraph,

        'feeding_images': feeding_images,
        'feeding_videos': feeding_videos,
        'feeding_paragraph': feeding_paragraph,
    }
    return render(request, 'src/index.html', context)



def about(request):
    aboutObject = About.objects.all().first()
    whatObjects = WhatWeDo.objects.all()
    trusteeObjects = Trustee.objects.all()
    context = {
        'about': aboutObject,
        'wwd': whatObjects,
        'trustee': trusteeObjects,
    }
    return render (request, 'src/about.html', context)


def causes(request):
    causeObjects = FeatureCause.objects.all()
    context = {
        'causes': causeObjects,
    }
    return render(request, 'src/causes.html', context)

def contact(request):

    return render(request, 'src/contact.html')


def gallery(request):
    galleryObjects = Gallery.objects.all().order_by('-id')
    context = {
        'galleries': galleryObjects,

    }
    return render(request, 'src/gallery.html', context)