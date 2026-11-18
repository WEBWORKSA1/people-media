/* People.Media — interactions. No frameworks, no trackers beyond AdSense. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  var C = window.PM_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); };

  /* ---------- Toast ---------- */
  function toast(msg) {
    var t = $("#toast"); if (!t) return;
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toast._t); toast._t = setTimeout(function () { t.classList.remove("show"); }, 4200);
  }
  window.pmToast = toast;

  /* ---------- Theme ---------- */
  var theme = store.get("pm-theme", null) || (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", theme);
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      theme = theme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", theme); store.set("pm-theme", theme);
    });
  });

  /* ---------- Mobile nav ---------- */
  var nav = $("#nav"), mb = $("#menuBtn");
  if (mb && nav) mb.addEventListener("click", function () {
    var open = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ---------- Cookie consent ---------- */
  var ck = $("#cookie");
  if (ck && !store.get("pm-consent", null)) ck.classList.add("show");
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () {
      store.set("pm-consent", b.getAttribute("data-consent"));
      if (b.getAttribute("data-consent") === "essential") {
        (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1;
      }
      ck.classList.remove("show");
    });
  });

  /* ---------- Reading progress + reveal ---------- */
  var bar = $(".reading-bar");
  if (bar) window.addEventListener("scroll", function () {
    var h = document.documentElement; var p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    bar.style.width = (p * 100).toFixed(1) + "%";
  }, { passive: true });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: .12 });
    $$(".fade").forEach(function (el) { io.observe(el); });
  } else { $$(".fade").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- Floating CTA ---------- */
  var fc = $(".float-cta");
  if (fc) window.addEventListener("scroll", function () { fc.classList.toggle("show", window.scrollY > 900); }, { passive: true });

  /* ---------- Secure form delivery ----------
     The destination inbox is never written in the page. It is assembled only at
     submit time from an encoded value and sent through FormSubmit's AJAX API. */
  var _k = ["=02bj5C", "bpFWbnBUM", "hN3ay92d", "iV2d"];
  function inbox() { try { return atob(_k.join("").split("").reverse().join("")); } catch (e) { return ""; } }
  function endpoint() { return "https://formsubmit.co/ajax/" + inbox(); }

  function serialize(form) {
    var data = {}; new FormData(form).forEach(function (v, k) {
      if (data[k]) data[k] = data[k] + ", " + v; else data[k] = v;
    });
    $$("[data-collect]", form).forEach(function (el) { data[el.getAttribute("data-collect")] = el.getAttribute("data-value") || el.value || ""; });
    return data;
  }

  function sendForm(form) {
    var data = serialize(form);
    if (data._honey) return Promise.resolve(true); // bot
    delete data._honey;
    data._subject = "[People.Media] " + (form.getAttribute("data-form") || "Form") + " — " + (data.name || data.email || "new submission");
    data._template = "table"; data._captcha = "false";
    data.page = location.href; data.submitted_at = new Date().toISOString();
    return fetch(endpoint(), {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data)
    }).then(function (r) { return r.ok; }).catch(function () { return false; });
  }

  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = $("button[type=submit]", form); var label = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.innerHTML = "Sending…"; }
      sendForm(form).then(function (ok) {
        if (btn) { btn.disabled = false; btn.innerHTML = label; }
        if (ok) {
          var done = form.getAttribute("data-success") || "Thank you — we received it and will reply within 2 business days.";
          var box = document.createElement("div"); box.className = "notice"; box.setAttribute("role", "status");
          box.innerHTML = "<strong>Received ✓</strong> " + esc(done);
          form.replaceWith(box); toast("Sent! Check your inbox for our reply.");
          if (form.getAttribute("data-form") === "Newsletter") store.set("pm-sub", 1);
        } else {
          toast("Couldn't send right now. Please try again in a minute.");
        }
      });
    });
  });

  /* ---------- Multi-step lead form ---------- */
  $$("[data-steps]").forEach(function (wrap) {
    var steps = $$(".step", wrap), dots = $$(".steps span", wrap), i = 0;
    function show(n) {
      steps.forEach(function (s, k) { s.classList.toggle("active", k === n); });
      dots.forEach(function (d, k) { d.classList.toggle("done", k <= n); }); i = n;
    }
    $$("[data-next]", wrap).forEach(function (b) {
      b.addEventListener("click", function () {
        var cur = steps[i]; var bad = $$("input,select,textarea", cur).filter(function (f) { return !f.checkValidity(); });
        if (bad.length) { bad[0].reportValidity(); return; }
        var group = $("[data-choice]", cur);
        if (group && group.hasAttribute("data-required") && !$(".opt.sel", group)) { toast("Pick one option to continue."); return; }
        show(Math.min(i + 1, steps.length - 1));
      });
    });
    $$("[data-prev]", wrap).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(i - 1, 0)); }); });
    show(0);
  });
  $$("[data-choice]").forEach(function (g) {
    var multi = g.hasAttribute("data-multi"); var hidden = $("input[type=hidden]", g);
    $$(".opt", g).forEach(function (o) {
      o.addEventListener("click", function () {
        if (!multi) $$(".opt", g).forEach(function (x) { x.classList.remove("sel"); });
        o.classList.toggle("sel");
        if (hidden) hidden.value = $$(".opt.sel", g).map(function (x) { return x.getAttribute("data-v"); }).join(", ");
      });
    });
  });
  // Preselect package from ?package=
  var qp = new URLSearchParams(location.search);
  if (qp.get("package")) { var po = $('.opt[data-v="' + qp.get("package").replace(/"/g, "") + '"]'); if (po) po.click(); }

  /* ---------- Search + filter ---------- */
  $$("[data-filter-scope]").forEach(function (scope) {
    var items = $$("[data-item]", scope), q = $(".search", scope), chips = $$(".chip", scope), cat = "all";
    function apply() {
      var term = (q && q.value || "").toLowerCase().trim(); var shown = 0;
      items.forEach(function (it) {
        var okC = cat === "all" || (it.getAttribute("data-cat") || "").indexOf(cat) > -1;
        var okQ = !term || it.textContent.toLowerCase().indexOf(term) > -1;
        it.style.display = okC && okQ ? "" : "none"; if (okC && okQ) shown++;
      });
      var empty = $("[data-empty]", scope); if (empty) empty.style.display = shown ? "none" : "";
    }
    if (q) q.addEventListener("input", apply);
    chips.forEach(function (c) { c.addEventListener("click", function () { chips.forEach(function (x) { x.classList.remove("active"); }); c.classList.add("active"); cat = c.getAttribute("data-cat"); apply(); }); });
  });

  /* ---------- Boost (community voting) ---------- */
  var boosts = store.get("pm-boosts", {});
  $$("[data-boost]").forEach(function (b) {
    var id = b.getAttribute("data-boost"), base = parseInt(b.getAttribute("data-base") || "0", 10);
    var n = $("b", b);
    function paint() { var on = !!boosts[id]; b.classList.toggle("on", on); if (n) n.textContent = (base + (on ? 1 : 0)).toLocaleString(); b.setAttribute("aria-pressed", on); }
    b.addEventListener("click", function () { boosts[id] = !boosts[id]; store.set("pm-boosts", boosts); paint(); if (boosts[id]) toast("Boosted! Share the profile to push it up the Trending list."); });
    paint();
  });
  // Sort trending lists by score
  $$("[data-sort-boost]").forEach(function (list) {
    var kids = $$("[data-score]", list);
    kids.sort(function (a, b) { return parseInt(b.getAttribute("data-score"), 10) - parseInt(a.getAttribute("data-score"), 10); })
      .forEach(function (k) { list.appendChild(k); });
  });

  /* ---------- Share ---------- */
  $$("[data-share]").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = location.href, t = document.title, kind = b.getAttribute("data-share"), u = encodeURIComponent(url), tt = encodeURIComponent(t);
      var map = { x: "https://twitter.com/intent/tweet?url=" + u + "&text=" + tt, fb: "https://www.facebook.com/sharer/sharer.php?u=" + u, li: "https://www.linkedin.com/sharing/share-offsite/?url=" + u, wa: "https://api.whatsapp.com/send?text=" + tt + "%20" + u };
      if (kind === "copy") { (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { toast("Link copied"); }, function () { prompt("Copy this link:", url); }); return; }
      if (kind === "native" && navigator.share) { navigator.share({ title: t, url: url }).catch(function () {}); return; }
      window.open(map[kind] || map.x, "_blank", "noopener,width=640,height=560");
    });
  });

  /* ---------- Countdown ---------- */
  $$("[data-countdown]").forEach(function (el) {
    var end = new Date(el.getAttribute("data-countdown") || (C.contest && C.contest.closes)).getTime();
    function tick() {
      var d = Math.max(0, end - Date.now()), s = Math.floor(d / 1000);
      var parts = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
      $$("b", el).forEach(function (b, k) { b.textContent = String(parts[k]).padStart(2, "0"); });
    }
    tick(); setInterval(tick, 1000);
  });

  /* ---------- Donations ---------- */
  var don = $("#donate");
  if (don) {
    var freq = "monthly", amt = 25, cur = (C.fundraising && C.fundraising.currency) || "$";
    var presets = { once: [10, 25, 50, 100, 250, 500], monthly: [5, 10, 25, 50, 100, 250], yearly: [50, 100, 250, 500, 1000, 2500] };
    var amtBox = $("#amounts", don), other = $("#otherAmt", don), out = $("#donSummary", don);
    function renderAmts() {
      amtBox.innerHTML = presets[freq].map(function (a) { return '<button type="button" data-a="' + a + '"' + (a === amt ? ' class="on"' : "") + ">" + cur + a + "</button>"; }).join("");
      $$("button", amtBox).forEach(function (b) { b.addEventListener("click", function () { amt = +b.getAttribute("data-a"); other.value = ""; renderAmts(); sum(); }); });
    }
    function sum() {
      var a = other.value ? +other.value : amt;
      out.textContent = cur + (a || 0) + (freq === "once" ? " one-time" : freq === "monthly" ? " / month" : " / year");
      $("#donAmount").value = a; $("#donFreq").value = freq;
    }
    $$(".seg button", don).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".seg button", don).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on");
        freq = b.getAttribute("data-f"); amt = presets[freq][2]; renderAmts(); sum();
      });
    });
    other.addEventListener("input", function () { $$("button", amtBox).forEach(function (x) { x.classList.remove("on"); }); sum(); });
    renderAmts(); sum();
    // Payment buttons (only those configured)
    var P = C.payments || {}, pay = $("#payLinks");
    if (pay) {
      var links = [];
      if (P.stripeLink) links.push(['Card (Stripe)', P.stripeLink]);
      if (P.paypalMe) links.push(['PayPal', "https://paypal.me/" + encodeURIComponent(P.paypalMe)]);
      if (P.buyMeACoffee) links.push(['Buy Me a Coffee', "https://www.buymeacoffee.com/" + encodeURIComponent(P.buyMeACoffee)]);
      if (P.kofi) links.push(['Ko-fi', "https://ko-fi.com/" + encodeURIComponent(P.kofi)]);
      if (P.upiId) links.push(['UPI', "upi://pay?pa=" + encodeURIComponent(P.upiId) + "&pn=People.Media&cu=INR"]);
      pay.innerHTML = links.length ? links.map(function (l) { return '<a class="btn btn-dark btn-sm" target="_blank" rel="noopener" href="' + esc(l[1]) + '">' + esc(l[0]) + "</a>"; }).join(" ")
        : '<span class="fine">Instant-pay buttons appear here once payment handles are configured. Your pledge below reserves your spot and we reply with a secure payment link.</span>';
    }
  }
  // Fundraising progress
  $$("[data-goal]").forEach(function (el) {
    var F = C.fundraising || { goal: 1, raised: 0 }; var pct = Math.min(100, Math.round((F.raised / F.goal) * 100));
    var i = $("i", el); setTimeout(function () { if (i) i.style.width = Math.max(pct, 2) + "%"; }, 200);
    var lab = $("[data-goal-label]"); if (lab) lab.textContent = (F.currency || "$") + (F.raised || 0).toLocaleString() + " raised of " + (F.currency || "$") + F.goal.toLocaleString() + " · " + (F.supporters || 0) + " founding supporters";
  });

  /* ---------- YouTube (lite embeds) ---------- */
  function liteVideo(v) {
    return '<div><div class="video" data-yt="' + esc(v.id) + '" role="button" tabindex="0" aria-label="Play ' + esc(v.title) + '">' +
      '<img loading="lazy" alt="" src="https://i.ytimg.com/vi/' + esc(v.id) + '/hqdefault.jpg"><span class="play"></span></div>' +
      '<p class="meta" style="margin-top:10px"><span class="tag teal">' + esc(v.channel || "Video") + "</span>" + (v.published ? "<span>" + esc(v.published.slice(0, 10)) + "</span>" : "") + "</p>" +
      '<h3 style="font-size:1.05rem;margin:4px 0 0">' + esc(v.title) + "</h3></div>";
  }
  function bindVideos(root) {
    $$("[data-yt]", root).forEach(function (el) {
      function play() { el.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + el.getAttribute("data-yt") + '?autoplay=1&rel=0" title="YouTube video" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>'; }
      el.addEventListener("click", play); el.addEventListener("keydown", function (e) { if (e.key === "Enter") play(); });
    });
  }
  bindVideos(document);
  var vg = $("#videoGrid");
  if (vg) {
    var limit = parseInt(vg.getAttribute("data-limit") || "12", 10);
    fetch("data/videos.json?v=" + Date.now().toString().slice(0, 7)).then(function (r) { return r.json(); }).then(function (d) {
      var vids = (d.videos || []).slice(0, limit);
      if (!vids.length) throw 0;
      vg.innerHTML = vids.map(liteVideo).join(""); bindVideos(vg);
      var up = $("[data-videos-updated]"); if (up && d.updated) up.textContent = "Auto-updated " + d.updated.slice(0, 16).replace("T", " ") + " UTC";
    }).catch(function () {
      vg.innerHTML = (C.youtubeFallback || []).map(function (c) { return '<a class="card" style="padding:22px;text-decoration:none" target="_blank" rel="noopener" href="' + esc(c.url) + '"><h3>' + esc(c.title) + '</h3><p class="fine">Watch on YouTube →</p></a>'; }).join("");
    });
  }

  /* ---------- Headlines (auto-refreshed JSON) ---------- */
  var hl = $("#headlines");
  if (hl) {
    fetch("data/headlines.json?v=" + Date.now().toString().slice(0, 7)).then(function (r) { return r.json(); }).then(function (d) {
      var items = (d.items || []).slice(0, parseInt(hl.getAttribute("data-limit") || "8", 10));
      if (!items.length) throw 0;
      hl.innerHTML = items.map(function (it) { return '<a href="' + esc(it.link) + '" target="_blank" rel="noopener nofollow"><span>' + esc(it.title) + "</span><small>" + esc(it.source) + "</small></a>"; }).join("");
    }).catch(function () { hl.innerHTML = '<p class="fine">Fresh headlines load after the next automatic refresh.</p>'; });
  }

  /* ---------- Born Today (live from Wikipedia's public API) ---------- */
  var bt = $("#bornToday");
  if (bt) {
    var now = new Date(), mm = String(now.getMonth() + 1).padStart(2, "0"), dd = String(now.getDate()).padStart(2, "0");
    var lbl = $("[data-today]"); if (lbl) lbl.textContent = now.toLocaleDateString(undefined, { month: "long", day: "numeric" });
    var cacheKey = "pm-born-" + mm + dd, cached = store.get(cacheKey, null);
    function paintBorn(list) {
      bt.innerHTML = "<ul>" + list.slice(0, parseInt(bt.getAttribute("data-limit") || "6", 10)).map(function (p) {
        return '<li><span class="yr">' + esc(p.year) + "</span>" + (p.img ? '<img loading="lazy" alt="" src="' + esc(p.img) + '">' : "") +
          '<span><a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.name) + "</a><br><small class=\"fine\">" + esc(p.desc || "") + "</small></span></li>";
      }).join("") + "</ul>";
    }
    if (cached) paintBorn(cached); else {
      fetch("https://en.wikipedia.org/api/rest_v1/feed/onthisday/births/" + mm + "/" + dd).then(function (r) { return r.json(); }).then(function (d) {
        var list = (d.births || []).filter(function (b) { return b.pages && b.pages[0]; }).map(function (b) {
          var p = b.pages[0]; return { year: b.year, name: (p.titles && p.titles.normalized) || p.title, desc: p.description, img: p.thumbnail && p.thumbnail.source, url: p.content_urls && p.content_urls.desktop && p.content_urls.desktop.page };
        }).filter(function (p) { return p.img; }).sort(function () { return Math.random() - .5; });
        store.set(cacheKey, list.slice(0, 20)); paintBorn(list);
      }).catch(function () { bt.innerHTML = '<p class="fine">Birthdays are loading slowly — refresh to try again.</p>'; });
    }
  }

  /* ---------- Newsletter modal (gentle, once per 7 days, never for subscribers) ---------- */
  var nm = $("#nlModal");
  if (nm && !store.get("pm-sub", 0)) {
    var last = store.get("pm-nl-seen", 0);
    if (Date.now() - last > 7 * 864e5) {
      var shown = false; var trigger = function () { if (shown) return; shown = true; nm.classList.add("show"); store.set("pm-nl-seen", Date.now()); };
      setTimeout(function () { window.addEventListener("scroll", function onS() { if (window.scrollY > 1600) { trigger(); window.removeEventListener("scroll", onS); } }, { passive: true }); }, 4000);
    }
  }
  $$("[data-close]").forEach(function (b) { b.addEventListener("click", function () { b.closest(".modal").classList.remove("show"); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") $$(".modal.show").forEach(function (m) { m.classList.remove("show"); }); });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
