/* ============================================================================
   HEADER & FOOTER — composants partagés, injectés sur toutes les pages.
   ========================================================================== */
(function () {
  "use strict";

  var file = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  var isHome = file === "" || file === "index.html";
  var isLineup = file.indexOf("lineup") === 0;
  var isGallery = file.indexOf("galerie") === 0;

  function homeHref(hash) {
    return isHome ? hash : "index.html" + hash;
  }

  /* quatre pages, rien de plus */
  var links = [
    { key: "accueil",     label: "Accueil",     url: homeHref("#accueil") },
    { key: "programme",   label: "Programme",   url: "lineup.html",              page: isLineup },
    { key: "galerie",     label: "Galerie",     url: "galerie.html",             page: isGallery },
    { key: "billetterie", label: "Billetterie", url: homeHref("#billetterie") }
  ];

  function logo() {
    return (
      '<img class="sh__logo" src="assets/logo.png" alt="" width="932" height="739" decoding="async">'
    );
  }

  function navItems(cls) {
    return links
      .map(function (l) {
        var cur = l.page ? ' aria-current="page"' : "";
        return (
          '<a class="' + cls + '" data-key="' + l.key + '" href="' + l.url + '"' + cur + ">" +
          l.label +
          "</a>"
        );
      })
      .join("");
  }

  var headerMarkup =
    '<header class="sh" id="siteHeader">' +
      '<div class="sh__bar">' +
        '<a class="sh__brand" href="' + homeHref("#accueil") + '" aria-label="Festival du Dibi — accueil">' +
          logo() +
          '<span class="sh__sep" aria-hidden="true"></span>' +
          '<span class="sh__tagline">' +
            "<b>12<sup>e</sup> édition</b>" +
            "<span>Bamako · Mali</span>" +
          "</span>" +
        "</a>" +
        '<span class="sh__name" aria-hidden="true">FESTI DIBI</span>' +
        '<nav class="sh__nav" aria-label="Navigation principale">' + navItems("sh__link") + "</nav>" +
        '<div class="sh__actions">' +
          '<button class="sh__burger" id="shBurger" type="button" aria-expanded="false" aria-controls="shMobile" aria-label="Ouvrir le menu">' +
            '<svg class="sh__ico sh__ico--open" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
              '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>' +
            "</svg>" +
            '<svg class="sh__ico sh__ico--close" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
              '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>' +
            "</svg>" +
          "</button>" +
        "</div>" +
      "</div>" +
      '<nav class="sh__mobile" id="shMobile" hidden aria-label="Navigation mobile">' +
        navItems("sh__mlink") +
      "</nav>" +
    "</header>";

  /* icônes : jeu Lucide (traits 24×24, stroke 2, bouts arrondis) */
  var social = [
    {
      label: "Facebook",
      url: "https://www.facebook.com/LeFestivalduDibi/",
      path: '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'
    },
    {
      label: "Instagram",
      url: "https://www.instagram.com/explore/tags/festivaldudibi/",
      path: '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>'
    },
    {
      label: "TikTok",
      url: "https://www.tiktok.com/search?q=festival%20du%20dibi",
      path: '<path d="M14.5 4c.5 2.4 2 3.9 4.4 4.2v3c-1.7 0-3.2-.5-4.4-1.4v6.1a5.4 5.4 0 1 1-5.4-5.4c.3 0 .6 0 .9.1v3.1a2.3 2.3 0 1 0 1.6 2.2V4h2.9Z" fill="currentColor" stroke="none"/>'
    },
    {
      label: "YouTube",
      url: "https://www.youtube.com/results?search_query=festival+du+dibi",
      path: '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/>'
    }
  ];

  function socialMarkup() {
    return social
      .map(function (s) {
        return (
          '<a href="' + s.url + '" target="_blank" rel="noopener" aria-label="' + s.label + ' — nouvelle fenêtre">' +
          '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
          s.path +
          "</svg></a>"
        );
      })
      .join("");
  }

  var footerMarkup =
    '<footer class="ft" id="siteFooter">' +
      '<div class="wrap ft__main">' +
        '<div class="ft__brand">' +
          '<a class="ft__logo-link" href="' + homeHref("#accueil") + '" aria-label="Festival du Dibi — accueil">' +
            '<img class="ft__logo" src="assets/logo.png" alt="Festival du Dibi, 12e édition" width="932" height="739" loading="lazy" decoding="async">' +
          "</a>" +
          '<p>Le 1<sup>er</sup> festival gastronomique d’Afrique de l’Ouest. La braise, le partage et le Mali, treize jours durant.</p>' +
          '<span class="ft__badge"><i></i>12<sup>e</sup> édition · 22 déc. 2026 → 3 janv. 2027</span>' +
          '<div class="ft__social" aria-label="Réseaux sociaux">' + socialMarkup() + "</div>" +
        "</div>" +
        '<nav class="ft__col" aria-label="Le festival">' +
          "<h3>Le festival</h3>" +
          '<a href="' + homeHref("#festival") + '">Le dibi, notre histoire</a>' +
          '<a href="' + homeHref("#histoire") + '">Les 12 éditions</a>' +
          '<a href="' + homeHref("#experience") + '">L’expérience</a>' +
          '<a href="lineup.html">Programme 2026</a>' +
          '<a href="galerie.html">Galerie photo</a>' +
        "</nav>" +
        '<nav class="ft__col" aria-label="Informations pratiques">' +
          "<h3>Pratique</h3>" +
          '<a href="' + homeHref("#billetterie") + '">Pass & billetterie</a>' +
          '<a href="' + homeHref("#infos") + '">Lieu & horaires</a>' +
          '<a href="' + homeHref("#infos") + '">Plan d’accès</a>' +
          '<a href="https://www.facebook.com/LeFestivalduDibi/" target="_blank" rel="noopener">Devenir exposant</a>' +
          '<a href="' + homeHref("#infos") + '">Nous contacter</a>' +
        "</nav>" +
        '<div class="ft__news">' +
          "<h3>La lettre du Dibi</h3>" +
          "<p>Programme, ouverture de la billetterie et coulisses de la 12<sup>e</sup> édition. Un message par mois, pas plus.</p>" +
          '<form class="ft__form" data-newsletter novalidate>' +
            '<label class="sr-only" for="nlEmail">Votre adresse e-mail</label>' +
            '<input id="nlEmail" type="email" name="email" placeholder="votre@email.com" autocomplete="email" required>' +
            '<button type="submit" aria-label="S’inscrire à la lettre du Dibi">' +
              '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>' +
            "</button>" +
          "</form>" +
          '<p class="ft__msg" data-newsletter-msg aria-live="polite"></p>' +
          '<a class="ft__contact" href="https://www.facebook.com/LeFestivalduDibi/" target="_blank" rel="noopener">' +
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>' +
            "Nous écrire sur Facebook" +
          "</a>" +
        "</div>" +
      "</div>" +
      '<div class="wrap ft__bottom">' +
        "<p>© <span data-year>2026</span> <b>Festival du Dibi</b> · InfluYence Group</p>" +
        "<p>Place du Cinquantenaire · Bamako, Mali</p>" +
        "<p>Maquette de démonstration — chiffres et programme à valider avec les organisateurs.</p>" +
      "</div>" +
      '<div class="ft__flag" aria-hidden="true"></div>' +
    "</footer>";

  var first = document.body.firstElementChild;
  if (first && (first.classList.contains("skip") || first.classList.contains("sr-only-focusable"))) {
    first.insertAdjacentHTML("afterend", headerMarkup);
  } else {
    document.body.insertAdjacentHTML("afterbegin", headerMarkup);
  }
  document.body.insertAdjacentHTML("beforeend", footerMarkup);

  var header = document.getElementById("siteHeader");
  var burger = document.getElementById("shBurger");
  var mobile = document.getElementById("shMobile");

  /* ---------------------------------------------------------- état scroll */
  var ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      header.classList.toggle("is-scrolled", (window.scrollY || 0) > 12);
      ticking = false;
    });
  }

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  /* -------------------------------------------------------------- menu */
  function closeMenu() {
    mobile.hidden = true;
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", "Ouvrir le menu");
  }

  burger.addEventListener("click", function () {
    var open = mobile.hidden;
    mobile.hidden = !open;
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    if (open) {
      var firstLink = mobile.querySelector("a");
      if (firstLink) firstLink.focus({ preventScroll: true });
    }
  });

  Array.prototype.forEach.call(mobile.querySelectorAll("a"), function (a) {
    a.addEventListener("click", closeMenu);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });

  document.addEventListener("pointerdown", function (e) {
    if (!mobile.hidden && !header.contains(e.target)) closeMenu();
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth >= 1000) closeMenu();
  });

  /* --------------------------------------------------------- scroll spy */
  function setActive(key) {
    var all = header.querySelectorAll("[data-key]");
    Array.prototype.forEach.call(all, function (a) {
      a.classList.toggle("is-active", a.getAttribute("data-key") === key);
    });
  }

  if (isHome && "IntersectionObserver" in window) {
    var map = {
      festival: "festival",
      histoire: "festival",
      experience: "festival",
      galerie: "galerie",
      programme: "programme",
      billetterie: "billetterie",
      infos: "infos"
    };
    var sections = Array.prototype.filter.call(
      document.querySelectorAll("section[id]"),
      function (s) { return !!map[s.id]; }
    );
    if (sections.length) {
      var spy = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            var key = map[entry.target.id];
            if (key) setActive(key);
          });
        },
        { rootMargin: "-42% 0px -50% 0px", threshold: 0 }
      );
      sections.forEach(function (s) { spy.observe(s); });
    }
  }

  /* -------------------------------------------------------- newsletter */
  var stored = null;
  try { stored = localStorage.getItem("festidibi-newsletter"); } catch (e) {}

  Array.prototype.forEach.call(document.querySelectorAll("[data-newsletter]"), function (form) {
    var input = form.querySelector('input[type="email"]');
    var box = form.parentElement.querySelector("[data-newsletter-msg]");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var value = (input.value || "").trim();
      if (!value || !input.checkValidity()) {
        if (box) box.textContent = "Entrez une adresse e-mail valide pour recevoir les infos.";
        input.focus();
        return;
      }
      try { localStorage.setItem("festidibi-newsletter", value); } catch (err) {}
      if (box) box.textContent = "Merci ! Vous serez prévenu·e de l’ouverture de la billetterie.";
      form.reset();
      form.classList.add("is-done");
      setTimeout(function () { form.classList.remove("is-done"); }, 2600);
    });
  });

  /* boutons « être prévenu » */
  Array.prototype.forEach.call(document.querySelectorAll("[data-notify]"), function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var footer = document.getElementById("siteFooter");
      if (!footer) return;
      footer.scrollIntoView({ behavior: "smooth", block: "start" });
      var input = footer.querySelector('input[type="email"]');
      var form = footer.querySelector("[data-newsletter]");
      if (!input) return;
      setTimeout(function () {
        input.focus({ preventScroll: true });
        if (form) {
          form.classList.add("is-highlight");
          setTimeout(function () { form.classList.remove("is-highlight"); }, 2200);
        }
      }, 650);
    });
  });

  /* -------------------------------------------------------------- année */
  Array.prototype.forEach.call(document.querySelectorAll("[data-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
