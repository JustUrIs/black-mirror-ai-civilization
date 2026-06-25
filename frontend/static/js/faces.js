// Map emotional_state + needs + alive to an emoji face.
// Order matters: most-extreme first.

export function faceFor(agent) {
  if (!agent.alive) return "💀";

  const n = agent.necesidades || {};
  const e = agent.emotional_state || {};
  const salud = agent.salud ?? 100;

  if (salud <= 30) return "🤕";
  if ((n.hambre ?? 0) >= 85) return "🥺";
  if ((n.sed ?? 0) >= 85) return "😓";
  if ((n.energia ?? 100) <= 20) return "😴";

  if ((e.miedo ?? 0) >= 60) return "😨";
  if ((e.verguenza ?? 0) >= 70) return "😳";
  if ((e.tristeza ?? 0) >= 70 || (e.animo ?? 50) < 25) return "😔";
  if ((e.ira ?? 0) >= 60) return "😠";

  if ((e.dignidad ?? 70) >= 85 && (e.animo ?? 50) >= 60) return "😌";
  if ((e.asombro ?? 30) >= 70) return "😲";
  if ((e.animo ?? 50) >= 70 && (e.miedo ?? 0) < 30) return "🙂";
  if ((e.soledad ?? 30) >= 70) return "🥲";

  if ((e.animo ?? 50) >= 40) return "😐";
  return "😟";
}

export function emojiForObject(t) {
  return ({
    piedra: "🪨",
    arbol_frutal: "🌳",
    fruta: "🍎",
    pan: "🥖",
    agua_extra: "💧",
    libro_extraño: "📕",
    libro_extrano: "📕",
  })[t] || "❓";
}

export const AGENT_COLORS = {
  borges:   "#ff8289",
  socrates: "#6fdc8c",
  arendt:   "#6cc4ff",
  alice:    "#ff8289",
  bob:      "#6fdc8c",
  carla:    "#6cc4ff",
  diego:    "#ffba6c",
};

export function colorFor(id) { return AGENT_COLORS[id] || "#d6d6dc"; }
