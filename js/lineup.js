/* ============================================================================
   Festi Dibi — programmation
   ----------------------------------------------------------------------------
   - filtres jour / scène / genre
   - favoris persistants (localStorage)
   - compteur, état vide, réinitialisation
   - animations Motion facultatives
   ========================================================================== */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var M = window.Motion;
  var canAnimate = !!M && !reduce;

  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-artist]"));
  if (!cards.length) return;

  var chips = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var countOut = document.querySelector("[data-lineup-count]");
  var emptyState = document.querySelector("[data-lineup-empty]");
  var emptyText = document.querySelector("[data-lineup-empty-text]");
  var favToggle = document.querySelector("[data-fav-toggle]");
  var favOut = document.querySelector("[data-fav-count]");
  var resets = Array.prototype.slice.call(document.querySelectorAll("[data-lineup-reset]"));

  var FAV_KEY = "festidibi-favs";
  var state = { day: "all", scene: "all", genre: "all", favOnly: false };
  var favourites = readFavourites();

  function readFavourites() {
    try {
      var raw = localStorage.getItem(FAV_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function saveFavourites() {
    try {
      localStorage.setItem(FAV_KEY, JSON.stringify(favourites));
    } catch (e) {}
  }

  function idOf(card) {
    return card.dataset.id || card.dataset.name || "";
  }

  function isFavourite(card) {
    return favourites.indexOf(idOf(card)) !== -1;
  }

  function updateFavouriteUI() {
    cards.forEach(function (card) {
      var btn = card.querySelector("[data-fav]");
      if (!btn) return;
      var on = isFavourite(card);
      card.classList.toggle("is-fav", on);
      btn.setAttribute("aria-pressed", String(on));
      var name = card.dataset.name || "cet artiste";
      btn.setAttribute("aria-label", (on ? "Retirer des favoris : " : "Ajouter aux favoris : ") + name);
    });

    if (favOut) favOut.textContent = String(favourites.length);
    if (favToggle) {
      favToggle.setAttribute("aria-pressed", String(state.favOnly));
      favToggle.classList.toggle("is-on", state.favOnly);
    }
  }

  function matches(card) {
    if (state.day !== "all" && card.dataset.day !== state.day) return false;
    if (state.scene !== "all" && card.dataset.scene !== state.scene) return false;
    if (state.genre !== "all" && card.dataset.genre !== state.genre) return false;
    if (state.favOnly && !isFavourite(card)) return false;
    return true;
  }

  function apply(animate) {
    var shown = [];

    cards.forEach(function (card) {
      var ok = matches(card);
      card.classList.toggle("is-hidden", !ok);
      card.hidden = !ok;
      if (ok) shown.push(card);
    });

    chips.forEach(function (chip) {
      var group = chip.dataset.filter;
      if (!(group in state)) return;
      chip.setAttribute("aria-pressed", String(state[group] === chip.dataset.value));
    });

    if (countOut) countOut.textContent = String(shown.length);
    if (emptyState) emptyState.hidden = shown.length > 0;

    if (emptyText) {
      emptyText.textContent = state.favOnly
        ? "Aucun favori pour le moment. Touchez le cœur d’un artiste pour composer votre programme."
        : "Aucun artiste ne correspond à ces filtres. Essayez une autre combinaison.";
    }

    if (animate && canAnimate && shown.length) {
      M.animate(
        shown,
        { opacity: [0, 1], y: [18, 0], scale: [0.98, 1] },
        { duration: 0.55, delay: M.stagger(0.045), easing: [0.16, 1, 0.3, 1] }
      );
    }
  }

  function reset() {
    state.day = "all";
    state.scene = "all";
    state.genre = "all";
    state.favOnly = false;
    updateFavouriteUI();
    apply(true);
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var group = chip.dataset.filter;
      if (!(group in state)) return;
      var value = chip.dataset.value;
      if (state[group] === value) return;
      state[group] = value;
      apply(true);
    });
  });

  if (favToggle) {
    favToggle.addEventListener("click", function () {
      state.favOnly = !state.favOnly;
      updateFavouriteUI();
      apply(true);
    });
  }

  resets.forEach(function (btn) {
    btn.addEventListener("click", reset);
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-fav]"), function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var card = btn.closest("[data-artist]");
      if (!card) return;
      var id = idOf(card);
      var at = favourites.indexOf(id);
      if (at === -1) favourites.push(id);
      else favourites.splice(at, 1);
      saveFavourites();
      updateFavouriteUI();
      apply(true);
    });
  });

  updateFavouriteUI();
  apply(false);
})();
