"""
Builds the same JSON shape the original static site's js/data.js exposed as
`window.ALHAZAWA_DATA`, but generated live from the database on every
request. main.js / animations.js / gallery.js are unchanged — they only
ever read window.ALHAZAWA_DATA, and have no idea whether it came from a
static file or a Django view.

Keeping this in one place means every template that needs it just calls
build_site_data(request) and dumps it into a <script> tag.
"""

from src.models import (
    GeneralInformation,
    Pillar,
    CoreValue,
    Beneficiary,
    Pilot,
    RoadmapStage,
    FutureCentreZone,
    FuturePhase,
    DayTimelineStep,
    Gallery,
    DonationArea,
    PartnerCategory,
    InquiryType,
    Story,
    Event,
)

DONATION_AMOUNTS = [5000, 10000, 25000, 50000, 100000]


def _slug(text):
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in (text or "")).strip("-") or "item"


def _address_lines(address):
    if not address:
        return {"line1": "", "line2": "", "line3": ""}
    parts = [p.strip() for p in address.split(",") if p.strip()]
    parts += [""] * (3 - len(parts))
    return {"line1": parts[0], "line2": parts[1], "line3": ", ".join(parts[2:]) if len(parts) > 2 else parts[2]}


def build_site_data():
    g_info = GeneralInformation.objects.first()

    org = {
        "name": g_info.org_name if g_info else "Alhazawa Orphans & Girl Child Foundation",
        "shortName": "Alhazawa Foundation",
        "founder": g_info.founder_name if g_info else "Prof. Mansir Dodo",
        "address": _address_lines(g_info.address if g_info else ""),
        "phone": g_info.tel if g_info else "",
        "phoneHref": "".join(ch for ch in (g_info.tel if g_info else "") if ch.isdigit() or ch == "+"),
        "website": g_info.website if g_info else "",
        "email": g_info.email if g_info else "",
    }

    pillars = [
        {
            "id": _slug(p.name),
            "tag": p.tag,
            "name": p.name,
            "short": p.short,
            "description": p.description,
            "icon": p.icon,
            "image": p.image.url if p.image else "",
        }
        for p in Pillar.objects.all()
    ]

    values = [
        {
            "id": _slug(v.name),
            "name": v.name,
            "concept": v.concept or None,
            "description": v.description,
        }
        for v in CoreValue.objects.all()
    ]

    beneficiaries = [
        {"id": _slug(b.name), "name": b.name, "note": b.note, "description": b.description}
        for b in Beneficiary.objects.all()
    ]

    pilots = [
        {
            "id": _slug(p.name),
            "name": p.name,
            "description": p.description,
            "outcome": p.outcome,
            "icon": p.icon,
        }
        for p in Pilot.objects.all()
    ]

    roadmap = [
        {
            "term": stage.term,
            "focus": stage.focus,
            "activities": [a.text for a in stage.activities.all()],
        }
        for stage in RoadmapStage.objects.prefetch_related("activities").all()
    ]

    future_centre = {
        "intro": g_info.future_centre_intro if g_info else "",
        "zones": [{"id": _slug(z.name), "name": z.name, "description": z.description, "image": z.image.url if z.image else ""} for z in FutureCentreZone.objects.all()],
        "phases": [{"id": _slug(ph.label), "label": ph.label, "title": ph.title, "note": ph.note} for ph in FuturePhase.objects.all()],
    }

    day_timeline = [
        {"time": t.time_label, "title": t.title, "description": t.description}
        for t in DayTimelineStep.objects.all()
    ]

    gallery = [
        {
            "id": f"g{g.pk}",
            "src": g.image.url if g.image else "",
            "category": g.category.name if g.category else "Uncategorised",
            "caption": g.caption or "",
            "size": g.size_hint,
        }
        for g in Gallery.objects.select_related("category").all()
        if g.image
    ]

    stories = [
        {
            "id": f"s{s.pk}",
            "sample": s.is_sample,
            "featured": s.is_featured,
            "category": s.category.name if s.category else "",
            "title": s.title,
            "excerpt": s.excerpt,
            "image": s.image.url if s.image else "",
            "date": s.date_label or "",
        }
        for s in Story.objects.select_related("category").all()
    ]

    events = [
        {
            "id": f"e{e.pk}",
            "sample": e.is_sample,
            "category": e.category.name if e.category else "",
            "title": e.title,
            "description": e.description,
            "dateLabel": e.event_date.strftime("%d %B %Y") if e.event_date else (e.date_label or "Date to be announced"),
        }
        for e in Event.objects.select_related("category").all()
    ]

    donation_areas = [
        {"id": _slug(d.name), "name": d.name, "description": d.description}
        for d in DonationArea.objects.all()
    ]

    partner_categories = [p.name for p in PartnerCategory.objects.all()]
    inquiry_types = [i.name for i in InquiryType.objects.all()]

    return {
        "org": org,
        "pillars": pillars,
        "values": values,
        "vision": g_info.vision if g_info else "",
        "mission": g_info.mission if g_info else "",
        "beneficiaries": beneficiaries,
        "roadmap": roadmap,
        "pilots": pilots,
        "futureCentre": future_centre,
        "gallery": gallery,
        "dayTimeline": day_timeline,
        "stories": stories,
        "events": events,
        "donationAreas": donation_areas,
        "donationAmounts": DONATION_AMOUNTS,
        "partnerCategories": partner_categories,
        "inquiryTypes": inquiry_types,
    }
