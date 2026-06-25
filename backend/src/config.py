"""Shared configuration constants loaded from environment."""
import os

MEMORIA_RECENT_CAP = int(os.getenv("MEMORIA_RECENT_CAP", "30"))
TICK_DURATION_SEC = int(os.getenv("TICK_DURATION_SEC", "30"))
MAP_ID = os.getenv("MAP_ID", "moderno")
