"""
Alhazawa Orphans & Girl Child Foundation — content models.

Every piece of content rendered on the public site lives in a model here,
registered in admin.py, so the Foundation can edit the entire site from
Django admin without ever touching code. Models with an `order` field are
sorted by it in the admin (drag-free — just type a number) and on the
front end.
"""

from django.db import models


# ---------------------------------------------------------------------------
# Site-wide settings (singleton) — replaces/extends the original
# GeneralInformation model. Only one row is ever expected to exist; the
# admin is configured to prevent adding a second.
# ---------------------------------------------------------------------------
class GeneralInformation(models.Model):
    # Organisation identity
    org_name = models.CharField(max_length=200, default="Alhazawa Orphans & Girl Child Foundation")
    founder_name = models.CharField(max_length=200, default="Prof. Mansir Dodo")
    logo = models.ImageField(upload_to="pictures", null=True, blank=True)
    logo2 = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Secondary/footer logo variant (optional).")

    # Contact
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    whatsapp = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)

    # Social links — leave blank to hide the icon on the front end
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)

    # Section headings (kept editable so wording can change without a dev)
    aboutHead = models.CharField(max_length=200, null=True, blank=True)
    causeHead = models.CharField(max_length=200, null=True, blank=True)
    whatHead = models.CharField(max_length=200, null=True, blank=True)
    donateHead = models.CharField(max_length=200, null=True, blank=True)
    donateContent = models.TextField(null=True, blank=True)
    teamHead = models.CharField(max_length=200, null=True, blank=True)
    testimonieHead = models.CharField(max_length=200, null=True, blank=True)
    contactHead = models.CharField(max_length=200, null=True, blank=True)
    contactContent = models.TextField(null=True, blank=True)
    pageHeaderImage = models.ImageField(upload_to="pictures", null=True, blank=True)
    hero_image_main = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Large hero photo on the homepage.")
    hero_image_float = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Small floating photo overlapping the main hero photo.")
    hero_badge_number = models.CharField(max_length=10, null=True, blank=True, default="4", help_text="Number shown in the floating hero badge.")
    hero_badge_label = models.CharField(max_length=100, null=True, blank=True, default="Strategic Focus Areas", help_text="Label shown under the hero badge number.")
    problem_section_image = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Photo or map shown next to \"The Challenge\" section on the homepage (Malumfashi/Katsina panel). Leave blank to use the default abstract graphic.")

    # Strategic statements (one of each — from the Foundation's Strategic Plan)
    vision = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    future_centre_intro = models.TextField(null=True, blank=True, help_text="Intro paragraph for the Future Centre page/section.")
    future_centre_concept_image = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Whole-site conceptual render for the top of the Future Centre page.")

    class Meta:
        verbose_name = "General Information"
        verbose_name_plural = "General Information"

    def __str__(self):
        return self.org_name or "General Information"


# ---------------------------------------------------------------------------
# About section (singleton-style, same shape as before)
# ---------------------------------------------------------------------------
class About(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    image1 = models.ImageField(upload_to="pictures", null=True, blank=True)
    image2 = models.ImageField(upload_to="pictures", null=True, blank=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return self.title or "About"


# ---------------------------------------------------------------------------
# Founder profile (singleton) — the real welcome message + founder photo
# ---------------------------------------------------------------------------
class FounderProfile(models.Model):
    name = models.CharField(max_length=200, default="Prof. Mansir Dodo")
    role_title = models.CharField(max_length=200, default="Founder & Visionary")
    bio = models.TextField(help_text="The founder's welcome / profile message.")
    quote = models.CharField(max_length=300, null=True, blank=True, help_text="Optional short signature line, e.g. '— Prof. Mansir Dodo, Founder'.")
    image = models.ImageField(upload_to="pictures", null=True, blank=True)

    class Meta:
        verbose_name = "Founder Profile"
        verbose_name_plural = "Founder Profile"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Governance / board members (was "Trustee")
# ---------------------------------------------------------------------------
class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Team / Board Member"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Strategic pillars — "Our Four Strategic Pillars"
# ---------------------------------------------------------------------------
class Pillar(models.Model):
    ICON_CHOICES = [
        ("book", "Book (Education)"),
        ("shield", "Shield (Welfare/Protection)"),
        ("spark", "Spark (Empowerment)"),
        ("hands", "Hands (Community)"),
        ("bowl", "Bowl (Feeding)"),
        ("tool", "Tool (Skills)"),
    ]
    tag = models.CharField(max_length=10, help_text="Short display tag, e.g. '01'.")
    name = models.CharField(max_length=200)
    short = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="book")
    image = models.ImageField(upload_to="pictures", null=True, blank=True, help_text="Representative photo for this pillar on the Programs page.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Core values
# ---------------------------------------------------------------------------
class CoreValue(models.Model):
    name = models.CharField(max_length=100)
    concept = models.CharField(max_length=100, null=True, blank=True, help_text="e.g. 'Raḥmah' — leave blank if none.")
    description = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Beneficiary groups — "Who We Serve"
# ---------------------------------------------------------------------------
class Beneficiary(models.Model):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=100, help_text="e.g. 'Primary beneficiaries'.")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Pilot programs
# ---------------------------------------------------------------------------
class Pilot(models.Model):
    ICON_CHOICES = Pillar.ICON_CHOICES
    name = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.CharField(max_length=300, help_text="Intended outcome, one sentence.")
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="book")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Roadmap — short term vs mid/long term
# ---------------------------------------------------------------------------
class RoadmapStage(models.Model):
    term = models.CharField(max_length=100, help_text="e.g. 'Short Term'.")
    focus = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.term


class RoadmapActivity(models.Model):
    stage = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE, related_name="activities")
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Roadmap Activities"

    def __str__(self):
        return self.text


# ---------------------------------------------------------------------------
# Future Centre
# ---------------------------------------------------------------------------
class FutureCentreZone(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class FuturePhase(models.Model):
    label = models.CharField(max_length=50, help_text="e.g. 'Phase 01'.")
    title = models.CharField(max_length=200)
    note = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label} — {self.title}"


# ---------------------------------------------------------------------------
# "A Day With The Foundation" timeline
# ---------------------------------------------------------------------------
class DayTimelineStep(models.Model):
    time_label = models.CharField(max_length=50, help_text="e.g. 'Arrival'.")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.time_label} — {self.title}"


# ---------------------------------------------------------------------------
# Gallery — categories + real photos/videos
# ---------------------------------------------------------------------------
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True, help_text="Optional short description shown alongside this category.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class Gallery(models.Model):
    SIZE_CHOICES = [("wide", "Wide"), ("tall", "Tall"), ("square", "Square")]
    image = models.ImageField(upload_to="pictures", null=True)
    caption = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="images")
    size_hint = models.CharField(max_length=10, choices=SIZE_CHOICES, default="square", help_text="Controls masonry layout sizing on the front end.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.caption or f"Gallery image #{self.pk}"


class GalleryVideo(models.Model):
    video = models.FileField(upload_to="videos", null=True)
    caption = models.CharField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="videos")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.caption or f"Gallery video #{self.pk}"


# ---------------------------------------------------------------------------
# Donation focus areas — replaces FeatureCause. goal/raised are optional;
# a progress bar only renders on the front end once real figures exist.
# ---------------------------------------------------------------------------
class DonationArea(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    goal = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank until a real fundraising goal is set.")
    raised = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank until real figures are available.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    def percentage(self):
        if not self.goal:
            return None
        return round((self.raised or 0) / self.goal * 100)


# ---------------------------------------------------------------------------
# Partnership categories & contact-form inquiry types — tiny lookup models
# so even these lists are admin-editable, not hardcoded.
# ---------------------------------------------------------------------------
class PartnerCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Partner Categories"

    def __str__(self):
        return self.name


class InquiryType(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Testimonials — starts empty (old data was unfilled template placeholder)
# ---------------------------------------------------------------------------
class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, null=True, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Stories / News
# ---------------------------------------------------------------------------
class StoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Story Categories"

    def __str__(self):
        return self.name


class Story(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(StoryCategory, on_delete=models.SET_NULL, null=True, related_name="stories")
    excerpt = models.TextField()
    body = models.TextField(null=True, blank=True, help_text="Optional full article body.")
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    date_label = models.CharField(max_length=100, null=True, blank=True, help_text="e.g. a real date, or 'Sample story — placeholder'.")
    is_sample = models.BooleanField(default=False, help_text="Marks this as illustrative placeholder content on the front end.")
    is_featured = models.BooleanField(default=False, help_text="Show as the large featured story at the top of the Stories page.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------
class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name="events")
    description = models.TextField()
    event_date = models.DateField(null=True, blank=True, help_text="Leave blank if not yet scheduled.")
    date_label = models.CharField(max_length=150, null=True, blank=True, help_text="Shown instead of event_date if that's blank, e.g. 'Date to be announced'.")
    is_sample = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Contact form submissions — a real inbox now that there's a real backend
# ---------------------------------------------------------------------------
class ContactMessage(models.Model):
    inquiry_type = models.ForeignKey(InquiryType, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject}"
