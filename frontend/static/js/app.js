// Eidolon Day 3 orchestrator: polling + state + render coordination.

import { get, post } from "./api.js";
import { initMap, updateAgents, updateWorldObjects, setTooltip } from "./map.js";
import { renderAgentList, renderObra, renderLog, renderAudit, setObraTab, getObraTab } from "./panels.js";
import { openAgentModal } from "./modal.js";

const $ = (sel) => document.querySelector(sel);
const els = {
  map: $("#map"),
  tooltip: $("#map-tooltip"),
  agentsList: $("#agents-list"),
  agentsCount: $("#agents-count"),
  obraBody: $("#obra-body"),
  logBody: $("#log-body"),
  logCounts: $("#log-counts"),
  summary: $("#summary-line"),
  time: $("#time-banner"),
  tick: $("#tick-display"),
  btnAudit: $("#btn-audit"),
  btnCreator: $("#btn-creator"),
  auditPanel: $("#audit-panel"),
  auditContent: $("#audit-content"),
  creatorPanel: $("#creator-panel"),
  creatorLocation: $("#creator-location"),
  modal: $("#agent-modal"),
};

setTooltip(els.tooltip);

// === bootstrap ===
async function boot() {
  try {
    const locations = await get("/locations");
    initMap(els.map, locations, {
      tooltip: els.tooltip,
      onAgentClick: (id) => openAgentModal(id, els.modal),
    });
    // Populate creator location dropdown
    els.creatorLocation.innerHTML = locations
      .map((l) => `<option value="${l.id}">${l.nombre_display}</option>`)
      .join("");
  } catch (e) {
    console.error("boot failed", e);
    els.map.innerHTML = `<text x="50%" y="50%" fill="#ff8289" text-anchor="middle">backend offline: ${e}</text>`;
    return;
  }
  attachListeners();
  startPolling();
}

// === polling ===
const intervals = {};

function poll(path, intervalMs, handler) {
  async function tick() {
    try { handler(await get(path)); }
    catch (e) { console.warn(`poll ${path}`, e); }
    intervals[path] = setTimeout(tick, intervalMs);
  }
  tick();
}

function startPolling() {
  poll("/agents", 2000, (agents) => {
    updateAgents(agents);
    renderAgentList(els.agentsList, agents, (id) => openAgentModal(id, els.modal));
    els.agentsCount.textContent = `(${agents.length})`;
  });

  poll("/world_objects", 2500, (objs) => {
    // Need currentTick to detect "new" objects for animation
    updateWorldObjects(objs, currentTick);
  });

  poll("/log?limit=40", 2000, (logs) => {
    renderLog(els.logBody, logs);
    els.logCounts.textContent = `(${logs.length})`;
  });

  poll("/world", 3000, (w) => {
    if (w && typeof w.tick_actual === "number") {
      currentTick = w.tick_actual;
      els.tick.textContent = `tick ${w.tick_actual}`;
    }
  });

  poll("/time", 3000, (t) => {
    if (!t || t.error) { els.time.textContent = "—"; return; }
    const cls = `time-${t.time_of_day}`;
    els.time.innerHTML =
      `<span class="${cls}">${t.time_of_day}</span> ` +
      `<span class="dim">·</span> ` +
      `<span>día ${t.dia_num}</span> ` +
      `<span class="dim">·</span> ` +
      `<span class="dim">${t.luna_phase.replace("_", " ")}</span>`;
  });

  poll("/summary", 4000, (s) => {
    if (!s) return;
    els.summary.textContent =
      `agentes ${s.agents_alive} · libros ${s.books} · leyes ${s.institutions_ratified} · ` +
      `posts ${s.posts} · log ${s.action_log_accepts}A/${s.action_log_rejects}R`;
  });

  // Obra
  const refreshObra = async () => {
    try {
      const [books, institutions, posts, pendingRituals, ratifiedRituals, code] = await Promise.all([
        get("/books"),
        get("/institutions"),
        get("/posts"),
        get("/rituals/pending"),
        get("/rituals"),
        get("/code"),
      ]);
      const rituals = [...(pendingRituals || []), ...((ratifiedRituals || []).map((r) => ({ ...r, status: "ratified", ratify_count: 3 })))];
      renderObra(els.obraBody, { books, institutions, posts, rituals, code });
    } catch (e) { console.warn("obra refresh", e); }
  };
  refreshObra();
  setInterval(refreshObra, 5000);

  // Audit
  const refreshAudit = async () => {
    try {
      const a = await get("/audit");
      renderAudit(els.auditContent, a);
      const tone = a.fail > 0 ? "pill-danger" : a.warn > 0 ? "pill-warn" : "pill-ok";
      els.btnAudit.className = `pill ${tone}`;
      els.btnAudit.textContent = `AUDIT ${a.pass}P/${a.warn}W/${a.fail}F/${a.info}i`;
    } catch (e) { console.warn("audit", e); }
  };
  refreshAudit();
  setInterval(refreshAudit, 15000);
}

let currentTick = 0;

// === event listeners ===
function attachListeners() {
  // Obra tabs
  document.querySelectorAll(".tab").forEach((t) => {
    t.addEventListener("click", async () => {
      document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
      t.classList.add("active");
      setObraTab(t.dataset.tab);
      try {
        const [books, institutions, posts, pendingRituals, ratifiedRituals, code] = await Promise.all([
          get("/books"), get("/institutions"), get("/posts"),
          get("/rituals/pending"), get("/rituals"), get("/code"),
        ]);
        const rituals = [...(pendingRituals || []), ...((ratifiedRituals || []).map((r) => ({ ...r, status: "ratified", ratify_count: 3 })))];
        renderObra(els.obraBody, { books, institutions, posts, rituals, code });
      } catch (e) { console.warn(e); }
    });
  });

  // Audit toggle
  els.btnAudit.addEventListener("click", (e) => {
    e.stopPropagation();
    els.creatorPanel.classList.add("hidden");
    els.auditPanel.classList.toggle("hidden");
  });

  // Creator toggle
  els.btnCreator.addEventListener("click", (e) => {
    e.stopPropagation();
    els.auditPanel.classList.add("hidden");
    els.creatorPanel.classList.toggle("hidden");
  });

  // Creator spawn buttons
  document.querySelectorAll(".obj-btn[data-type]").forEach((b) => {
    b.addEventListener("click", async () => {
      const objectType = b.dataset.type;
      const loc = els.creatorLocation.value;
      try {
        const r = await post("/admin/spawn_object", { location_id: loc, object_type: objectType });
        if (r.error) alert(r.error);
        els.creatorPanel.classList.add("hidden");
      } catch (e) { alert(e); }
    });
  });

  // Revive all
  document.getElementById("btn-revive-all").addEventListener("click", async () => {
    try {
      const r = await post("/admin/revive", {});
      console.log("revived:", r.revived);
      els.creatorPanel.classList.add("hidden");
    } catch (e) { alert(e); }
  });

  // Close popovers on click outside
  document.addEventListener("click", (e) => {
    if (!e.target.closest("#audit-panel") && !e.target.closest("#btn-audit")) {
      els.auditPanel.classList.add("hidden");
    }
    if (!e.target.closest("#creator-panel") && !e.target.closest("#btn-creator")) {
      els.creatorPanel.classList.add("hidden");
    }
  });

  // Modal close
  els.modal.addEventListener("click", (e) => {
    if (e.target.dataset.close === "1") {
      els.modal.classList.add("hidden");
    }
  });

  // ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      els.modal.classList.add("hidden");
      els.auditPanel.classList.add("hidden");
      els.creatorPanel.classList.add("hidden");
    }
  });
}

boot();
