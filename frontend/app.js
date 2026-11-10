/* ReviewLens front end — talks to the FastAPI backend (/api/*). */
(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const els = {
    review: $("#review"), count: $("#count"), analyze: $("#analyzeBtn"), clear: $("#clearBtn"),
    error: $("#formError"), result: $("#result"), arc: $("#arc"), pct: $("#pct"),
    badge: $("#badge"), badgeIcon: $("#badgeIcon"), verdict: $("#verdictLabel"), insight: $("#insight"),
    engineTag: $("#engineTag"), wordCount: $("#wordCount"), highlighted: $("#highlighted"),
    legend: $("#legend"), topics: $("#topics"), topicsCol: $("#topicsCol"),
    historySec: $("#historySec"), historyList: $("#historyList"), clearHistory: $("#clearHistory"),
    engineBtn: $("#engineBtn"), engineDot: $("#engineDot"), engineLabel: $("#engineLabel"),
    panel: $("#enginePanel"), panelDot: $("#panelDot"), panelName: $("#panelName"),
    panelDesc: $("#panelDesc"), panelError: $("#panelError"), modelsDir: $("#modelsDir"),
    reload: $("#reloadBtn"), theme: $("#themeBtn"), kbd: $("#kbdHint"),
  };

  const CIRC = 2 * Math.PI * 52;
  const HISTORY_KEY = "reviewlens.history";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let maxChars = 5000;
  let busy = false;

  const SAMPLES = {
    positive: "Absolutely love this blender! It crushes ice in seconds, arrived a day early, and the support team was super helpful when I had a question about the warranty.",
    mixed: "The design is beautiful and setup was easy, but the battery barely lasts half a day. Okay for the price, I guess.",
    negative: "Terrible experience. The package arrived damaged, the battery died after two days, and customer service never replied to my emails. Complete waste of money.",
  };

  const LABELS = { positive: "Positive", neutral: "Neutral", negative: "Negative" };
  const ICONS = {
    positive: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.5 14.2c1 1.5 2.7 2.3 4.5 2.3s3.5-.8 4.5-2.3"/><path d="M8.5 9.5h.01M15.5 9.5h.01" stroke-width="3"/></svg>',
    neutral: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 15.5h8"/><path d="M8.5 9.5h.01M15.5 9.5h.01" stroke-width="3"/></svg>',
    negative: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.5 16.5c1-1.5 2.7-2.3 4.5-2.3s3.5.8 4.5 2.3"/><path d="M8.5 9.5h.01M15.5 9.5h.01" stroke-width="3"/></svg>',
  };

  /* ---------- storage helpers (never throw) ---------- */
  const store = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, val) { try { localStorage.setItem(key, val); } catch { /* private mode */ } },
  };

  /* ---------- theme ---------- */
  function currentTheme() {
    const t = document.documentElement.dataset.theme;
    if (t) return t;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  els.theme.addEventListener("click", () => {
    const next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    store.set("reviewlens.theme", next);
  });

  /* ---------- engine status ---------- */
  function renderStatus(s) {
    const keras = s.engine === "keras";
    const k = s.keras || {};
    maxChars = s.max_chars || maxChars;
    els.review.maxLength = maxChars;
    updateCount();

    els.engineDot.dataset.state = keras ? "keras" : "builtin";
    els.panelDot.dataset.state = keras ? "keras" : "builtin";
    els.engineLabel.textContent = keras ? "Keras model active" : "Built-in engine";
    els.panelName.textContent = keras ? `Keras model · ${k.file}` : "Built-in engine";
    els.panelDesc.textContent = keras
      ? "Your trained CNN scores each review."
      : "Rule-based analysis. Works out of the box, no model file needed.";
    els.panelError.hidden = !k.error;
    els.panelError.textContent = k.error || "";
    if (k.models_dir) els.modelsDir.textContent = k.models_dir;
  }

  async function loadStatus() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) throw new Error();
      renderStatus(await res.json());
    } catch {
      els.engineDot.dataset.state = "";
      els.engineLabel.textContent = "Server unreachable";
    }
  }

  els.reload.addEventListener("click", async () => {
    els.reload.disabled = true;
    els.reload.textContent = "Reloading…";
    try {
      const res = await fetch("/api/reload", { method: "POST" });
      if (!res.ok) throw new Error();
      renderStatus(await res.json());
    } catch {
      els.panelError.hidden = false;
      els.panelError.textContent = "Could not reach the server.";
    } finally {
      els.reload.disabled = false;
      els.reload.textContent = "Reload model";
    }
  });

  function setPanel(open) {
    els.panel.hidden = !open;
    els.engineBtn.setAttribute("aria-expanded", String(open));
  }
  els.engineBtn.addEventListener("click", (e) => { e.stopPropagation(); setPanel(els.panel.hidden); });
  document.addEventListener("click", (e) => {
    if (!els.panel.hidden && !els.panel.contains(e.target)) setPanel(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !els.panel.hidden) { setPanel(false); els.engineBtn.focus(); }
  });

  /* ---------- composer ---------- */
  function updateCount() {
    const n = els.review.value.length;
    els.count.textContent = `${n.toLocaleString()} / ${maxChars.toLocaleString()}`;
    els.clear.hidden = n === 0;
  }
  els.review.addEventListener("input", () => { updateCount(); showError(""); });
  els.clear.addEventListener("click", () => { els.review.value = ""; updateCount(); showError(""); els.review.focus(); });

  document.querySelectorAll("[data-sample]").forEach((btn) => {
    btn.addEventListener("click", () => {
      els.review.value = SAMPLES[btn.dataset.sample];
      updateCount();
      analyze();
    });
  });

  els.kbd.textContent = /Mac|iPhone|iPad/.test(navigator.platform) ? "⌘ ↵" : "Ctrl ↵";
  els.review.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); analyze(); }
  });
  els.analyze.addEventListener("click", analyze);

  function showError(msg) {
    els.error.hidden = !msg;
    els.error.textContent = msg || "";
  }

  function setBusy(on) {
    busy = on;
    els.analyze.disabled = on;
    els.analyze.classList.toggle("busy", on);
    els.analyze.querySelector(".btn-label").textContent = on ? "Analyzing…" : "Analyze review";
    els.result.classList.toggle("loading", on);
    els.result.setAttribute("aria-busy", String(on));
  }

  async function analyze() {
    if (busy) return;
    const text = els.review.value.trim();
    if (!text) { showError("Paste or type a customer review first."); els.review.focus(); return; }
    showError("");
    setBusy(true);
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const detail = typeof data.detail === "string" ? data.detail : "Something went wrong. Please try again.";
        throw new Error(detail);
      }
      renderResult(data, text);
      pushHistory(text, data);
    } catch (err) {
      showError(err instanceof TypeError ? "Can't reach the server. Is the app still running?" : err.message);
    } finally {
      setBusy(false);
    }
  }

  /* ---------- result ---------- */
  function animateNumber(target) {
    if (reduceMotion) { els.pct.textContent = target.toFixed(1); return; }
    const start = performance.now(), dur = 800;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - t, 3);
      els.pct.textContent = (target * eased).toFixed(1);
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  function renderHighlighted(text, highlights) {
    els.highlighted.replaceChildren();
    let cursor = 0;
    for (const h of highlights) {
      if (h.start < cursor || h.end > text.length) continue;
      if (h.start > cursor) els.highlighted.append(text.slice(cursor, h.start));
      const mark = document.createElement("mark");
      mark.className = h.polarity === "positive" ? "pos" : "neg";
      mark.textContent = text.slice(h.start, h.end);
      mark.title = h.polarity === "positive" ? "Positive signal" : "Negative signal";
      els.highlighted.append(mark);
      cursor = h.end;
    }
    if (cursor < text.length) els.highlighted.append(text.slice(cursor));
    const has = (p) => highlights.some((h) => h.polarity === p);
    $("#lgPos").hidden = !has("positive");
    $("#lgNeg").hidden = !has("negative");
    els.legend.dataset.empty = String(highlights.length === 0);
  }

  function renderTopics(aspects) {
    els.topics.replaceChildren();
    if (!aspects.length) {
      const li = document.createElement("li");
      li.className = "none";
      li.textContent = "No specific topics detected.";
      els.topics.append(li);
      return;
    }
    for (const a of aspects) {
      const li = document.createElement("li");
      li.className = "topic";
      li.dataset.s = a.sentiment;
      const name = document.createElement("span");
      name.textContent = a.name;
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = a.mixed ? "Mixed" : LABELS[a.sentiment];
      li.append(name, tag);
      els.topics.append(li);
    }
  }

  function renderResult(data, text) {
    const first = els.result.hidden;
    els.result.hidden = false;
    els.result.dataset.sentiment = data.sentiment;
    els.verdict.textContent = LABELS[data.sentiment];
    els.badgeIcon.innerHTML = ICONS[data.sentiment]; // static, trusted markup only
    els.insight.textContent = data.insight;
    els.engineTag.textContent = data.engine === "keras" ? "Keras model" : "Built-in engine";
    els.wordCount.textContent = `${data.word_count} word${data.word_count === 1 ? "" : "s"}`;
    els.result.querySelector(".gauge").setAttribute("aria-label", `${LABELS[data.sentiment]}, ${data.percentage}% confidence`);
    renderHighlighted(text, data.highlights || []);
    renderTopics(data.aspects || []);

    // gauge: reset, then animate to the new value on the next frame
    els.arc.style.transition = "none";
    els.arc.style.strokeDashoffset = CIRC;
    els.pct.textContent = "0.0";
    requestAnimationFrame(() => requestAnimationFrame(() => {
      els.arc.style.transition = "";
      els.arc.style.strokeDashoffset = CIRC * (1 - data.percentage / 100);
      animateNumber(data.percentage);
    }));

    if (first || els.result.getBoundingClientRect().bottom > window.innerHeight) {
      els.result.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
    }
  }

  /* ---------- history (browser only) ---------- */
  function readHistory() {
    try { const v = JSON.parse(store.get(HISTORY_KEY) || "[]"); return Array.isArray(v) ? v : []; } catch { return []; }
  }
  function pushHistory(text, data) {
    const items = readHistory().filter((i) => i.text !== text);
    items.unshift({ text, sentiment: data.sentiment, percentage: data.percentage });
    store.set(HISTORY_KEY, JSON.stringify(items.slice(0, 6)));
    renderHistory();
  }
  function renderHistory() {
    const items = readHistory();
    els.historySec.hidden = items.length === 0;
    els.historyList.replaceChildren();
    for (const item of items) {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "h-item";
      btn.dataset.s = item.sentiment;
      btn.title = "Analyze this review again";
      const dot = document.createElement("span"); dot.className = "h-dot";
      const txt = document.createElement("span"); txt.className = "h-text"; txt.textContent = item.text;
      const res = document.createElement("span"); res.className = "h-res";
      res.textContent = `${LABELS[item.sentiment] || item.sentiment} ${Number(item.percentage).toFixed(1)}%`;
      btn.append(dot, txt, res);
      btn.addEventListener("click", () => { els.review.value = item.text; updateCount(); analyze(); window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" }); });
      li.append(btn);
      els.historyList.append(li);
    }
  }
  els.clearHistory.addEventListener("click", () => { store.set(HISTORY_KEY, "[]"); renderHistory(); });

  /* ---------- init ---------- */
  updateCount();
  renderHistory();
  loadStatus();
})();
