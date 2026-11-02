/* ============================================================================
   Festi Dibi — application
   ========================================================================== */

var EDITION = {
  numero: 12,
  debut: "2026-12-22T16:00:00",
  fin: "2027-01-03T23:00:00"
};

var $ = function (s, c) { return (c || document).querySelector(s); };
var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

/* ---------------------------------------------------------- compte à rebours */
function initCountdown() {
  var d = $("#cd-d");
  if (!d) return;

  var h = $("#cd-h");
  var m = $("#cd-m");
  var s = $("#cd-s");
  var box = $("#countdown");
  var start = new Date(EDITION.debut).getTime();
  var end = new Date(EDITION.fin).getTime();

  function message(text) {
    if (box && box.dataset.done !== text) {
      box.dataset.done = text;
      box.innerHTML = '<p class="countdown__live">' + text + "</p>";
    }
  }

  function tick() {
    var now = Date.now();
    var diff = start - now;

    if (now >= end) {
      message("La 12<sup>e</sup> édition est terminée — à l’année prochaine");
      return;
    }
    if (diff <= 0) {
      message("Le festival est en cours · Place du Cinquantenaire");
      return;
    }

    var pad = function (n) { return String(n).padStart(2, "0"); };
    d.textContent = Math.floor(diff / 86400000);
    h.textContent = pad(Math.floor((diff % 86400000) / 3600000));
    m.textContent = pad(Math.floor((diff % 3600000) / 60000));
    s.textContent = pad(Math.floor((diff % 60000) / 1000));
  }

  tick();
  setInterval(tick, 1000);
}

/* --------------------------------------------------------------- braises */
function initEmbers() {
  var canvas = $("#embers");
  if (!canvas) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var ctx = canvas.getContext("2d", { alpha: true });
  if (!ctx) return;

  var w = 0;
  var h = 0;
  var dpr = 1;
  var particles = [];
  var raf = null;
  var visible = true;
  var running = true;

  /* deux sprites pré-rendus : bien plus rapide que recréer un gradient
     pour chaque particule à chaque image. */
  function sprite(hue) {
    var c = document.createElement("canvas");
    var size = 64;
    c.width = size;
    c.height = size;
    var g = c.getContext("2d");
    var grad = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
    grad.addColorStop(0, "hsla(" + hue + ",96%,72%,.95)");
    grad.addColorStop(0.32, "hsla(" + hue + ",96%,58%,.55)");
    grad.addColorStop(1, "hsla(" + hue + ",96%,50%,0)");
    g.fillStyle = grad;
    g.fillRect(0, 0, size, size);
    return c;
  }

  var sprites = [sprite(38), sprite(12)];

  function spawn(initial) {
    return {
      x: Math.random() * w,
      y: initial ? Math.random() * h : h + Math.random() * h * 0.3,
      r: Math.random() * 1.9 + 0.55,
      vy: -(Math.random() * 0.42 + 0.12),
      vx: (Math.random() - 0.5) * 0.16,
      life: Math.random(),
      sprite: sprites[Math.random() > 0.45 ? 0 : 1]
    };
  }

  function resize() {
    var rect = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    w = rect.width;
    h = rect.height;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var count = Math.max(14, Math.min(26, Math.round(w / 48)));
    particles = Array.from({ length: count }, function () { return spawn(true); });
  }

  function draw() {
    if (!running) return;
    if (!visible || document.hidden) {
      raf = null;
      return;
    }

    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = "lighter";

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.y += p.vy;
      p.x += p.vx + Math.sin((p.y + p.life * 90) / 88) * 0.2;
      p.life += 0.0045;
      if (p.y < -24) {
        var n = spawn(false);
        p.x = n.x;
        p.y = n.y;
        p.r = n.r;
        p.vy = n.vy;
        p.vx = n.vx;
        p.life = n.life;
        p.sprite = n.sprite;
      }

      var alpha = Math.max(0, 0.5 - Math.abs((p.life % 1) - 0.5));
      var size = p.r * 16;
      ctx.globalAlpha = alpha;
      ctx.drawImage(p.sprite, p.x - size / 2, p.y - size / 2, size, size);
    }

    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "source-over";
    raf = requestAnimationFrame(draw);
  }

  function start() {
    if (running && !raf && visible && !document.hidden) {
      raf = requestAnimationFrame(draw);
    }
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(
      function (entries) {
        visible = entries[0].isIntersecting;
        if (!visible && raf) {
          cancelAnimationFrame(raf);
          raf = null;
        } else {
          start();
        }
      },
      { threshold: 0 }
    ).observe(canvas);
  }

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      running = false;
      if (raf) {
        cancelAnimationFrame(raf);
        raf = null;
      }
    } else {
      running = true;
      start();
    }
  });

  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      resize();
      start();
    }, 180);
  });

  resize();
  start();
}

/* -------------------------------------------------------------- installation */
function initInstall() {
  var btn = $("#installBtn");
  if (!btn) return;
  var deferred = null;

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferred = e;
    btn.hidden = false;
  });

  btn.addEventListener("click", async function () {
    if (!deferred) return;
    deferred.prompt();
    var choice = await deferred.userChoice;
    if (choice.outcome === "accepted") btn.hidden = true;
    deferred = null;
  });

  window.addEventListener("appinstalled", function () {
    btn.hidden = true;
    deferred = null;
  });
}

/* ------------------------------------------------------------- retour en haut */
function initToTop() {
  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "to-top";
  btn.setAttribute("aria-label", "Revenir en haut de la page");
  btn.innerHTML =
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
    '<path d="M12 19V5m0 0-6 6m6-6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  document.body.appendChild(btn);

  btn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  var ticking = false;
  function update() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      btn.classList.toggle("is-visible", window.scrollY > 700);
      ticking = false;
    });
  }
  update();
  window.addEventListener("scroll", update, { passive: true });
}

/* ---------------------------------------------------------- service worker */
function initSW() {
  if (!("serviceWorker" in navigator)) return;
  if (location.protocol !== "http:" && location.protocol !== "https:") return;

  window.addEventListener("load", function () {
    navigator.serviceWorker.register("sw.js").catch(function () {});
  });
}

/* ------------------------------------------------------------------ départ */
document.addEventListener("DOMContentLoaded", function () {
  if (typeof Motion === "undefined") {
    document.documentElement.classList.add("motion-off");
  }
  initCountdown();
  initEmbers();
  initInstall();
  initToTop();
  initSW();
});
