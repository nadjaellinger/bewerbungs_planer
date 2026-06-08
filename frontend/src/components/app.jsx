// app.jsx — Bewerbungsplaner main application
import { useState as uS, useEffect as uE, useMemo as uM } from 'react'
import { STATUS_META, STATUS_ORDER, useApplications } from './data.jsx'
import { Stats, fmtDateShort } from './ui.jsx'
import { TableView } from './table.jsx'
import { Drawer } from './drawer.jsx'
import { AddForm } from './addform.jsx'
import { useTweaks, TweaksPanel, TweakSection, TweakToggle, TweakRadio, TweakColor } from './tweaks-panel.jsx'

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "tableDirection": "table",
  "phosphor": "magenta",
  "grid": false,
  "scanlines": true,
  "glow": true
}/*EDITMODE-END*/;

const PHOSPHOR = {
  magenta: { phosphor: "#ff2e97", soft: "#ff8ad0" },
  cyan:    { phosphor: "#25e7ff", soft: "#9bf1ff" },
  purple:  { phosphor: "#b066ff", soft: "#d6aaff" },
};

const FILTERS = [
  { key: "all",    label: "Alle",        test: () => true },
  { key: "active", label: "Aktiv",       test: a => STATUS_META[a.status].group === "active" },
  { key: "talks",  label: "In Gesprächen", test: a => ["INVITED_FIRST","INTERVIEWED_FIRST","INVITED_SECOND","INTERVIEWED_SECOND","INVITED_THIRD","INTERVIEWED_THIRD"].includes(a.status) },
  { key: "offers", label: "Angebote",    test: a => ["OFFERED","ACCEPTED"].includes(a.status) },
  { key: "closed", label: "Abgeschlossen", test: a => STATUS_META[a.status].group === "closed" },
  { key: "mot",    label: "✉ Motivationsschr.", test: a => a.requires_motivation_letter },
];

const TODAY = "2026-04-18";

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const { apps: initialApps, loading, error } = useApplications()
  const [apps, setApps] = uS([])
  const [query, setQuery] = uS("");
  const [filter, setFilter] = uS("all");
  const [sortKey, setSortKey] = uS("updated");
  const [dir, setDir] = uS("desc");
  const [selId, setSelId] = uS(null);
  const [addOpen, setAddOpen] = uS(false);

  // Daten von API übernehmen sobald geladen
  uE(() => { if (initialApps.length) setApps(initialApps) }, [initialApps])

  // apply theme vars
  uE(() => {
    const ph = PHOSPHOR[t.phosphor] || PHOSPHOR.magenta;
    const root = document.documentElement;
    root.style.setProperty("--c-phosphor", ph.phosphor);
    root.style.setProperty("--c-phosphor-soft", ph.soft);
    document.body.classList.toggle("no-grid", !t.grid);
    document.body.classList.toggle("no-scanlines", !t.scanlines);
    document.body.classList.toggle("no-glow", !t.glow);
  }, [t.phosphor, t.grid, t.scanlines, t.glow]);

  const filtered = uM(() => {
    const f = FILTERS.find(x => x.key === filter) || FILTERS[0];
    const q = query.trim().toLowerCase();
    return apps.filter(a => f.test(a) && (
      !q || a.company.toLowerCase().includes(q) || a.position.toLowerCase().includes(q) || (a.source||"").toLowerCase().includes(q)
    ));
  }, [apps, filter, query]);

  function onSort(key) {
    if (key === sortKey) setDir(d => d === "asc" ? "desc" : "asc");
    else { setSortKey(key); setDir(key === "updated" ? "desc" : "asc"); }
  }

  function setStatus(id, status) {
    setApps(prev => prev.map(a => {
      if (a.id !== id) return a;
      if (a.status === status) return a;
      const hist = [...a.history, [TODAY, status]];
      return { ...a, status, history: hist };
    }));
  }

  function addApp(data) {
    setApps(prev => {
      const id = Math.max(0, ...prev.map(a => a.id)) + 1;
      return [{ id, ...data, history: [[TODAY, data.status]] }, ...prev];
    });
    setAddOpen(false);
  }

  const selected = apps.find(a => a.id === selId) || null;

  return (
    <div className="app">
      <div className="synth-grid" />
      <div className="synth-horizon" />
      <div className="crt-overlay" />
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" />
          <span className="brand-word">BEWERBUNGS<span className="brand-accent">PLANER</span></span>
          <span className="brand-ver">v1.0 · {filtered.length}/{apps.length} aktiv</span>
        </div>
        <button className="btn btn-primary btn-add" onClick={() => setAddOpen(true)}>+ Neue Bewerbung</button>
      </header>

      <Stats apps={apps} />

      <div className="controls">
        <div className="search">
          <span className="search-prompt">&gt;</span>
          <input className="search-input" value={query} onChange={e => setQuery(e.target.value)}
                 placeholder="suche firma, position, quelle …" />
          {query && <button className="search-clear" onClick={() => setQuery("")}>✕</button>}
          <span className="search-caret" />
        </div>
        <div className="filters">
          {FILTERS.map(f => {
            const n = apps.filter(f.test).length;
            return (
              <button key={f.key} className={`chip ${filter === f.key ? "chip-on" : ""}`} onClick={() => setFilter(f.key)}>
                {f.label}<span className="chip-n">{n}</span>
              </button>
            );
          })}
        </div>
      </div>

      <main className="content">
        <TableView direction={t.tableDirection} apps={filtered} onOpen={setSelId}
                   sortKey={sortKey} dir={dir} onSort={onSort} activeId={selId} />
      </main>

      <footer className="footer">
        <span>BEWERBUNGSPLANER // {apps.length} EINTRÄGE</span>
        <span className="blink">█</span>
        <span>STAND {fmtDateShort(TODAY)}</span>
      </footer>

      {selected && <Drawer app={selected} onClose={() => setSelId(null)} onSetStatus={setStatus} />}
      {addOpen && <AddForm onAdd={addApp} onClose={() => setAddOpen(false)} />}

      <TweaksPanel>
        <TweakSection label="Darstellung" />
        <TweakRadio label="Tabellen-Stil" value={t.tableDirection}
                    options={["table", "log", "cards"]}
                    onChange={v => setTweak("tableDirection", v)} />
        <TweakSection label="Synthwave" />
        <TweakColor label="Neon-Akzent" value={PHOSPHOR[t.phosphor].phosphor}
                    options={[PHOSPHOR.magenta.phosphor, PHOSPHOR.cyan.phosphor, PHOSPHOR.purple.phosphor]}
                    onChange={(v) => {
                      const key = Object.keys(PHOSPHOR).find(k => PHOSPHOR[k].phosphor === v) || "magenta";
                      setTweak("phosphor", key);
                    }} />
        <TweakToggle label="Neon-Raster" value={t.grid} onChange={v => setTweak("grid", v)} />
        <TweakToggle label="Scanlines" value={t.scanlines} onChange={v => setTweak("scanlines", v)} />
        <TweakToggle label="Neon-Glühen" value={t.glow} onChange={v => setTweak("glow", v)} />
      </TweaksPanel>
    </div>
  );
}

export default App
