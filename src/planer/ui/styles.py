class Theme:
    """Zentrales Farbschema – Darkmode mit Indigo & Amber als Highlight-Farben."""

    # ── Hintergründe ──────────────────────────────────────────────────────────
    PAGE       = "#0f172a"   # slate-900  – Seitenhintergrund
    SURFACE    = "#1e293b"   # slate-800  – Kacheln / Panels
    SURFACE_HI = "#293b50"   # slate-750  – Hover / erhöhte Flächen

    # ── Rahmen ────────────────────────────────────────────────────────────────
    BORDER     = "#334155"   # slate-700

    # ── Text ──────────────────────────────────────────────────────────────────
    TEXT       = "#f1f5f9"   # slate-100  – Primär
    TEXT_SUB   = "#94a3b8"   # slate-400  – Sekundär
    TEXT_MUTED = "#64748b"   # slate-500  – Gedimmt

    # ── Highlight-Farben ──────────────────────────────────────────────────────
    INDIGO     = "#6366f1"               # Akzent-Primär
    INDIGO_DIM = "rgba(99,102,241,0.20)"
    AMBER      = "#f59e0b"               # Akzent-Sekundär / Warnhinweise
    AMBER_DIM  = "rgba(245,158,11,0.20)"
    GREEN      = "#10b981"
    GREEN_DIM  = "rgba(16,185,129,0.20)"
    RED        = "#ef4444"
    RED_DIM    = "rgba(239,68,68,0.20)"

    # ── Header-Verlauf ────────────────────────────────────────────────────────
    HEADER_GRADIENT = "linear-gradient(135deg, #1e1b4b 0%, #312e81 55%, #1a3a6c 100%)"

    # ── Statistik-Kacheln: (Hintergrund, Icon-Farbe) ──────────────────────────
    STAT: dict[str, tuple[str, str]] = {
        "total":    ("rgba(99,102,241,0.20)",  "#818cf8"),
        "active":   ("rgba(245,158,11,0.20)",  "#fbbf24"),
        "offers":   ("rgba(16,185,129,0.20)",  "#34d399"),
        "accepted": ("rgba(16,185,129,0.15)",  "#10b981"),
        "rejected": ("rgba(239,68,68,0.15)",   "#f87171"),
    }

    @classmethod
    def card(cls) -> str:
        """CSS-Inlinestil für eine dunkle Kachel."""
        return (
            f"background:{cls.SURFACE}; "
            f"border:1px solid {cls.BORDER}; "
            "border-radius:14px; overflow:hidden"
        )
