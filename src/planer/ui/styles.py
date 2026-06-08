class Theme:
    """Zentrales Farbschema – Darkmode, Indigo als Primär-, Amber als Warn-Akzent."""

    # ── Hintergründe ──────────────────────────────────────────────────────────
    PAGE       = "#0f172a"   # slate-900
    SURFACE    = "#1e293b"   # slate-800
    SURFACE_HI = "#243650"   # Hover

    # ── Rahmen ────────────────────────────────────────────────────────────────
    BORDER     = "#334155"   # slate-700
    BORDER_SUB = "#1e293b"   # Tabellentrennlinie

    # ── Text ──────────────────────────────────────────────────────────────────
    TEXT       = "#f1f5f9"
    TEXT_SUB   = "#94a3b8"
    TEXT_MUTED = "#64748b"

    # ── Akzentfarben ─────────────────────────────────────────────────────────
    INDIGO     = "#6366f1"
    INDIGO_DIM = "rgba(99,102,241,0.18)"
    AMBER      = "#f59e0b"
    AMBER_DIM  = "rgba(245,158,11,0.18)"
    TEAL       = "#0d9488"
    TEAL_DIM   = "rgba(13,148,136,0.18)"
    GREEN      = "#22c55e"
    GREEN_DIM  = "rgba(34,197,94,0.18)"
    RED        = "#ef4444"
    RED_DIM    = "rgba(239,68,68,0.15)"

    # ── Header ────────────────────────────────────────────────────────────────
    HEADER_GRADIENT = "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1a3a6c 100%)"

    # ── Stat-Kacheln: (bg, icon-color)  –  Teal für Angebote, Grün für Angenommen
    STAT: dict[str, tuple[str, str]] = {
        "total":    ("rgba(99,102,241,0.18)",  "#818cf8"),
        "active":   ("rgba(245,158,11,0.18)",  "#fbbf24"),
        "offers":   ("rgba(13,148,136,0.18)",  "#2dd4bf"),
        "accepted": ("rgba(34,197,94,0.18)",   "#86efac"),
        "rejected": ("rgba(239,68,68,0.15)",   "#f87171"),
    }

    # ── Globales CSS ──────────────────────────────────────────────────────────
    GLOBAL_CSS = """
        .nicegui-content { padding: 0 !important; }
        .bp-card { transition: filter 0.15s ease; cursor: default; }
        .bp-card:hover { filter: brightness(1.10); }
        .bp-table .q-table__top { display: none; }
        .bp-table thead tr th {
            background: #0a1120 !important;
            color: #64748b !important;
            font-size: 0.7rem !important;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            font-weight: 700;
            padding: 10px 16px !important;
            border-bottom: 1px solid #334155 !important;
        }
        .bp-table tbody tr td {
            background: #1e293b;
            border-bottom: 1px solid #1a2a3a !important;
            color: #cbd5e1;
            font-size: 0.84rem;
            padding: 9px 16px !important;
        }
        .bp-table tbody tr:hover td { background: #243650 !important; }
        .bp-table .q-table { border: 1px solid #334155 !important; border-radius: 12px !important; }
    """

    @classmethod
    def card(cls) -> str:
        return (
            f"background:{cls.SURFACE}; "
            f"border:1px solid {cls.BORDER}; "
            "border-radius:12px; overflow:hidden"
        )
