// Agent detail modal: AI-Town-style profile + history + interactions.

import { get } from "./api.js";
import { faceFor, colorFor } from "./faces.js";

export async function openAgentModal(agentId, modalEl) {
  const card = document.getElementById("agent-modal-card");
  card.innerHTML = `<div class="empty-state">cargando ${agentId}…</div>`;
  modalEl.classList.remove("hidden");

  let agent, logs, books, letters, posts;
  try {
    [agent, logs, books, letters, posts] = await Promise.all([
      get(`/agents/${agentId}`),
      get(`/log?agent_id=${agentId}&limit=40`),
      get(`/books`),
      get(`/letters`),
      get(`/posts`),
    ]);
  } catch (e) {
    card.innerHTML = `<div class="empty-state">error: ${e}</div>`;
    return;
  }
  if (agent.error) {
    card.innerHTML = `<div class="empty-state">${agent.error}</div>`;
    return;
  }

  const seed = agent.seed_json || {};
  const myBooks = (books || []).filter((b) => b.autor_id === agentId);
  const myLetters = (letters || []).filter((l) => l.autor_id === agentId);
  const myPosts = (posts || []).filter((p) => p.autor_id === agentId);

  card.innerHTML = `
    <div class="modal-head">
      <div class="modal-emoji" style="color:${colorFor(agent.id)}">${faceFor(agent)}</div>
      <div class="modal-title">
        <h2 style="color:${colorFor(agent.id)}">${escapeHTML(agent.nombre)}</h2>
        <div class="modal-sub">
          en ${escapeHTML(agent.ubicacion)} · salud ${Math.round(agent.salud)} ·
          ${Math.round(agent.gleam)} gleam · ${agent.alive ? "vivo" : "💀 muerto"}
        </div>
      </div>
      <button class="modal-close" data-close="1">cerrar [×]</button>
    </div>

    ${section("Personalidad", `
      ${kv("conflicto", agent.primary_conflict || seed.primary_conflict)}
      ${kv("manera de hablar", seed.manera_de_hablar)}
      ${kv("morales", (agent.moral_lines || []).join(" · "))}
      ${kv("miedos", (seed.miedos || []).join(" · "))}
      ${kv("deseos", (seed.deseos || []).join(" · "))}
      ${kv("habilidades", (seed.habilidades_basicas || []).join(" · "))}
      ${kv("personalidad", (seed.personalidad_5_palabras || []).join(" · "))}
    `)}

    ${section("Pensamientos y estado", `
      ${kv("intencion actual", agent.intencion_actual || "(sin definir)")}
      ${kv("conocimiento", (agent.conocimiento || []).join(", ") || "(nada)")}
      ${kv("memoria_summary", agent.memoria_summary || "(vacio)")}
      ${kv("necesidades", Object.entries(agent.necesidades || {})
        .map(([k, v]) => `${k}=${Math.round(v)}`).join(" · "))}
    `)}

    ${section("Estado emocional", emotionalGrid(agent.emotional_state))}

    ${section("Relaciones", relationsList(agent.relaciones))}

    ${section(`Historial de acciones (${(logs || []).length})`, timeline(logs))}

    ${section(`Interacciones`, interactionsList(logs, agentId))}

    ${section(`Memoria reciente (${(agent.memoria_recent || []).length})`,
      (agent.memoria_recent || []).slice(-15).reverse().map((m) => `
        <div class="tl-row">
          <span class="tl-tick">t${m.tick ?? "?"}</span>
          <span class="tl-type">${escapeHTML(m.type || "")}</span>
          <span class="tl-detail">${escapeHTML(m.msg || m.snippet || m.titulo || "")}</span>
        </div>
      `).join("") || `<div class="empty-state">sin memoria</div>`)}

    ${section(`Sus artefactos`, artifactList(myBooks, myLetters, myPosts))}

    ${section("Personal history (durable)",
      (agent.personal_history || []).map((h) => `
        <div class="tl-row">
          <span class="tl-tick">t${h.tick ?? "?"}</span>
          <span class="tl-type">${escapeHTML(h.type || "")}</span>
          <span class="tl-detail">${escapeHTML(h.summary || "")}</span>
        </div>`).join("")
      || `<div class="empty-state">(vacio — esperado pre-Day 3 LLM)</div>`)}
  `;
}

function section(title, body) {
  return `
    <section class="modal-section">
      <div class="modal-section-title">${title}</div>
      <div class="modal-section-body">${body || `<div class="empty-state">vacio</div>`}</div>
    </section>
  `;
}

function kv(k, v) {
  if (!v) return "";
  return `<div class="kv-row"><span class="k">${k}</span><span class="v">${escapeHTML(v)}</span></div>`;
}

function emotionalGrid(es) {
  if (!es || Object.keys(es).length === 0) {
    return `<div class="empty-state">sin emotional_state</div>`;
  }
  return `<div class="emo-grid">
    ${Object.entries(es).map(([k, v]) => `
      <div class="kv-row" style="grid-template-columns:90px 1fr">
        <span class="k">${k}</span>
        <span class="v">${Number(v).toFixed(0)}</span>
      </div>
    `).join("")}
  </div>`;
}

function relationsList(rels) {
  const keys = Object.keys(rels || {});
  if (!keys.length) return `<div class="empty-state">sin relaciones</div>`;
  return keys.map((k) => {
    const v = rels[k];
    const cls = v > 0.1 ? "pos" : v < -0.1 ? "neg" : "neu";
    return `<div class="relation-row">
      <span>${escapeHTML(k)}</span>
      <span class="relation-val ${cls}">${v.toFixed(2)}</span>
    </div>`;
  }).join("");
}

function timeline(logs) {
  if (!logs || !logs.length) return `<div class="empty-state">sin acciones</div>`;
  return `<div class="timeline">${logs.map((l) => `
    <div class="tl-row ${l.status}">
      <span class="tl-tick">t${l.tick}</span>
      <span class="tl-type">${escapeHTML(l.action_type)}</span>
      <span class="tl-detail">${escapeHTML(l.status === "accept" ? l.side_effect_summary : l.error_nl)}</span>
    </div>
  `).join("")}</div>`;
}

function interactionsList(logs, agentId) {
  if (!logs) return `<div class="empty-state">cargando...</div>`;
  const interactionTypes = new Set(["TALK", "TRADE", "GIFT", "ATTACK", "TEACH", "LEARN", "RATIFY"]);
  const xs = (logs || []).filter((l) => interactionTypes.has(l.action_type));
  if (!xs.length) return `<div class="empty-state">sin interacciones registradas</div>`;
  return `<div class="timeline">${xs.map((l) => {
    const otro = l.params?.agente || l.params?.de || l.params?.proposal_id || "?";
    return `<div class="tl-row ${l.status}">
      <span class="tl-tick">t${l.tick}</span>
      <span class="tl-type">${escapeHTML(l.action_type)}</span>
      <span class="tl-detail">→ ${escapeHTML(String(otro))} · ${escapeHTML(l.side_effect_summary || l.error_nl || "")}</span>
    </div>`;
  }).join("")}</div>`;
}

function artifactList(books, letters, posts) {
  const parts = [];
  if (books?.length) {
    parts.push(`<div class="modal-section-title" style="margin-top:8px">libros</div>`);
    parts.push(books.map((b) => `
      <div class="kv-row"><span class="k">t${b.tick}</span><span class="v">"${escapeHTML(b.titulo)}" (${b.longitud_chars} chars)</span></div>
    `).join(""));
  }
  if (letters?.length) {
    parts.push(`<div class="modal-section-title" style="margin-top:8px">cartas</div>`);
    parts.push(letters.map((l) => `
      <div class="kv-row"><span class="k">t${l.tick}</span><span class="v">${escapeHTML(l.titulo || l.destinatario || "")}</span></div>
    `).join(""));
  }
  if (posts?.length) {
    parts.push(`<div class="modal-section-title" style="margin-top:8px">posts</div>`);
    parts.push(posts.map((p) => `
      <div class="kv-row"><span class="k">t${p.tick}</span><span class="v">${escapeHTML(p.contenido)}</span></div>
    `).join(""));
  }
  return parts.join("") || `<div class="empty-state">sin artefactos producidos</div>`;
}

function escapeHTML(s) {
  if (s == null) return "";
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}
