/* ==========================================================================
   ALHAZAWA ORPHANS & GIRL CHILD FOUNDATION — main.js
   Navigation, interactions, content rendering from data.js, forms.
   Depends on: data.js (loaded first). Vanilla JS only.
   ========================================================================== */

(function () {
  "use strict";

  const $  = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));
  const D  = window.ALHAZAWA_DATA || {};

  document.addEventListener("DOMContentLoaded", () => {
    initHeader();
    initMobileMenu();
    initBackToTop();
    initCustomCursor();
    initMagneticButtons();
    initActiveNav();
    setYear();

    renderPillars();
    renderValues();
    renderBeneficiaries();
    renderPilots();
    renderRoadmap();
    renderFutureCentreZones();
    renderPhaseTrack();
    renderTimeline();
    renderDonationAreas();
    renderAmountSelector();
    renderPartners();
    renderEvents();
    renderContactChips();
    initHeroParticles();

    initContactForm();
    initDonateForm();
  });

  /* ----------------------------------------------------------------------
     Header: shrink + glass on scroll
     ---------------------------------------------------------------------- */
  function initHeader() {
    const header = $(".site-header");
    if (!header) return;
    const onScroll = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ----------------------------------------------------------------------
     Mobile menu
     ---------------------------------------------------------------------- */
  function initMobileMenu() {
    const toggle = $(".nav-toggle");
    const menu = $(".mobile-menu");
    if (!toggle || !menu) return;
    const close = () => { toggle.classList.remove("is-open"); menu.classList.remove("is-open"); document.body.style.overflow = ""; };
    toggle.addEventListener("click", () => {
      const open = toggle.classList.toggle("is-open");
      menu.classList.toggle("is-open", open);
      document.body.style.overflow = open ? "hidden" : "";
    });
    $$("a", menu).forEach((a) => a.addEventListener("click", close));
  }

  /* ----------------------------------------------------------------------
     Back to top
     ---------------------------------------------------------------------- */
  function initBackToTop() {
    const btn = $(".back-to-top");
    if (!btn) return;
    window.addEventListener("scroll", () => {
      btn.classList.toggle("is-visible", window.scrollY > 700);
    }, { passive: true });
    btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  /* ----------------------------------------------------------------------
     Subtle custom cursor (desktop, fine-pointer only)
     ---------------------------------------------------------------------- */
  function initCustomCursor() {
    const isFine = window.matchMedia("(pointer: fine)").matches;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!isFine || reduceMotion) return;

    const dot = document.createElement("div");
    const ring = document.createElement("div");
    dot.className = "cursor-dot";
    ring.className = "cursor-ring";
    document.body.append(dot, ring);
    // Deliberately not revealed until the first real mousemove — otherwise
    // the cursor elements sit visible at (0,0) before the pointer ever moves.

    let mx = 0, my = 0, rx = 0, ry = 0, hasMoved = false;
    window.addEventListener("mousemove", (e) => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate(${mx}px, ${my}px) translate(-50%,-50%)`;
      if (!hasMoved) {
        hasMoved = true;
        rx = mx; ry = my;
        document.documentElement.classList.add("has-custom-cursor");
      }
    });
    (function loop() {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%,-50%)`;
      requestAnimationFrame(loop);
    })();

    $$("a, button, .masonry-item, .value-card, .pillar-card, input, textarea, select").forEach((el) => {
      el.addEventListener("mouseenter", () => ring.classList.add("is-active"));
      el.addEventListener("mouseleave", () => ring.classList.remove("is-active"));
    });
  }

  /* ----------------------------------------------------------------------
     Magnetic buttons — subtle cursor-follow on primary/gold buttons
     ---------------------------------------------------------------------- */
  function initMagneticButtons() {
    const isFine = window.matchMedia("(pointer: fine)").matches;
    if (!isFine) return;
    $$(".btn-primary, .btn-gold, .btn-secondary").forEach((btn) => {
      btn.classList.add("magnetic");
      btn.addEventListener("mousemove", (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.18}px, ${y * 0.32}px)`;
      });
      btn.addEventListener("mouseleave", () => { btn.style.transform = ""; });
    });
  }

  /* ----------------------------------------------------------------------
     Active nav link based on current page filename
     ---------------------------------------------------------------------- */
  function initActiveNav() {
    const path = window.location.pathname.split("/").pop() || "index.html";
    $$(".nav-links a, .mobile-menu a").forEach((a) => {
      const href = a.getAttribute("href");
      if (href === path || (path === "" && href === "index.html")) a.classList.add("is-active");
    });
  }

  function setYear() {
    $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
  }

  /* ----------------------------------------------------------------------
     Icon set — small inline SVG library keyed by name
     ---------------------------------------------------------------------- */
  const ICONS = {
    book: '<path d="M4 5.5C4 4.7 4.7 4 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5v-13Z"/><path d="M20 5.5c0-.8-.7-1.5-1.5-1.5H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5v-13Z"/>',
    shield: '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3Z"/><path d="m9 12 2 2 4-4"/>',
    spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    hands: '<path d="M8 13V6a2 2 0 1 1 4 0v6"/><path d="M12 12V4a2 2 0 1 1 4 0v8"/><path d="M16 12.5V7a2 2 0 1 1 4 0v7c0 4-3 7-7 7s-6-2-8-5l-1.5-3a1.5 1.5 0 0 1 2.6-1.5L8 13"/>',
    bowl: '<path d="M3 12h18a9 6 0 0 1-18 0Z"/><path d="M8 12V7a4 4 0 0 1 8 0v5"/>',
    tool: '<path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 1 5.4-5.4L15 12l-2-2 1.7-1.7Z"/>',
    location: '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
    phone: '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2c-8 0-14-6-14-14a2 2 0 0 1 2-2Z"/>',
    mail: '<path d="M4 5h16v14H4z"/><path d="m4 6 8 7 8-7"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18Z"/>',
    check: '<path d="m5 13 4 4L19 7"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/>',
    arrowRight: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    chevLeft: '<path d="m15 6-6 6 6 6"/>',
    chevRight: '<path d="m9 6 6 6-6 6"/>',
    up: '<path d="M12 19V5M6 11l6-6 6 6"/>',
    fb: '<path d="M14 9h3V6h-3a3 3 0 0 0-3 3v2H9v3h2v6h3v-6h2.5l.5-3H14V9.5c0-.3.2-.5.5-.5Z"/>',
    ig: '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    tw: '<path d="M22 5.9a8 8 0 0 1-2.3.6 4 4 0 0 0 1.8-2.2 8 8 0 0 1-2.5 1 4 4 0 0 0-6.9 3.6A11.4 11.4 0 0 1 3.9 4.8a4 4 0 0 0 1.2 5.3 4 4 0 0 1-1.8-.5v.1a4 4 0 0 0 3.2 3.9 4 4 0 0 1-1.8.1 4 4 0 0 0 3.7 2.8A8 8 0 0 1 2 18.4a11.3 11.3 0 0 0 6.1 1.8c7.4 0 11.4-6.1 11.4-11.4v-.5A8 8 0 0 0 22 5.9Z"/>'
  };
  function icon(name) {
    return `<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ICONS.spark}</svg>`;
  }

  /* ----------------------------------------------------------------------
     Renderers — each is a no-op if its container isn't on the page
     ---------------------------------------------------------------------- */

  function renderPillars() {
    const root = $("[data-render='pillars']");
    if (!root || !D.pillars) return;
    root.innerHTML = D.pillars.map((p) => `
      <article class="pillar-card" data-reveal="up">
        <span class="p-tag">${p.tag}</span>
        <div class="p-icon">${icon(p.icon)}</div>
        <span class="p-short">${p.short}</span>
        <h3>${p.name}</h3>
        <p class="desc">${p.description}</p>
      </article>
    `).join("");
  }

  function renderValues() {
    const root = $("[data-render='values']");
    if (!root || !D.values) return;
    root.innerHTML = D.values.map((v) => `
      <article class="value-card" data-reveal="up">
        <div class="v-icon">${icon(v.id === "compassion" ? "hands" : v.id === "dignity" ? "shield" : v.id === "integrity" ? "check" : v.id === "excellence" ? "spark" : "globe")}</div>
        <h4>${v.name}</h4>
        ${v.concept ? `<span class="concept">${v.concept}</span>` : ""}
        <p>${v.description}</p>
      </article>
    `).join("");
  }

  function renderBeneficiaries() {
    const root = $("[data-render='beneficiaries']");
    if (!root || !D.beneficiaries) return;
    root.innerHTML = D.beneficiaries.map((b) => `
      <article class="beneficiary-card" data-reveal="up">
        <span class="note">${b.note}</span>
        <h4>${b.name}</h4>
        <p>${b.description}</p>
      </article>
    `).join("");
  }

  function renderPilots() {
    const root = $("[data-render='pilots']");
    if (!root || !D.pilots) return;
    root.innerHTML = D.pilots.map((p) => `
      <article class="pilot-card" data-reveal="up">
        <div class="pi-icon">${icon(p.icon)}</div>
        <div>
          <h4>${p.name}</h4>
          <p>${p.description}</p>
          <span class="outcome">Intended outcome: ${p.outcome}</span>
        </div>
      </article>
    `).join("");
  }

  function renderRoadmap() {
    const root = $("[data-render='roadmap']");
    if (!root || !D.roadmap) return;
    root.innerHTML = D.roadmap.map((r, i) => `
      <div class="roadmap-stage" data-reveal="up">
        <div class="r-dot">${i + 1}</div>
        <h4>${r.term}</h4>
        <span class="r-focus">${r.focus}</span>
        <ul>${r.activities.map((a) => `<li>${a}</li>`).join("")}</ul>
      </div>
    `).join("");
  }

  function renderFutureCentreZones() {
    const root = $("[data-render='zones']");
    if (!root || !D.futureCentre) return;
    root.innerHTML = D.futureCentre.zones.map((z, i) => `
      <article class="zone-card" data-reveal="up">
        <span class="z-num">0${i + 1}</span>
        <h4>${z.name}</h4>
        <p>${z.description}</p>
      </article>
    `).join("");
  }

  function renderPhaseTrack() {
    const root = $("[data-render='phases']");
    if (!root || !D.futureCentre) return;
    root.innerHTML = D.futureCentre.phases.map((p, i) => `
      <div class="phase-step${i === 0 ? " is-active" : ""}" data-reveal="up">
        <span class="label">${p.label}</span>
        <h5>${p.title}</h5>
        <p>${p.note}</p>
      </div>
    `).join("");
  }

  function renderTimeline() {
    const root = $("[data-render='timeline']");
    if (!root || !D.dayTimeline) return;
    root.innerHTML = D.dayTimeline.map((t) => `
      <div class="timeline-item" data-reveal="up">
        <span class="t-dot"></span>
        <span class="t-time">${t.time}</span>
        <h4>${t.title}</h4>
        <p>${t.description}</p>
      </div>
    `).join("");
  }

  function renderDonationAreas() {
    const root = $("[data-render='donation-areas']");
    if (!root || !D.donationAreas) return;
    root.innerHTML = D.donationAreas.map((a, i) => `
      <button type="button" class="donation-card${i === 0 ? " is-selected" : ""}" data-area="${a.id}" data-reveal="up">
        <h4>${a.name}</h4>
        <p>${a.description}</p>
      </button>
    `).join("");
    $$(".donation-card", root).forEach((card) => {
      card.addEventListener("click", () => {
        $$(".donation-card", root).forEach((c) => c.classList.remove("is-selected"));
        card.classList.add("is-selected");
        updateDonateSummary();
      });
    });
  }

  function renderAmountSelector() {
    const root = $("[data-render='amounts']");
    if (!root || !D.donationAmounts) return;
    const chips = D.donationAmounts.map((amt, i) => `
      <button type="button" class="amount-chip${i === 1 ? " is-selected" : ""}" data-amount="${amt}">₦${amt.toLocaleString()}</button>
    `).join("");
    root.innerHTML = chips + `
      <label class="amount-custom"><span>₦</span><input type="number" min="0" step="500" placeholder="Custom amount" data-custom-amount></label>
    `;
    $$(".amount-chip", root).forEach((chip) => {
      chip.addEventListener("click", () => {
        $$(".amount-chip", root).forEach((c) => c.classList.remove("is-selected"));
        chip.classList.add("is-selected");
        const custom = $("[data-custom-amount]", root);
        if (custom) custom.value = "";
        updateDonateSummary();
      });
    });
    const custom = $("[data-custom-amount]", root);
    if (custom) custom.addEventListener("input", () => {
      $$(".amount-chip", root).forEach((c) => c.classList.remove("is-selected"));
      updateDonateSummary();
    });
  }

  function updateDonateSummary() {
    const summary = $("[data-donate-summary]");
    if (!summary) return;
    const selectedArea = $(".donation-card.is-selected h4");
    const custom = $("[data-custom-amount]");
    const selectedChip = $(".amount-chip.is-selected");
    let amount = "";
    if (custom && custom.value) amount = `₦${Number(custom.value).toLocaleString()}`;
    else if (selectedChip) amount = selectedChip.textContent;
    $("[data-summary-area]", summary).textContent = selectedArea ? selectedArea.textContent : "General Support";
    $("[data-summary-amount]", summary).textContent = amount || "Select an amount";
  }

  function renderPartners() {
    const root = $("[data-render='partners']");
    if (!root || !D.partnerCategories) return;
    root.innerHTML = D.partnerCategories.map((p) => `<div class="partner-chip" data-reveal="up">${p}</div>`).join("");
  }

  function renderEvents() {
    const root = $("[data-render='events']");
    if (!root || !D.events) return;
    root.innerHTML = D.events.map((e) => `
      <article class="event-card" data-reveal="up">
        <div class="e-date">${icon("calendar")}</div>
        <div>
          ${e.sample ? '<span class="sample-flag">Sample</span>' : ""}
          <span class="e-cat">${e.category}</span>
          <h4>${e.title}</h4>
          <p class="e-desc">${e.description}</p>
          <span class="e-when">${e.dateLabel}</span>
        </div>
      </article>
    `).join("");
  }

  function renderContactChips() {
    const root = $("[data-render='inquiry-chips']");
    if (!root || !D.inquiryTypes) return;
    root.innerHTML = D.inquiryTypes.map((t, i) => `
      <label><input type="radio" name="inquiryType" value="${t}" ${i === 0 ? "checked" : ""}><span>${t}</span></label>
    `).join("");
  }

  /* ----------------------------------------------------------------------
     Hero floating particles (decorative)
     ---------------------------------------------------------------------- */
  function initHeroParticles() {
    const root = $("[data-particles]");
    if (!root) return;
    const count = 10;
    for (let i = 0; i < count; i++) {
      const p = document.createElement("i");
      p.style.left = Math.random() * 100 + "%";
      p.style.top = Math.random() * 100 + "%";
      p.style.animationDelay = (Math.random() * 6) + "s";
      p.style.animationDuration = (7 + Math.random() * 5) + "s";
      root.appendChild(p);
    }
  }

  /* ----------------------------------------------------------------------
     Contact form — static-site friendly: no real submission, honest
     success state, per project content rules.
     ---------------------------------------------------------------------- */
  function initContactForm() {
    const form = $("#contact-form");
    if (!form) return;
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      form.style.display = "none";
      const success = $("#contact-success");
      if (success) success.classList.add("is-visible");
    });
  }

  function initDonateForm() {
    const form = $("#donate-form");
    if (!form) return;
    updateDonateSummary();
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const note = $("#donate-note");
      if (note) note.hidden = false;
    });
  }

  window.AlhazawaIcons = icon;
})();
