from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("programs/", views.programs, name="programs"),
    path("impact/", views.impact, name="impact"),
    path("future-centre/", views.future_centre, name="future_centre"),
    path("stories/", views.stories, name="stories"),
    path("donate/", views.donate, name="donate"),
    path("contact/", views.contact, name="contact"),

    # Old template's routes — kept as permanent redirects so any existing
    # bookmarks/search-engine links to /causes/ or /gallery/ still resolve.
    path("causes/", views.legacy_causes_redirect, name="legacy_causes"),
    path("gallery/", views.legacy_gallery_redirect, name="legacy_gallery"),
]
