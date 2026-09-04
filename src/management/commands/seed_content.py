"""
One-time content seed for the merged Alhazawa site.

Run once, right after migrating: `python manage.py seed_content`

- Fills in GeneralInformation / FounderProfile with real content recovered
  from the live site's old Paragraph/About rows (captured before those
  tables were removed) plus the corrected contact details.
- Re-creates the 3 real trustees as TeamMember rows, pointing at the same
  already-uploaded photo files.
- Categorizes and re-captions the 13 real (previously untagged) Gallery
  photos and 2 GalleryVideo rows.
- Populates every new content model (pillars, values, beneficiaries,
  pilots, roadmap, Future Centre, day timeline, donation areas, partner
  categories, inquiry types) from the Foundation's Strategic Plan.
- Seeds 4 clearly-flagged sample Stories and 4 sample Events so those
  pages aren't empty on launch — real content can replace them in admin
  at any time.

Safe to re-run: every step uses get_or_create / update_or_create keyed on
a natural identifier, so running this twice does not duplicate rows.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from src.models import (
    GeneralInformation,
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
    StoryCategory,
    Story,
    EventCategory,
    Event,
)


class Command(BaseCommand):
    help = "Seed the merged Alhazawa site with real + strategic-plan content."

    @transaction.atomic
    def handle(self, *args, **options):
        self.seed_general_information()
        self.seed_founder()
        self.seed_team()
        self.seed_pillars()
        self.seed_values()
        self.seed_beneficiaries()
        self.seed_pilots()
        self.seed_roadmap()
        self.seed_future_centre()
        self.seed_day_timeline()
        self.seed_gallery_categories_and_recategorize()
        self.seed_new_photos_september()
        self.seed_donation_areas()
        self.seed_partner_categories()
        self.seed_inquiry_types()
        self.seed_stories()
        self.seed_events()
        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    # ------------------------------------------------------------------
    def seed_general_information(self):
        g, _ = GeneralInformation.objects.get_or_create(pk=1)
        g.org_name = "Alhazawa Orphans & Girl Child Foundation"
        g.founder_name = "Prof. Mansir Dodo"
        g.address = "64 Galadima Tunau Road, Gangarawa, Alhazawa, Malumfashi, Katsina State, Nigeria"
        g.email = "info@alhazawaogcf.com.ng"
        g.tel = "+234 806 566 6829"
        g.whatsapp = "+234 806 566 6829"
        g.website = "www.alhazawaogcf.com.ng"
        g.vision = (
            "To nurture a generation of morally upright, educated, and self-reliant orphans "
            "and girls who contribute positively to society, guided by Islamic values and "
            "human dignity."
        )
        g.mission = (
            "To provide holistic care, quality education, moral upbringing, and sustainable "
            "empowerment for orphans and the girl-child through structured programs, "
            "accountable governance, and community-centered partnerships."
        )
        g.future_centre_intro = (
            "The Foundation's Strategic Plan proposes a purpose-built Centre — developed on "
            "an identified site in Alhazawa — bringing education, skills training and "
            "institutional coordination under one roof. This is a development vision, phased "
            "in line with available resources and strategic priorities; it has not yet been "
            "constructed."
        )
        if not g.logo:
            g.logo.name = "pictures/alhazawa-logo-transparent.png"
        if not g.hero_image_main:
            g.hero_image_main.name = "pictures/seed-hero-main.jpg"
        if not g.hero_image_float:
            g.hero_image_float.name = "pictures/seed-hero-float.jpg"
        if not g.future_centre_concept_image:
            g.future_centre_concept_image.name = "pictures/seed-future-centre-concept.jpg"
        g.hero_badge_number = "4"
        g.hero_badge_label = "Strategic Focus Areas"
        g.aboutHead = g.aboutHead or "Why We Exist"
        g.causeHead = g.causeHead or "Where Your Gift Goes"
        g.whatHead = g.whatHead or "Our Four Strategic Pillars"
        g.donateHead = g.donateHead or "Your Support Can Become Someone's Future"
        g.teamHead = g.teamHead or "Governance"
        g.contactHead = g.contactHead or "Let's Talk About What's Possible"
        g.bank_name = g.bank_name or "Bank Name (to be confirmed)"
        g.bank_account_name = g.bank_account_name or "Alhazawa Orphans & Girl Child Foundation"
        g.bank_account_number = g.bank_account_number or "XXXX XXXX XXXX"
        g.save()
        self.stdout.write("GeneralInformation seeded.")

    # ------------------------------------------------------------------
    def seed_founder(self):
        founder, _ = FounderProfile.objects.get_or_create(pk=1)
        founder.name = "Prof. Mansir Dodo"
        founder.role_title = "Founder & Visionary"
        founder.bio = (
            "Welcome to Alhazawa Orphans and Girl Child Foundation.\n\n"
            "It is with a heart full of gratitude and hope that I welcome you to this space "
            "dedicated to compassion, empowerment, and transformation. At Alhazawa Foundation, "
            "we are deeply committed to restoring hope and dignity to orphans and vulnerable "
            "girls by providing them with access to education, healthcare, shelter, and "
            "emotional support.\n\n"
            "Our journey is rooted in the belief that every child, regardless of background or "
            "circumstance, deserves a chance to dream, grow, and succeed. Through the generous "
            "support of individuals and partners like you, we are creating opportunities that "
            "change lives and break the cycle of poverty and neglect.\n\n"
            "I invite you to walk with us on this noble path. Whether you are here to support, "
            "volunteer, or simply learn more, your presence means everything. Together, we can "
            "build a brighter and more inclusive future, one child at a time."
        )
        founder.quote = "— Prof. Mansir Dodo, Founder"
        if not founder.image:
            founder.image.name = "pictures/seed-founder-photo.jpg"
        founder.save()
        self.stdout.write("FounderProfile seeded.")

    # ------------------------------------------------------------------
    def seed_team(self):
        members = [
            ("Abdulmalik Dahiru", "Chairman", "pictures/WhatsApp_Image_2023-04-12_at_1.55.24_PM_QAtbXE5.jpeg", 1),
            ("Amina Abdallah", "Vice Chairman", "pictures/WhatsApp_Image_2023-04-12_at_1.25.11_PM.jpeg", 2),
            ("Hassan Abdulsalam", "Secretary General", "pictures/WhatsApp_Image_2023-04-12_at_1.24.34_PM.jpeg", 3),
        ]
        for name, designation, image_path, order in members:
            member, _ = TeamMember.objects.get_or_create(name=name, defaults={"designation": designation, "order": order})
            member.designation = designation
            member.order = order
            if not member.image:
                member.image.name = image_path
            member.save()
        self.stdout.write("Team members seeded.")

    # ------------------------------------------------------------------
    def seed_pillars(self):
        data = [
            ("01", "Education Support", "Academic assistance & learning continuity",
             "Provision of academic assistance, learning materials, and structured learning programs aimed at improving access to education, school retention, and academic performance.",
             "book", "pictures/seed-hero-float.jpg"),
            ("02", "Welfare, Care & Protection", "Basic needs, health and protective care",
             "Support for basic needs including access to clean water through boreholes, feeding, safe shelter, health referrals, sanitation, and psychosocial care to ensure a stable, healthy, and protective environment for beneficiaries.",
             "shield", "pictures/seed-feeding-session.jpg"),
            ("03", "Girl-Child Empowerment", "Life skills, mentorship & confidence",
             "Life-skills development, moral guidance, mentorship, and confidence-building initiatives designed to prepare girls for responsible and productive futures.",
             "spark", "pictures/seed-founder-photo.jpg"),
            ("04", "Community Engagement & Advocacy", "Partnership, ownership & advocacy",
             "Collaboration with families, community leaders, and partners to promote girls' education, child protection, and sustainable community ownership.",
             "hands", "pictures/seed-learning-table.jpg"),
        ]
        for i, (tag, name, short, desc, icon, image_path) in enumerate(data):
            p, _ = Pillar.objects.get_or_create(name=name, defaults={"tag": tag, "short": short, "description": desc, "icon": icon, "order": i})
            p.tag, p.short, p.description, p.icon, p.order = tag, short, desc, icon, i
            if not p.image:
                p.image.name = image_path
            p.save()
        self.stdout.write("Pillars seeded.")

    # ------------------------------------------------------------------
    def seed_values(self):
        data = [
            ("Compassion", "Raḥmah", "Serving with mercy and empathy."),
            ("Dignity", None, "Upholding the worth of every child."),
            ("Integrity", None, "Transparency, accountability, and trust."),
            ("Excellence", "Iḥsān", "Continuous improvement in service delivery."),
            ("Sustainability", None, "Long-term impact over short-term relief."),
        ]
        for i, (name, concept, desc) in enumerate(data):
            v, _ = CoreValue.objects.get_or_create(name=name, defaults={"concept": concept, "description": desc, "order": i})
            v.concept, v.description, v.order = concept, desc, i
            v.save()
        self.stdout.write("Core values seeded.")

    # ------------------------------------------------------------------
    def seed_beneficiaries(self):
        data = [
            ("Orphaned Children", "Primary beneficiaries", "The primary beneficiaries are orphaned children from disadvantaged backgrounds in underserved communities of Northern Nigeria."),
            ("Vulnerable Girls", "Primary beneficiaries", "Girls from disadvantaged backgrounds who benefit from life-skills development, moral guidance, mentorship, and confidence-building initiatives."),
            ("Caregivers & Families", "Secondary beneficiaries", "Caregivers and families who share in the support, guidance and community-centered partnerships that surround each child."),
            ("Host Communities", "Secondary beneficiaries", "Host communities engaged through advocacy and collaboration to promote girls' education, child protection, and sustainable community ownership."),
        ]
        for i, (name, note, desc) in enumerate(data):
            b, _ = Beneficiary.objects.get_or_create(name=name, defaults={"note": note, "description": desc, "order": i})
            b.note, b.description, b.order = note, desc, i
            b.save()
        self.stdout.write("Beneficiaries seeded.")

    # ------------------------------------------------------------------
    def seed_pilots(self):
        data = [
            ("Education Support Pilot", "Provision of school materials, holiday and after-school lessons, and targeted academic support for orphans and vulnerable girls to improve learning outcomes and school retention.", "Improved learning outcomes and stronger school retention.", "book"),
            ("Feeding & Welfare Support Pilot", "Implementation of a structured feeding program and basic welfare support to improve nutrition, health, and learning readiness among beneficiaries.", "Better nutrition, health and readiness to learn.", "bowl"),
            ("Girl-Child Empowerment Pilot", "Delivery of life-skills training, mentorship sessions, and moral development activities aimed at building confidence, resilience, and positive life choices for girls.", "Greater confidence, resilience and positive life choices.", "spark"),
            ("Skills & Community Engagement Pilot", "Introduction of basic vocational, entrepreneurial, or practical skills training alongside community sensitization activities to encourage local participation and support.", "Stronger local participation and practical skill-building.", "tool"),
        ]
        for i, (name, desc, outcome, icon) in enumerate(data):
            p, _ = Pilot.objects.get_or_create(name=name, defaults={"description": desc, "outcome": outcome, "icon": icon, "order": i})
            p.description, p.outcome, p.icon, p.order = desc, outcome, icon, i
            p.save()
        self.stdout.write("Pilots seeded.")

    # ------------------------------------------------------------------
    def seed_roadmap(self):
        short, _ = RoadmapStage.objects.get_or_create(term="Short Term", defaults={"focus": "Education & Welfare Support", "order": 0})
        short.focus, short.order = "Education & Welfare Support", 0
        short.save()
        for i, text in enumerate([
            "Long vacation academic lessons for orphans and vulnerable girls",
            "Feeding programme during lesson periods",
        ]):
            RoadmapActivity.objects.get_or_create(stage=short, text=text, defaults={"order": i})

        long_term, _ = RoadmapStage.objects.get_or_create(term="Mid to Long Term", defaults={"focus": "Institutional & Program Development", "order": 1})
        long_term.focus, long_term.order = "Institutional & Program Development", 1
        long_term.save()
        for i, text in enumerate([
            "Establishment of a standard school",
            "Development of a skills acquisition centre",
            "Construction of the Foundation's head office",
            "Expansion of education, welfare, and empowerment programmes",
        ]):
            RoadmapActivity.objects.get_or_create(stage=long_term, text=text, defaults={"order": i})
        self.stdout.write("Roadmap seeded.")

    # ------------------------------------------------------------------
    def seed_future_centre(self):
        zones = [
            ("Standard School", "Classrooms and basic learning facilities designed to provide quality education for orphans and vulnerable girls, with provision for future expansion.", "pictures/seed-hero-main.jpg"),
            ("Skills Acquisition Centre", "Dedicated spaces for vocational, entrepreneurial, and life-skills training aimed at empowering beneficiaries with practical skills for self-reliance.", "pictures/seed-future-centre-concept.jpg"),
            ("Foundation Head Office", "The administrative head office, supporting coordination, governance, and efficient management of the Foundation's programs and partnerships.", None),
        ]
        for i, (name, desc, image_path) in enumerate(zones):
            z, _ = FutureCentreZone.objects.get_or_create(name=name, defaults={"description": desc, "order": i})
            z.description, z.order = desc, i
            if image_path and not z.image:
                z.image.name = image_path
            z.save()

        phases = [
            ("Phase 01", "Education & Welfare", "Underway — long vacation lessons and feeding support for beneficiaries."),
            ("Phase 02", "School Development", "Planned — establishment of the standard school."),
            ("Phase 03", "Skills Centre", "Planned — development of the skills acquisition centre."),
            ("Phase 04", "Institutional Expansion", "Planned — Foundation head office and expanded programming."),
        ]
        for i, (label, title, note) in enumerate(phases):
            ph, _ = FuturePhase.objects.get_or_create(label=label, defaults={"title": title, "note": note, "order": i})
            ph.title, ph.note, ph.order = title, note, i
            ph.save()
        self.stdout.write("Future Centre seeded.")

    # ------------------------------------------------------------------
    def seed_day_timeline(self):
        data = [
            ("Arrival", "Children Arrive", "Beneficiaries gather at the lesson site for the day's academic session."),
            ("Learning", "Academic Lessons", "Structured lessons — including core subjects such as mathematics — delivered by Foundation volunteers and the founder."),
            ("Mentorship", "Guidance & Mentorship", "Moral guidance and confidence-building conversations, especially for girl beneficiaries."),
            ("Feeding", "Feeding Session", "A shared meal supporting nutrition and learning readiness during the lesson period."),
            ("Community", "Community & Materials", "Distribution of learning materials and engagement with caregivers and community members."),
        ]
        for i, (time_label, title, desc) in enumerate(data):
            t, _ = DayTimelineStep.objects.get_or_create(time_label=time_label, defaults={"title": title, "description": desc, "order": i})
            t.title, t.description, t.order = title, desc, i
            t.save()
        self.stdout.write("Day timeline seeded.")

    # ------------------------------------------------------------------
    def seed_gallery_categories_and_recategorize(self):
        categories = {
            "Education": "Structured lessons, including long vacation academic support that keeps learning going through the school break.",
            "Feeding": "A shared meal alongside every lesson period, supporting nutrition and learning readiness.",
            "Learning Materials": "Books, writing boards and school supplies distributed directly to beneficiaries.",
            "Girl-Child Support": "Mentorship, guidance and direct engagement with girl beneficiaries.",
            "Community": "Families, volunteers, staff and community leaders taking part alongside beneficiaries.",
            "Recognition": "Beneficiaries recognized for effort and achievement.",
        }
        cats = {}
        for i, (name, desc) in enumerate(categories.items()):
            c, _ = GalleryCategory.objects.get_or_create(name=name, defaults={"description": desc, "order": i})
            c.description, c.order = desc, i
            c.save()
            cats[name] = c

        # (filename fragment, category name, size hint, new caption)
        photo_updates = [
            ("5.36.31_PM", "Education", "wide", "Beneficiaries work through a long vacation lesson together."),
            ("5.36.30_PM", "Learning Materials", "wide", "Learning materials distributed directly to beneficiaries."),
            ("5.36.25_PM", "Learning Materials", "wide", "New textbooks handed out to beneficiaries in the classroom."),
            ("5.28.27_PM", "Community", "wide", "Community members and beneficiaries gather for a distribution event."),
            ("5.29.42_PM", "Recognition", "tall", "A beneficiary recognized for outstanding academic performance."),
            ("08.46.37_1e331f8c", "Community", "wide", "Beneficiaries and Foundation volunteers together during a programme session."),
            ("08.46.37_671c3065", "Community", "wide", "A group moment with beneficiaries and Foundation staff."),
            ("08.46.36_96e4d568", "Education", "wide", "A classroom lesson in session, mats and lap-desks standing in for furniture."),
            ("08.46.35_e9da5221", "Learning Materials", "tall", "A beneficiary shows the writing board provided to support his lessons."),
            ("08.46.35_307d2fb4", "Community", "wide", "Foundation representatives and community members with beneficiaries."),
            ("08.46.34_bfb9649f", "Community", "wide", "Beneficiaries and Foundation staff gather for a group photograph."),
            ("16.28.47_dac9c5a5", "Learning Materials", "tall", "A beneficiary receives learning materials directly from a Foundation representative."),
            ("16.28.46_f9ebe4ad", "Learning Materials", "tall", "A young beneficiary receives his learning materials package."),
        ]
        order = 0
        for fragment, cat_name, size_hint, caption in photo_updates:
            gallery_item = Gallery.objects.filter(image__icontains=fragment).first()
            if gallery_item:
                gallery_item.category = cats[cat_name]
                gallery_item.size_hint = size_hint
                gallery_item.caption = caption
                gallery_item.order = order
                gallery_item.save()
                order += 1
            else:
                self.stdout.write(self.style.WARNING(f"Gallery photo matching '{fragment}' not found — skipped."))

        video_updates = [
            ("ee092f13", "Community", "A message of appreciation from the Alhazawa community."),
            ("08bcf59e", "Education", "Long vacation lessons, captured on video."),
        ]
        for fragment, cat_name, caption in video_updates:
            video_item = GalleryVideo.objects.filter(video__icontains=fragment).first()
            if video_item:
                video_item.category = cats[cat_name]
                video_item.caption = caption
                video_item.save()
            else:
                self.stdout.write(self.style.WARNING(f"Gallery video matching '{fragment}' not found — skipped."))

        self.stdout.write("Gallery categorized.")

    # ------------------------------------------------------------------
    def seed_new_photos_september(self):
        """21 real photos added after the initial launch — more lesson
        sessions, feeding, materials distribution, and one striking
        portrait. Filenames already live in media/pictures/."""
        cats = {c.name: c for c in GalleryCategory.objects.all()}

        photos = [
            ("new-lesson-mixed-mat.jpg", "Education", "wide", "Beneficiaries settle into a lesson, lap-desks and notebooks out."),
            ("new-feeding-snack-1.jpg", "Feeding", "wide", "A shared snack break during a lesson session."),
            ("new-lesson-lapdesks-1.jpg", "Education", "wide", "A full classroom of lap-desks, heads down and writing."),
            ("new-lesson-closeup.jpg", "Education", "wide", "Beneficiaries focused on their lesson."),
            ("new-community-group.jpg", "Community", "wide", "Foundation staff and volunteers pictured with beneficiaries."),
            ("new-feeding-snack-2.jpg", "Feeding", "wide", "Bread and a drink — a feeding session in progress."),
            ("new-lesson-lapdesks-2.jpg", "Education", "wide", "Beneficiaries at their lap-desks along the classroom wall."),
            ("new-lesson-wideroom.jpg", "Education", "wide", "A lesson spans the length of the room."),
            ("new-lesson-orangemat.jpg", "Education", "wide", "Beneficiaries write together on a woven mat."),
            ("new-maths-lesson.jpg", "Learning Materials", "tall", "A mathematics lesson on open sentences, addition and subtraction."),
            ("new-lesson-redtable-1.jpg", "Education", "wide", "A mixed-age group at lesson, mats and a shared table."),
            ("new-lesson-redtable-2.jpg", "Education", "wide", "Beneficiaries writing at a shared table."),
            ("new-lesson-lapdesks-3.jpg", "Education", "wide", "A classroom lesson in session, lap-desks along the wall."),
            ("new-lesson-reading.jpg", "Education", "tall", "A beneficiary reads quietly during a lesson."),
            ("new-lesson-redtable-3.jpg", "Education", "wide", "Beneficiaries at their books during a lesson session."),
            ("new-materials-boards-1.jpg", "Learning Materials", "wide", "Beneficiaries proudly hold up their new writing boards."),
            ("new-materials-boards-2.jpg", "Learning Materials", "wide", "New learning boards distributed to beneficiaries."),
            ("new-community-waiting.jpg", "Community", "wide", "Younger beneficiaries gather before the day's session begins."),
            ("new-lesson-tealmat-1.jpg", "Education", "wide", "Beneficiaries settle in for a lesson, shoes left at the mat's edge."),
            ("new-lesson-tealmat-2.jpg", "Education", "wide", "A lesson in session on the woven mat."),
            ("new-portrait-writingslate.jpg", "Education", "tall", "A beneficiary holds his Qur'anic writing slate — tradition and learning side by side."),
        ]

        start_order = Gallery.objects.count()
        for i, (filename, cat_name, size_hint, caption) in enumerate(photos):
            image_path = f"pictures/{filename}"
            item, created = Gallery.objects.get_or_create(
                image=image_path,
                defaults={
                    "category": cats.get(cat_name),
                    "size_hint": size_hint,
                    "caption": caption,
                    "order": start_order + i,
                },
            )
            if not created:
                item.category = cats.get(cat_name)
                item.size_hint = size_hint
                item.caption = caption
                item.save()

        self.stdout.write(f"{len(photos)} new photos seeded into the gallery.")

    # ------------------------------------------------------------------
    def seed_donation_areas(self):
        data = [
            ("Education Support", "School materials, holiday lessons and academic support."),
            ("Feeding", "Structured feeding during lesson periods."),
            ("Learning Materials", "Books, stationery and classroom essentials."),
            ("Girl-Child Empowerment", "Mentorship, life-skills and confidence-building."),
            ("Future Centre", "Toward the proposed school, skills centre and head office."),
            ("General Support", "Where the need is greatest, at the Foundation's discretion."),
        ]
        for i, (name, desc) in enumerate(data):
            d, _ = DonationArea.objects.get_or_create(name=name, defaults={"description": desc, "order": i})
            d.description, d.order = desc, i
            d.save()
        self.stdout.write("Donation areas seeded.")

    # ------------------------------------------------------------------
    def seed_partner_categories(self):
        names = ["Individuals", "Corporate Organizations", "Foundations", "Development Partners",
                 "Government Institutions", "Community Leaders", "Volunteers", "Educational Institutions"]
        for i, name in enumerate(names):
            c, _ = PartnerCategory.objects.get_or_create(name=name, defaults={"order": i})
            c.order = i
            c.save()
        self.stdout.write("Partner categories seeded.")

    # ------------------------------------------------------------------
    def seed_inquiry_types(self):
        names = ["General Inquiry", "Donation", "Partnership", "Volunteering", "Program Support", "Media"]
        for i, name in enumerate(names):
            t, _ = InquiryType.objects.get_or_create(name=name, defaults={"order": i})
            t.order = i
            t.save()
        self.stdout.write("Inquiry types seeded.")

    # ------------------------------------------------------------------
    def seed_stories(self):
        cat_names = ["Foundation Stories", "Program Updates", "Girl-Child Programs", "Education Initiatives", "Community Stories", "Announcements"]
        cats = {}
        for i, name in enumerate(cat_names):
            c, _ = StoryCategory.objects.get_or_create(name=name, defaults={"order": i})
            cats[name] = c

        # A genuine lesson-in-progress photo (not the gift/materials handover
        # shots) — best fit for the "Long Vacation Lessons" featured story.
        long_vac_photo = Gallery.objects.filter(image__icontains="5.36.31_PM").first()

        data = [
            ("Long Vacation Lessons Bring Learning to Alhazawa", "Foundation Stories",
             "During the school break, the Foundation opened its doors for structured academic lessons — proof that a holiday need not mean a pause in learning.",
             long_vac_photo.image.name if long_vac_photo and long_vac_photo.image else "pictures/seed-hero-main.jpg",
             True, True),
            ("A Feeding Programme Rooted in Care", "Program Updates",
             "Alongside every lesson, a shared meal — because a child who is fed is a child who is ready to learn.",
             "pictures/seed-feeding-session.jpg", True, False),
            ("Dignity, Delivered by Hand", "Girl-Child Programs",
             "Founder Prof. Mansir Dodo continues to engage beneficiaries directly — a reminder that this Foundation's work is personal, not abstract.",
             "pictures/seed-founder-photo.jpg", True, False),
            ("Mathematics on a Half-Built Wall", "Education Initiatives",
             "A whiteboard, a marker, and unfinished blockwork — evidence that education at Alhazawa begins before the buildings are even complete.",
             "pictures/seed-hero-float.jpg", True, False),
        ]
        for i, (title, cat_name, excerpt, image_path, is_sample, is_featured) in enumerate(data):
            s, _ = Story.objects.get_or_create(title=title, defaults={
                "category": cats[cat_name], "excerpt": excerpt, "is_sample": is_sample,
                "is_featured": is_featured, "date_label": "Sample story — placeholder", "order": i,
            })
            s.category, s.excerpt, s.is_sample, s.is_featured, s.order = cats[cat_name], excerpt, is_sample, is_featured, i
            s.date_label = s.date_label or "Sample story — placeholder"
            if not s.image:
                s.image.name = image_path
            s.save()
        self.stdout.write("Stories seeded.")

    # ------------------------------------------------------------------
    def seed_events(self):
        cat_names = ["Educational Programs", "Community Outreach", "Girl-Child Programs", "Fundraising"]
        cats = {}
        for i, name in enumerate(cat_names):
            c, _ = EventCategory.objects.get_or_create(name=name, defaults={"order": i})
            cats[name] = c

        data = [
            ("Long Vacation Academic Lessons", "Educational Programs", "Structured holiday lessons for orphans and vulnerable girls.", "Recurring — school holiday periods"),
            ("Community Sensitization Session", "Community Outreach", "Engagement with families and community leaders on girls' education and child protection.", "Date to be announced"),
            ("Mentorship & Confidence Circle", "Girl-Child Programs", "Life-skills and moral development session for girl beneficiaries.", "Date to be announced"),
            ("Partnership & Giving Drive", "Fundraising", "A call to individuals, corporates and partners to support the Foundation's next phase.", "Date to be announced"),
        ]
        for i, (title, cat_name, desc, date_label) in enumerate(data):
            e, _ = Event.objects.get_or_create(title=title, defaults={
                "category": cats[cat_name], "description": desc, "date_label": date_label,
                "is_sample": True, "order": i,
            })
            e.category, e.description, e.date_label, e.is_sample, e.order = cats[cat_name], desc, date_label, True, i
            e.save()
        self.stdout.write("Events seeded.")
