/* ============================================================================
   Festi Dibi — Motion
   ----------------------------------------------------------------------------
   Animations pilotées par Motion (motion.dev), la bibliothèque de l'écosystème
   Framer Motion pour le web vanilla. Tout est local : aucune dépendance CDN.
   - apparitions au scroll (reveal)
   - cascades (stagger)
   - parallaxe liée au scroll
   - compteurs animés
   - respect de prefers-reduced-motion
   ========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var M = window.Motion;

  if (!M || reduce) {
    root.classList.add("motion-off");
    return;
  }

  var animate = M.animate;
  var inView = M.inView;
  var stagger = M.stagger;
  var scroll = M.scroll;

  var EASE = [0.16, 1, 0.3, 1];
  var EASE_SOFT = [0.22, 0.61, 0.36, 1];

  root.classList.add("motion-ready");

  /* --------------------------------------------------------------- hero */
  var heroItems = document.querySelectorAll("[data-hero]");
  if (heroItems.length) {
    animate(
      heroItems,
      { opacity: [0, 1], y: [26, 0] },
      {
        delay: stagger(0.075, { startDelay: 0.1 }),
        duration: 1.05,
        easing: EASE
      }
    );
  }

  /* ------------------------------------------------------------- reveals */
  document.querySelectorAll("[data-reveal]").forEach(function (el) {
    var delay = Number(el.dataset.delay || 0) / 1000;
    inView(
      el,
      function () {
        animate(
          el,
          { opacity: [0, 1], y: [26, 0] },
          { duration: 0.9, delay: delay, easing: EASE }
        );
      },
      { amount: 0.12, margin: "0px 0px -8% 0px" }
    );
  });

  /* ------------------------------------------------------------- cascades */
  document.querySelectorAll("[data-stagger]").forEach(function (group) {
    var items = group.querySelectorAll("[data-stagger-item]");
    if (!items.length) return;
    inView(
      group,
      function () {
        animate(
          items,
          { opacity: [0, 1], y: [24, 0] },
          { delay: stagger(0.07), duration: 0.85, easing: EASE }
        );
      },
      { amount: 0.08, margin: "0px 0px -6% 0px" }
    );
  });

  /* ------------------------------------------------------------- compteurs */
  var fmt = new Intl.NumberFormat("fr-FR");
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = Number(el.dataset.count || 0);
    var suffix = el.dataset.suffix || "";
    inView(
      el,
      function () {
        animate(0, target, {
          duration: 1.8,
          easing: EASE,
          onUpdate: function (v) {
            el.textContent = fmt.format(Math.round(v)) + suffix;
          }
        });
      },
      { amount: 0.55 }
    );
  });

  /* --------------------------------------------------------- traits animés */
  document.querySelectorAll(".stat, .tl").forEach(function (el) {
    inView(
      el,
      function () {
        el.classList.add("is-in");
      },
      { amount: 0.45 }
    );
  });

  /* ------------------------------------------------------------- marquee */
  /* la pause au survol évite de « perdre » la lecture du bandeau */
  var marquee = document.querySelector(".marquee__track");
  if (marquee) {
    marquee.addEventListener("pointerenter", function () {
      marquee.style.animationPlayState = "paused";
    });
    marquee.addEventListener("pointerleave", function () {
      marquee.style.animationPlayState = "running";
    });
  }

  /* --------------------------------------------------------- points de repère */
  document.querySelectorAll("[data-reveal]").forEach(function (el) {
    el.addEventListener("animationend", function () {
      el.style.willChange = "auto";
    });
  });

  window.__festiMotion = { animate: animate, stagger: stagger, easing: EASE_SOFT };
})();
