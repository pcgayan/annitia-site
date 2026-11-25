/* Annitia A.: language toggle (Swedish by default, English remembered across pages), phone menu, launch-list mailto. */
(function () {
  var KEY = "annitia-lang";

  function setLang(l, remember) {
    document.documentElement.lang = l;
    document.querySelectorAll("[data-" + l + "]").forEach(function (el) {
      el.innerHTML = el.getAttribute("data-" + l);
    });
    document.getElementById("b-en").setAttribute("aria-pressed", l === "en");
    document.getElementById("b-sv").setAttribute("aria-pressed", l === "sv");
    if (remember) { try { localStorage.setItem(KEY, l); } catch (e) { /* private window: not remembered */ } }
  }
  document.getElementById("b-en").addEventListener("click", function () { setLang("en", true); });
  document.getElementById("b-sv").addEventListener("click", function () { setLang("sv", true); });

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  // The pages are served in Swedish; only a saved choice of English switches them.
  if (saved === "en") setLang("en", false);

  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open);
  });

  var form = document.getElementById("join-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = document.getElementById("email").value.trim();
      if (!m) return;
      var subj = encodeURIComponent("Launch list: Annitia A.");
      var body = encodeURIComponent("Please add this address to the launch list: " + m);
      window.location.href = "mailto:ktronicsdev@gmail.com?subject=" + subj + "&body=" + body;
    });
  }
})();
