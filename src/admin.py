from django.contrib import admin
from django.utils.html import format_html

from src.models import (
    GeneralInformation,
    About,
    FounderProfile,
    TeamMember,
    Pillar,
    CoreValue,
    Beneficiary,
    Pilot,
    RoadmapStage,
    RoadmapActivity,
    FutureCentreZone,
    FuturePhase,
    DayTimelineStep,
    GalleryCategory,
    Gallery,
    GalleryVideo,
    DonationArea,
    PartnerCategory,
    InquiryType,
    Testimonial,
    StoryCategory,
    Story,
    EventCategory,
    Event,
    ContactMessage,
)

admin.site.site_header = "Alhazawa Foundation Admin"
admin.site.site_title = "Alhazawa Admin"
admin.site.index_title = "Site Content"


class SingletonAdmin(admin.ModelAdmin):
    """For models that should only ever have one row (site settings, about, founder)."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


def thumb(field_name, label):
    """Build a small thumbnail-rendering callable for use directly inside a
    ModelAdmin's list_display tuple. Django calls list_display callables as
    func(obj) — a single argument, not a bound method — so this takes only
    `obj`."""

    def _thumb(obj):
        image = getattr(obj, field_name, None)
        if image:
            return format_html('<img src="{}" style="height:42px;border-radius:6px;object-fit:cover;">', image.url)
        return "—"

    _thumb.short_description = label
    return _thumb


@admin.register(GeneralInformation)
class GeneralInformationAdmin(SingletonAdmin):
    fieldsets = (
        ("Identity", {"fields": ("org_name", "founder_name", "logo", "logo2")}),
        ("Contact", {"fields": ("address", "email", "tel", "whatsapp", "website")}),
        ("Social Links", {"fields": ("facebook_url", "instagram_url", "twitter_url")}),
        ("Strategic Statements", {"fields": ("vision", "mission", "future_centre_intro", "future_centre_concept_image")}),
        ("Homepage Hero", {"fields": ("hero_image_main", "hero_image_float", "hero_badge_number", "hero_badge_label")}),
        ("Section Headings", {
            "fields": (
                "aboutHead", "causeHead", "whatHead", "donateHead", "donateContent",
                "teamHead", "testimonieHead", "contactHead", "contactContent", "pageHeaderImage",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(About)
class AboutAdmin(SingletonAdmin):
    list_display = ("title",)


@admin.register(FounderProfile)
class FounderProfileAdmin(SingletonAdmin):
    list_display = ("name", "role_title", thumb("image", "Photo"))


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "order", thumb("image", "Photo"))
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ("tag", "name", "short", "icon", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("name", "concept", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ("name", "note", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    list_display = ("name", "outcome", "icon", "order")
    list_editable = ("order",)
    ordering = ("order",)


class RoadmapActivityInline(admin.TabularInline):
    model = RoadmapActivity
    extra = 1


@admin.register(RoadmapStage)
class RoadmapStageAdmin(admin.ModelAdmin):
    list_display = ("term", "focus", "order")
    list_editable = ("order",)
    ordering = ("order",)
    inlines = [RoadmapActivityInline]


@admin.register(FutureCentreZone)
class FutureCentreZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(FuturePhase)
class FuturePhaseAdmin(admin.ModelAdmin):
    list_display = ("label", "title", "note", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(DayTimelineStep)
class DayTimelineStepAdmin(admin.ModelAdmin):
    list_display = ("time_label", "title", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (thumb("image", "Preview"), "caption", "category", "size_hint", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    ordering = ("order", "-id")


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ("caption", "category", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    ordering = ("order", "-id")


@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "goal", "raised", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(PartnerCategory)
class PartnerCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(InquiryType)
class InquiryTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", thumb("image", "Photo"))
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(StoryCategory)
class StoryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_sample", "is_featured", "order")
    list_editable = ("order",)
    list_filter = ("category", "is_sample", "is_featured")
    search_fields = ("title", "excerpt")
    ordering = ("order", "-id")


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "event_date", "date_label", "is_sample", "order")
    list_editable = ("order",)
    list_filter = ("category", "is_sample")
    ordering = ("order", "-id")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "inquiry_type", "email", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "inquiry_type", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "inquiry_type", "created_at")
    ordering = ("-created_at",)
