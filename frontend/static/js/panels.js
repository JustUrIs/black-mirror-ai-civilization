// Side panels: AgentList, Obra (tabs), LiveLog.

import { faceFor, colorFor } from "./faces.js";

let obraTab = "libros";

export function renderAgentList(container, agents, onClick) {
  if (!agents || !agents.length) {
    container.innerHTML = `<div class="empty-state">sin agentes</div>`;
    return;
  }
  container.innerHTML = "";
  for (const a of agents) {
    const card = document.createElement("button");
    card.className = "agent-card";
    card.style.borderLeft = `3px solid ${colorFor(a.id)}`;
    card.onclick = () => onClick(a.id);

    const n = a.necesidades || {};
    const transit = a.in_transit
      ? `<span class="agent-card-transit">→ ${a.in_transit.destino} (${a.in_transit.ticks_restantes}t)</span>`
      : `salud ${Math.round(a.salud)} · ${Math.round(a.gleam)}g`;

    card.innerHTML = `
      <div class="agent-card-head">
        <span class="agent-emoji">${faceFor(a)}</span>
        <span class="agent-card-name">${escapeHTML(a.nombre)}</span>
        <span class="agent-card-loc">${escapeHTML(a.ubicacion)}</span>
      </div>
      <div class="agent-card-status">${transit}</div>
      ${bar("hambre", n.hambre || 0, true)}
      ${bar("energia", n.energia ?? 100, false)}
      ${bar("sed", n.sed || 0, true)}
    `;
    container.append(card);
  }
}

function bar(label, value, danger) {
  const pct = Math.max(0, Math.min(100, value));
  let cls;
  if (danger) cls = pct >= 80 ? "bar-danger" : pct >= 50 ? "bar-warn" : "bar-dim";
  else cls = pct >= 80 ? "bar-ok" : pct >= 30 ? "bar-dim" : "bar-danger";
  return `<div class="bar-row">
    <label>${label}</label>
    <div class="bar"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
    <span class="bar-val">${Math.round(pct)}</span>
  </div>`;
}

export function setObraTab(t) { obraTab = t; }
export function getObraTab() { return obraTab; }

export function renderObra(container, data) {
  const { books, institutions, posts, rituals } = data;
  let html = "";

  if (obraTab === "libros") {
    if (!books?.length) html = empty("(sin libros)");
    else html = books.map((b) => `
      <article class="obra-card">
        <div class="obra-card-title">"${escapeHTML(b.titulo)}"</div>
        <div class="obra-card-meta">${escapeHTML(b.autor_id)} · t${b.tick} · ${b.longitud_chars} chars</div>
        <div class="obra-card-body">${escapeHTML(truncate(b.contenido, 220))}</div>
      </article>
    `).join("");
  } else if (obraTab === "leyes") {
    if (!institutions?.length) html = empty("(sin leyes ratificadas)");
    else html = institutions.map((i) => `
      <article class="obra-card">
        <div class="obra-card-title">${escapeHTML(i.nombre)}</div>
        <div class="obra-card-meta">ratificada · tick ${i.ratified_tick}</div>
        <div class="obra-card-body notitalic">${escapeHTML(i.texto)}</div>
      </article>
    `).join("");
  } else if (obraTab === "posts") {
    if (!posts?.length) html = empty("(sin posts)");
    else html = posts.slice().reverse().map((p) => `
      <article class="obra-card">
        <div class="obra-card-meta">@${escapeHTML(p.autor_id)} · t${p.tick} · #${escapeHTML(p.red)}</div>
        <div class="obra-card-body notitalic">${escapeHTML(p.contenido)}</div>
      </article>
    `).join("");
  } else if (obraTab === "rituales") {
    if (!rituals?.length) html = empty("(sin rituales)");
    else html = rituals.map((r) => `
      <article class="obra-card">
        <div class="obra-card-title">${escapeHTML(r.nombre)}</div>
        <div class="obra-card-meta">${escapeHTML(r.frecuencia || "(sin frecuencia)")} · ${r.status}</div>
        <div class="obra-card-body">${escapeHTML(r.descripcion)}</div>
        <div class="obra-card-progress">ratificacion: ${r.ratify_count}/3 (${(r.ratifiers || []).join(", ") || "ninguno"})</div>
      </article>
    `).join("");
  }
  container.innerHTML = html;
}

function empty(msg) { return `<div class="obra-empty">${msg}</div>`; }

export function renderLog(container, logs) {
  if (!logs?.length) {
    container.innerHTML = `<div class="empty-state">(sin acciones)</div>`;
    return;
  }
  container.innerHTML = logs.map((l) => {
    const detail = l.status === "accept" ? l.side_effect_summary : l.error_nl;
    return `
      <div class="log-row ${l.status}">
        <div class="log-row-head">
          <span class="log-tick">t${l.tick}</span>
          <span class="log-agent" style="color:${colorFor(l.agent_id)}">${escapeHTML(l.agent_id)}</span>
          <span class="log-action ${l.status}">${escapeHTML(l.action_type)}</span>
        </div>
        <div class="log-detail">${escapeHTML(detail || "")}</div>
      </div>
    `;
  }).join("");
}

export function renderAudit(container, report) {
  if (!report || !report.checks) {
    container.innerHTML = `<div class="empty-state">cargando...</div>`;
    return;
  }
  // Group by category
  const byCat = {};
  for (const c of report.checks) {
    (byCat[c.category] = byCat[c.category] || []).push(c);
  }
  let html = "";
  for (const cat of Object.keys(byCat).sort()) {
    html += `<div style="font-size:10px;color:var(--fg-dim);margin:8px 0 2px;text-transform:uppercase;letter-spacing:0.1em">— ${cat} —</div>`;
    for (const c of byCat[cat]) {
      html += `
        <div class="audit-row ${c.status}">
          <div class="audit-name">[${c.status}] ${escapeHTML(c.name)}</div>
          <div class="audit-summary">${escapeHTML(c.summary)}</div>
        </div>
      `;
    }
  }
  container.innerHTML = html;
}

function escapeHTML(s) {
  if (s == null) return "";
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function truncate(s, n) {
  if (!s) return "";
  return s.length > n ? s.slice(0, n) + "…" : s;
}
