// ui.jsx — shared helpers, badges, and the stats readout
import { useState, useEffect, useRef, useMemo } from 'react'
import { STATUS_META, statusColor } from './data.jsx'

// ---------- date helpers ----------
const MONTHS_DE = ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"];
function fmtDate(iso) {
  if (!iso) return "—";
  const [y, m, d] = iso.split("-").map(Number);
  return `${String(d).padStart(2,"0")}. ${MONTHS_DE[m-1]} ${y}`;
}
function fmtDateShort(iso) {
  if (!iso) return "—";
  const [y, m, d] = iso.split("-").map(Number);
  return `${String(d).padStart(2,"0")}.${String(m).padStart(2,"0")}.${String(y).slice(2)}`;
}
function lastUpdate(app) {
  if (!app.history || !app.history.length) return null;
  return app.history[app.history.length - 1][0];
}
function daysSince(iso) {
  if (!iso) return null;
  const then = new Date(iso + "T00:00:00");
  const now = new Date("2026-04-18T00:00:00"); // "today" anchor for the prototype
  return Math.round((now - then) / 86400000);
}
function agoLabel(iso) {
  const d = daysSince(iso);
  if (d == null) return "—";
  if (d <= 0) return "heute";
  if (d === 1) return "vor 1 Tag";
  if (d < 7) return `vor ${d} Tagen`;
  const w = Math.round(d / 7);
  if (w === 1) return "vor 1 Woche";
  if (d < 60) return `vor ${w} Wochen`;
  return `vor ${Math.round(d/30)} Monaten`;
}

// ---------- status badge ----------
function StatusBadge({ status, size = "md" }) {
  const meta = STATUS_META[status];
  if (!meta) return null;
  const color = statusColor(status);
  return (
    <span className={`badge badge-${size}`} style={{ "--bc": color }}>
      <span className="badge-dot" />
      {meta.label}
    </span>
  );
}

function MotivationFlag({ on, title }) {
  if (!on) return <span className="mot-flag mot-off" title="Kein Motivationsschreiben nötig">·</span>;
  return (
    <span className="mot-flag mot-on" title={title || "Motivationsschreiben erforderlich"}>✉</span>
  );
}

// ---------- stats readout ----------
function StatBlock({ value, label, color }) {
  return (
    <div className="stat-block">
      <div className="stat-value" style={color ? { color } : null}>{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

function Stats({ apps }) {
  const total = apps.length;
  const active = apps.filter(a => STATUS_META[a.status].group === "active").length;
  const interviews = apps.filter(a => ["INVITED_FIRST","INTERVIEWED_FIRST","INVITED_SECOND","INTERVIEWED_SECOND","INVITED_THIRD","INTERVIEWED_THIRD"].includes(a.status)).length;
  const offers = apps.filter(a => a.status === "OFFERED" || a.status === "ACCEPTED").length;
  const rejected = apps.filter(a => a.status === "REJECTED").length;
  // response rate = anything that moved beyond APPLIED at any point / total
  const responded = apps.filter(a => a.history.some(h => h[1] !== "APPLIED")).length;
  const rate = total ? Math.round((responded / total) * 100) : 0;

  // mini distribution bar across pipeline groups
  const dist = [
    { k: "active",  n: active,   c: "var(--c-cyan)" },
    { k: "won",     n: offers,   c: "var(--c-green)" },
    { k: "closed",  n: apps.filter(a => STATUS_META[a.status].group === "closed").length, c: "var(--c-mute)" },
  ];

  return (
    <div className="stats">
      <StatBlock value={total} label="Gesamt" />
      <StatBlock value={active} label="Aktiv" color="var(--c-cyan)" />
      <StatBlock value={interviews} label="In Gesprächen" color="var(--c-amber)" />
      <StatBlock value={offers} label="Angebote" color="var(--c-green)" />
      <StatBlock value={rejected} label="Absagen" color="var(--c-red)" />
      <div className="stat-block stat-rate">
        <div className="stat-value">{rate}<span className="pct">%</span></div>
        <div className="stat-label">Rückmeldequote</div>
        <div className="rate-bar"><div className="rate-fill" style={{ width: rate + "%" }} /></div>
      </div>
    </div>
  );
}

export {
  fmtDate, fmtDateShort, lastUpdate, daysSince, agoLabel,
  StatusBadge, MotivationFlag, Stats, StatBlock,
}
