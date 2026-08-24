from django.contrib import messages
from django.shortcuts import render, redirect

from src.models import (
    GalleryVideo,
    Testimonial,
    InquiryType,
    ContactMessage,
    Pillar,
    FutureCentreZone,
    FuturePhase,
    Story,
)


def home(request):
    context = {
        "testimonials": Testimonial.objects.all()[:3],
        "videos": GalleryVideo.objects.select_related("category").all()[:2],
    }
    return render(request, "src/index.html", context)


def about(request):
    return render(request, "src/about.html")


def programs(request):
    context = {
        "pillars": Pillar.objects.all(),
        "skills_zone": FutureCentreZone.objects.filter(name__icontains="skill").first(),
    }
    return render(request, "src/programs.html", context)


def impact(request):
    context = {
        "videos": GalleryVideo.objects.select_related("category").all(),
    }
    return render(request, "src/impact.html", context)


def future_centre(request):
    context = {
        "zones": FutureCentreZone.objects.all(),
        "phases": FuturePhase.objects.all(),
    }
    return render(request, "src/future_centre.html", context)


def stories(request):
    context = {
        "featured_story": Story.objects.filter(is_featured=True).select_related("category").first(),
    }
    return render(request, "src/stories.html", context)


def donate(request):
    return render(request, "src/donate.html")


def contact(request):
    if request.method == "POST":
        inquiry_type_id = request.POST.get("inquiry_type")
        ContactMessage.objects.create(
            inquiry_type_id=inquiry_type_id if inquiry_type_id else None,
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            subject=request.POST.get("subject", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        messages.success(request, "sent")
        return redirect("contact")

    context = {"inquiry_types": InquiryType.objects.all()}
    return render(request, "src/contact.html", context)


# --- Backward-compatible redirects for the old template's routes ---------
def legacy_causes_redirect(request):
    return redirect("donate", permanent=True)


def legacy_gallery_redirect(request):
    return redirect("impact", permanent=True)
