"""LLM gateway with disk cache + audit log.

Day 1: stub mode (no real API calls — returns canned responses).
Day 2+: enable real Anthropic + Gemini + Cerebras backends.

Tiers (PLAN_v4.md §14.1):
  - leader   → Claude Sonnet 4.6  (decision + drama)
  - crowd    → Claude Haiku 4.5   (NPCs ambientales, post-MVP)
  - content  → Claude Sonnet 4.6  (WRITE_BOOK / WRITE_CODE generation)
  - narrator → Gemini Flash 2.0   (crónica + diarios batch)
  - micro    → Gemini Flash 2.0   (trigger 3 observación)
  - fallback → Cerebras Llama 3.3 70B (free, if APIs down)
"""
import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from ..db.session import get_session
from ..db.schema import LLMCallLog


log = logging.getLogger("llm")

Tier = Literal["leader", "crowd", "content", "narrator", "micro"]

MODEL_BY_TIER: dict[str, str] = {
    "leader":   "claude-sonnet-4-6",
    "crowd":    "claude-haiku-4-5-20251001",
    "content":  "claude-sonnet-4-6",
    "narrator": "gemini-2.0-flash",
    "micro":    "gemini-2.0-flash",
}

FALLBACK_MODEL = "cerebras-llama-3.3-70b"


@dataclass
class LLMResult:
    text: str
    model: str
    tier: str
    cached: bool
    latency_ms: int


class LLMGateway:
    def __init__(self, cache_dir: str | None = None, stub_mode: bool | None = None):
        self.cache_dir = Path(cache_dir or os.getenv("LLM_CACHE_DIR", "./artifacts/cache"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Stub mode auto-enabled when no API keys present (Day 1 default).
        if stub_mode is None:
            stub_mode = not (os.getenv("ANTHROPIC_API_KEY") and os.getenv("GEMINI_API_KEY"))
        self.stub_mode = stub_mode
        if self.stub_mode:
            log.info("LLMGateway: stub_mode ENABLED (no API keys or forced).")

    def _hash(self, model: str, prompt: str) -> str:
        return hashlib.sha256(f"{model}::{prompt}".encode("utf-8")).hexdigest()[:32]

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def call(self, prompt: str, tier: Tier, max_tokens: int = 1024) -> LLMResult:
        model = MODEL_BY_TIER[tier]
        key = self._hash(model, prompt)
        cp = self._cache_path(key)

        # Cache hit
        if cp.exists():
            data = json.loads(cp.read_text(encoding="utf-8"))
            self._log_call(model, tier, key, was_cached=True, latency_ms=0)
            return LLMResult(text=data["text"], model=model, tier=tier, cached=True, latency_ms=0)

        # Miss → call API (or stub)
        start = time.time()
        if self.stub_mode:
            text = self._stub_response(tier, prompt)
        else:
            try:
                text = self._call_real(model, prompt, max_tokens)
            except Exception as e:
                log.warning("primary model %s failed (%s), falling back to %s", model, e, FALLBACK_MODEL)
                text = self._call_real(FALLBACK_MODEL, prompt, max_tokens)
                model = FALLBACK_MODEL
        latency_ms = int((time.time() - start) * 1000)

        cp.write_text(json.dumps({"text": text, "model": model}), encoding="utf-8")
        self._log_call(model, tier, key, was_cached=False, latency_ms=latency_ms)
        return LLMResult(text=text, model=model, tier=tier, cached=False, latency_ms=latency_ms)

    def _stub_response(self, tier: str, prompt: str) -> str:
        """Day 1 stub: canned responses to allow loop testing without API costs."""
        if tier in ("leader", "crowd"):
            # Return canned JSON action
            return json.dumps({
                "type": "REFLECT",
                "params": {"prompt_interno": "pensar que hacer despues"}
            })
        if tier == "content":
            return "[stub content — real LLM disabled in day 1]"
        if tier == "narrator":
            return "Pasaron cosas. La ciudad sigue."
        if tier == "micro":
            return "observado."
        return "stub."

    def _call_real(self, model: str, prompt: str, max_tokens: int) -> str:
        if model.startswith("claude-"):
            return self._call_anthropic(model, prompt, max_tokens)
        if model.startswith("gemini-"):
            return self._call_gemini(model, prompt, max_tokens)
        if model.startswith("cerebras-"):
            return self._call_cerebras(model, prompt, max_tokens)
        raise ValueError(f"unknown model {model}")

    def _call_anthropic(self, model: str, prompt: str, max_tokens: int) -> str:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text

    def _call_gemini(self, model: str, prompt: str, max_tokens: int) -> str:
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        gmodel = genai.GenerativeModel(model)
        resp = gmodel.generate_content(prompt, generation_config={"max_output_tokens": max_tokens})
        return resp.text

    def _call_cerebras(self, model: str, prompt: str, max_tokens: int) -> str:
        # Stubbed for Day 1; wire SDK on Day 2.
        raise NotImplementedError("cerebras backend pending Day 2")

    def _log_call(self, model: str, tier: str, key: str, was_cached: bool, latency_ms: int) -> None:
        try:
            with get_session() as s:
                s.add(LLMCallLog(
                    model=model, tier=tier, prompt_hash=key,
                    latency_ms=latency_ms, was_cached=was_cached,
                ))
                s.commit()
        except Exception as e:
            log.warning("LLMCallLog write failed: %s", e)
