"""Post-simulation audits.

Different from GM real-time validation. Audits run periodically over
accumulated state to detect WORLD-level coherence problems that single-action
checks cannot catch.

Categories:
  - coherence: artifacts vs world ontology
  - personality: behavior vs agent seed
  - sealed_world: outside-influence detection
  - capability: depth + diversity of agent life
"""
