// SVG map renderer.
// Renders 8 locations + 11 edges. Updates agents + world_objects each tick.

import { faceFor, colorFor, emojiForObject } from "./faces.js";

const SVG_NS = "http://www.w3.org/2000/svg";

let projection = null;
let svg = null;
let layers = {};
let onAgentClick = null;

const agentMarkers = new Map();   // id -> { group, face, name, halo }
const objectMarkers = new Map();  // id -> { group }

export function initMap(svgEl, locations, opts = {}) {
  svg = svgEl;
  onAgentClick = opts.onAgentClick || (() => {});
  const tooltip = opts.tooltip;

  const xs = locations.map((l) => l.x);
  const ys = locations.map((l) => l.y);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys), maxY = Math.max(...ys);
  const padX = (maxX - minX) * 0.15;
  const padY = (maxY - minY) * 0.20;
  const vbW = 1000;
  const vbH = 700;
  svg.setAttribute("viewBox", `0 0 ${vbW} ${vbH}`);

  projection = (x, y) => {
    const nx = (x - (minX - padX)) / ((maxX + padX) - (minX - padX));
    const ny = (y - (minY - padY)) / ((maxY + padY) - (minY - padY));
    return [nx * vbW, ny * vbH];
  };

  // Layers (order matters for z-index)
  layers.edges = el("g", { class: "edges" });
  layers.locations = el("g", { class: "locations" });
  layers.objects = el("g", { class: "objects" });
  layers.transit = el("g", { class: "transits" });
  layers.agents = el("g", { class: "agents" });
  svg.innerHTML = "";
  svg.append(layers.edges, layers.locations, layers.objects, layers.transit, layers.agents);

  // Edges
  const byId = new Map(locations.map((l) => [l.id, l]));
  const drawn = new Set();
  for (const loc of locations) {
    const [x1, y1] = projection(loc.x, loc.y);
    for (const dst of loc.transitions || []) {
      const key = [loc.id, dst].sort().join("|");
      if (drawn.has(key)) continue;
      drawn.add(key);
      const t = byId.get(dst);
      if (!t) continue;
      const [x2, y2] = projection(t.x, t.y);
      const line = el("line", {
        x1, y1, x2, y2, class: "edge",
      });
      layers.edges.append(line);
    }
  }

  // Locations
  for (const loc of locations) {
    const [cx, cy] = projection(loc.x, loc.y);
    const color = locColor(loc);
    const r = (loc.radius || 5) * 5; // viewBox is 1000 wide vs coords ~70 wide
    const circle = el("circle", {
      cx, cy, r,
      fill: color, "fill-opacity": 0.15,
      stroke: color, "stroke-opacity": 0.6, "stroke-width": 2,
      class: "loc-circle",
      "data-loc": loc.id,
    });
    circle.addEventListener("mouseenter", (e) => showLocTooltip(e, loc, tooltip));
    circle.addEventListener("mouseleave", () => hideTooltip(tooltip));
    layers.locations.append(circle);

    const label = el("text", {
      x: cx, y: cy + r + 14,
      "text-anchor": "middle",
      class: "loc-label",
    });
    label.textContent = loc.nombre_display;
    layers.locations.append(label);
  }

  // Cache for project lookups
  initMap.byId = byId;
}

export function updateAgents(agents) {
  const byId = initMap.byId;
  const seen = new Set();

  for (const a of agents) {
    seen.add(a.id);
    let [tx, ty] = projection(a.x, a.y);
    let transitDest = null;

    if (a.in_transit) {
      const origin = byId.get(a.in_transit.origen);
      const dest = byId.get(a.in_transit.destino);
      if (origin && dest) {
        const total = a.in_transit.distancia_total || 1;
        const walked = Math.max(0, total - a.in_transit.ticks_restantes * 5);
        const progress = Math.max(0, Math.min(1, walked / total));
        const [ox, oy] = projection(origin.x, origin.y);
        const [dx, dy] = projection(dest.x, dest.y);
        tx = ox + (dx - ox) * progress;
        ty = oy + (dy - oy) * progress;
        transitDest = [dx, dy];
      }
    }

    let m = agentMarkers.get(a.id);
    if (!m) {
      const group = el("g", { class: "agent-group" });
      group.style.color = colorFor(a.id);
      const halo = el("circle", { cx: 0, cy: 0, r: 22, class: "agent-halo", fill: colorFor(a.id), stroke: colorFor(a.id) });
      const face = el("text", { x: 0, y: 2, class: "agent-face" });
      face.textContent = faceFor(a);
      const name = el("text", { x: 0, y: -28, class: "agent-name" });
      name.textContent = a.nombre.split(" ")[0];
      group.append(halo, face, name);
      group.addEventListener("click", () => onAgentClick(a.id));
      group.addEventListener("mouseenter", (e) => showAgentTooltip(e, a));
      group.addEventListener("mouseleave", () => hideTooltip(initMap.tooltip));
      layers.agents.append(group);
      m = { group, halo, face, name };
      agentMarkers.set(a.id, m);
    }
    m.group.setAttribute("transform", `translate(${tx}, ${ty})`);
    m.face.textContent = faceFor(a);

    // Transit line
    if (m.transitLine) { m.transitLine.remove(); m.transitLine = null; }
    if (transitDest) {
      const line = el("line", {
        x1: tx, y1: ty, x2: transitDest[0], y2: transitDest[1],
        stroke: "#ffba6c", "stroke-width": 1.5,
        class: "transit-line",
      });
      layers.transit.append(line);
      m.transitLine = line;
    }
  }

  // Cleanup stale
  for (const [id, m] of agentMarkers) {
    if (seen.has(id)) continue;
    m.group.remove();
    m.transitLine?.remove();
    agentMarkers.delete(id);
  }
}

export function updateWorldObjects(objects, currentTick) {
  const byId = initMap.byId;
  const seen = new Set();
  // group multiple objects at same location with offset
  const counter = new Map();
  for (const obj of objects) {
    if (obj.state !== "active") continue;
    seen.add(obj.id);
    const loc = byId.get(obj.location_id);
    if (!loc) continue;
    const idx = counter.get(obj.location_id) || 0;
    counter.set(obj.location_id, idx + 1);
    const [cx, cy] = projection(loc.x, loc.y);
    const offsetX = (idx % 3 - 1) * 14;
    const offsetY = Math.floor(idx / 3) * -14 - 30;

    let m = objectMarkers.get(obj.id);
    if (!m) {
      const group = el("g", { class: "world-object" });
      const text = el("text", { class: "world-object-icon" });
      text.textContent = emojiForObject(obj.object_type);
      group.append(text);
      if (currentTick - obj.created_tick <= 1) group.classList.add("world-object-new");
      layers.objects.append(group);
      m = { group };
      objectMarkers.set(obj.id, m);
    }
    m.group.setAttribute("transform", `translate(${cx + offsetX}, ${cy + offsetY})`);
  }
  for (const [id, m] of objectMarkers) {
    if (seen.has(id)) continue;
    m.group.remove();
    objectMarkers.delete(id);
  }
}

function locColor(loc) {
  if (loc.tipo === "publico" && loc.permite_trabajo) return "#ffba6c";
  if (loc.tipo === "publico") return "#6cc4ff";
  return "#8d8d97";
}

function showLocTooltip(e, loc, tooltip) {
  if (!tooltip) return;
  const objs = (loc.objetos || []).map((o) => o.id).slice(0, 6).join(", ");
  tooltip.textContent =
    `${loc.nombre_display}\n` +
    `${loc.tipo}${loc.permite_trabajo ? " · trabajo" : ""}\n` +
    `objetos: ${objs || "(ninguno)"}`;
  tooltip.classList.remove("hidden");
  tooltip.style.left = (e.offsetX + 12) + "px";
  tooltip.style.top = (e.offsetY + 12) + "px";
}

function showAgentTooltip(e, a) {
  const tooltip = initMap.tooltip;
  if (!tooltip) return;
  const n = a.necesidades || {};
  tooltip.textContent =
    `${a.nombre}\n` +
    `en ${a.ubicacion}\n` +
    `salud ${Math.round(a.salud)} · ${Math.round(a.gleam)}g\n` +
    `hambre ${Math.round(n.hambre || 0)} · energia ${Math.round(n.energia || 0)}\n` +
    (a.in_transit ? `→ ${a.in_transit.destino} (${a.in_transit.ticks_restantes}t)` : "");
  tooltip.classList.remove("hidden");
  tooltip.style.left = (e.offsetX + 12) + "px";
  tooltip.style.top = (e.offsetY + 12) + "px";
}

function hideTooltip(tooltip) {
  if (tooltip) tooltip.classList.add("hidden");
}

// SVG element helper
function el(tag, attrs = {}) {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === undefined || v === null) continue;
    node.setAttribute(k, v);
  }
  return node;
}

// Stash tooltip ref later
export function setTooltip(t) { initMap.tooltip = t; }
