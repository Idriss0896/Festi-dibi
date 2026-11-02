/* ============================================================================
   Festi Dibi — galerie
   ----------------------------------------------------------------------------
   - visionneuse accessible (Échap, flèches, piège de focus, swipe)
   - filtres de catégories sur la page galerie
   - animations Motion facultatives : le site reste utilisable sans JS/Motion
   ========================================================================== */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var M = window.Motion;
  var canAnimate = !!M && !reduce;

  var lb = null;
  var lbImg = null;
  var lbCat = null;
  var lbTitle = null;
  var lbCount = null;
  var closeBtn = null;
  var prevBtn = null;
  var nextBtn = null;
  var current = [];
  var cursor = 0;
  var opener = null;

  function allTriggers() {
    return Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  }

  function isVisible(el) {
    var item = el.closest("[data-gallery-item]");
    if (item && (item.hidden || item.classList.contains("is-hidden"))) return false;
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  }

  function visibleTriggers() {
    return allTriggers().filter(isVisible);
  }

  function labelOf(el, key, fallback) {
    if (el.dataset && el.dataset[key]) return el.dataset[key];
    return fallback || "";
  }

  function srcOf(trigger) {
    if (trigger.dataset.full) return trigger.dataset.full;
    var img = trigger.querySelector("img");
    return img ? img.currentSrc || img.src : "";
  }

  function altOf(trigger) {
    var img = trigger.querySelector("img");
    return img ? img.alt : "";
  }

  /* ------------------------------------------------------------ lightbox */
  function build() {
    if (lb) return;

    lb = document.createElement("div");
    lb.className = "lb";
    lb.id = "lightbox";
    lb.hidden = true;
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Visionneuse photo");

    lb.innerHTML =
      '<button class="lb__close" type="button" data-lb-close aria-label="Fermer la visionneuse">' +
        '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
          '<path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' +
        "</svg>" +
      "</button>" +
      '<button class="lb__nav lb__prev" type="button" data-lb-prev aria-label="Photo précédente">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
          '<path d="M15 5 8 12l7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
        "</svg>" +
      "</button>" +
      '<button class="lb__nav lb__next" type="button" data-lb-next aria-label="Photo suivante">' +
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
          '<path d="m9 5 7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
        "</svg>" +
      "</button>" +
      '<figure class="lb__figure" data-lb-figure>' +
        '<img class="lb__img" alt="" decoding="async" data-lb-img>' +
        '<figcaption class="lb__cap">' +
          '<span class="lb__cat" data-lb-cat></span>' +
          '<b class="lb__title" data-lb-title></b>' +
          '<span class="lb__count" data-lb-count aria-live="polite"></span>' +
        "</figcaption>" +
      "</figure>";

    document.body.appendChild(lb);

    lbImg = lb.querySelector("[data-lb-img]");
    lbCat = lb.querySelector("[data-lb-cat]");
    lbTitle = lb.querySelector("[data-lb-title]");
    lbCount = lb.querySelector("[data-lb-count]");
    closeBtn = lb.querySelector("[data-lb-close]");
    prevBtn = lb.querySelector("[data-lb-prev]");
    nextBtn = lb.querySelector("[data-lb-next]");

    closeBtn.addEventListener("click", close);
    prevBtn.addEventListener("click", function () { step(-1); });
    nextBtn.addEventListener("click", function () { step(1); });

    lb.addEventListener("click", function (e) {
      if (e.target === lb) close();
    });

    /* swipe tactile et glisser à la souris */
    var figure = lb.querySelector("[data-lb-figure]");
    var startX = 0;
    var startY = 0;
    var tracking = false;

    figure.addEventListener("pointerdown", function (e) {
      if (e.target.closest("button")) return;
      tracking = true;
      startX = e.clientX;
      startY = e.clientY;
    });

    figure.addEventListener("pointerup", function (e) {
      if (!tracking) return;
      tracking = false;
      var dx = e.clientX - startX;
      var dy = e.clientY - startY;
      if (Math.abs(dx) > 46 && Math.abs(dx) > Math.abs(dy)) step(dx < 0 ? 1 : -1);
    });

    figure.addEventListener("pointercancel", function () { tracking = false; });
  }

  function render() {
    var trigger = current[cursor];
    if (!trigger) return;

    lbImg.src = srcOf(trigger);
    lbImg.alt = altOf(trigger);
    lbCat.textContent = labelOf(trigger, "cat", "Festival du Dibi");
    lbTitle.textContent = labelOf(trigger, "title", "Festival du Dibi");
    lbCount.textContent = (cursor + 1) + " / " + current.length;
    lb.setAttribute("aria-label", "Photo " + (cursor + 1) + " sur " + current.length + " — " + labelOf(trigger, "title", ""));

    var many = current.length > 1;
    prevBtn.hidden = !many;
    nextBtn.hidden = !many;

    if (canAnimate) {
      M.animate(lbImg, { opacity: [0.25, 1], scale: [0.992, 1] }, { duration: 0.38, easing: [0.16, 1, 0.3, 1] });
    }

    preload(cursor - 1);
    preload(cursor + 1);
  }

  function preload(at) {
    var trigger = current[(at + current.length) % current.length];
    if (!trigger || !current.length) return;
    var src = srcOf(trigger);
    if (src) {
      var im = new Image();
      im.decoding = "async";
      im.src = src;
    }
  }

  function open(trigger) {
    build();
    current = visibleTriggers();
    cursor = current.indexOf(trigger);
    if (cursor < 0) {
      current = [trigger];
      cursor = 0;
    }
    opener = trigger;

    render();
    lb.hidden = false;
    document.body.classList.add("lb-open");

    if (canAnimate) {
      M.animate(lb, { opacity: [0, 1] }, { duration: 0.28, easing: "ease-out" });
      M.animate(lb.querySelector("[data-lb-figure]"), { opacity: [0, 1], scale: [0.955, 1] }, { duration: 0.5, easing: [0.16, 1, 0.3, 1] });
    }

    closeBtn.focus({ preventScroll: true });
  }

  function close() {
    if (!lb || lb.hidden) return;
    lb.hidden = true;
    document.body.classList.remove("lb-open");
    lbImg.removeAttribute("src");
    if (opener && document.contains(opener)) opener.focus({ preventScroll: true });
  }

  function step(dir) {
    if (!current.length) return;
    cursor = (cursor + dir + current.length) % current.length;
    render();
  }

  function trapFocus(e) {
    if (e.key !== "Tab" || !lb || lb.hidden) return;
    var focusables = [closeBtn, prevBtn, nextBtn].filter(function (b) { return b && !b.hidden; });
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-lightbox]");
    if (!trigger) return;
    e.preventDefault();
    open(trigger);
  });

  document.addEventListener("keydown", function (e) {
    if (!lb || lb.hidden) return;
    if (e.key === "Escape") {
      e.preventDefault();
      close();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      step(-1);
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      step(1);
    } else {
      trapFocus(e);
    }
  });

  /* -------------------------------------------------------------- filtres */
  var galleryItems = Array.prototype.slice.call(document.querySelectorAll("[data-gallery-item]"));
  var filterChips = Array.prototype.slice.call(document.querySelectorAll("[data-gallery-filter]"));
  var countOut = document.querySelector("[data-gallery-count]");
  var emptyState = document.querySelector("[data-gallery-empty]");

  if (galleryItems.length && filterChips.length) {
    var activeFilter = "all";

    function applyFilter(value, animate) {
      activeFilter = value;
      var shown = [];

      galleryItems.forEach(function (item) {
        var ok = value === "all" || item.dataset.cat === value;
        item.classList.toggle("is-hidden", !ok);
        item.hidden = !ok;
        if (ok) shown.push(item);
      });

      filterChips.forEach(function (chip) {
        chip.setAttribute("aria-pressed", String(chip.dataset.galleryFilter === value));
      });

      if (countOut) countOut.textContent = String(shown.length);
      if (emptyState) emptyState.hidden = shown.length > 0;

      if (animate && canAnimate && shown.length) {
        M.animate(
          shown,
          { opacity: [0, 1], y: [16, 0], scale: [0.975, 1] },
          { duration: 0.55, delay: M.stagger(0.035), easing: [0.16, 1, 0.3, 1] }
        );
      }
    }

    filterChips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        if (chip.dataset.galleryFilter === activeFilter) return;
        applyFilter(chip.dataset.galleryFilter, true);
      });
    });

    applyFilter("all", false);
  }
})();
