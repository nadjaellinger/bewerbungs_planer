// table.jsx — sortable list with 3 visual directions: table / log / cards
import { useState } from 'react'
import { STATUS_META, STATUS_ORDER, statusColor } from './data.jsx'
import { StatusBadge, MotivationFlag, fmtDateShort, lastUpdate, agoLabel } from './ui.jsx'

const COLUMNS = [
  { key: "company",  label: "Firma",      sortable: true },
  { key: "position", label: "Position",   sortable: true },
  { key: "status",   label: "Status",     sortable: true },
  { key: "source",   label: "Quelle",     sortable: true },
  { key: "mot",      label: "MS",         sortable: false, title: "Motivationsschreiben" },
  { key: "updated",  label: "Aktualisiert", sortable: true },
];

function sortApps(apps, sortKey, dir) {
  const mult = dir === "asc" ? 1 : -1;
  const val = (a) => {
    switch (sortKey) {
      case "company": return a.company.toLowerCase();
      case "position": return a.position.toLowerCase();
      case "status": return STATUS_META[a.status].stage;
      case "source": return (a.source || "").toLowerCase();
      case "updated": return lastUpdate(a) || "";
      default: return "";
    }
  };
  return [...apps].sort((x, y) => {
    const vx = val(x), vy = val(y);
    if (vx < vy) return -1 * mult;
    if (vx > vy) return 1 * mult;
    return 0;
  });
}

// ---------- classic data table ----------
function DataTable({ apps, onOpen, sortKey, dir, onSort, activeId }) {
  return (
    <div className="tablewrap">
      <table className="apptable">
        <thead>
          <tr>
            <th className="th-idx">#</th>
            {COLUMNS.map(c => (
              <th key={c.key} className={`th-${c.key} ${c.sortable ? "sortable" : ""}`}
                  title={c.title} onClick={c.sortable ? () => onSort(c.key) : undefined}>
                <span className="th-inner">
                  {c.label}
                  {c.sortable && <span className="sort-caret">{sortKey === c.key ? (dir === "asc" ? "▲" : "▼") : "·"}</span>}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {apps.map((a, i) => (
            <tr key={a.id} className={activeId === a.id ? "row-active" : ""} onClick={() => onOpen(a.id)}>
              <td className="td-idx">{String(i + 1).padStart(2, "0")}</td>
              <td className="td-company">
                <span className="co-name">{a.company}</span>
                {a.comments && <span className="has-note" title="Notiz vorhanden">●</span>}
              </td>
              <td className="td-position">{a.position}</td>
              <td className="td-status"><StatusBadge status={a.status} size="sm" /></td>
              <td className="td-source">{a.source || "—"}</td>
              <td className="td-mot"><MotivationFlag on={a.requires_motivation_letter} /></td>
              <td className="td-updated">
                <span className="upd-rel">{agoLabel(lastUpdate(a))}</span>
                <span className="upd-abs">{fmtDateShort(lastUpdate(a))}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {apps.length === 0 && <Empty />}
    </div>
  );
}

// ---------- terminal log lines ----------
function LogView({ apps, onOpen, activeId }) {
  return (
    <div className="logwrap">
      {apps.map((a, i) => {
        const color = statusColor(a.status);
        return (
          <div key={a.id} className={`logline ${activeId === a.id ? "log-active" : ""}`}
               style={{ "--bc": color }} onClick={() => onOpen(a.id)}>
            <span className="log-ts">[{fmtDateShort(lastUpdate(a))}]</span>
            <span className="log-id">APP_{String(a.id).padStart(3, "0")}</span>
            <span className="log-tag" style={{ color }}>{STATUS_META[a.status].short}</span>
            <span className="log-co">{a.company}</span>
            <span className="log-sep">::</span>
            <span className="log-pos">{a.position}</span>
            {a.requires_motivation_letter && <span className="log-mot" title="Motivationsschreiben erforderlich">✉</span>}
            {a.comments && <span className="log-note" title="Notiz vorhanden">#</span>}
            <span className="log-src">{a.source ? `‹${a.source}›` : ""}</span>
          </div>
        );
      })}
      {apps.length === 0 && <Empty />}
    </div>
  );
}

// ---------- card grid ----------
function CardView({ apps, onOpen, activeId }) {
  return (
    <div className="cardgrid">
      {apps.map((a) => {
        const color = statusColor(a.status);
        return (
          <div key={a.id} className={`appcard ${activeId === a.id ? "card-active" : ""}`}
               style={{ "--bc": color }} onClick={() => onOpen(a.id)}>
            <div className="card-top">
              <span className="card-id">APP_{String(a.id).padStart(3, "0")}</span>
              <MotivationFlag on={a.requires_motivation_letter} />
            </div>
            <div className="card-co">{a.company}</div>
            <div className="card-pos">{a.position}</div>
            <div className="card-foot">
              <StatusBadge status={a.status} size="sm" />
            </div>
            <div className="card-meta">
              <span>{a.source || "—"}</span>
              <span>{agoLabel(lastUpdate(a))}</span>
            </div>
          </div>
        );
      })}
      {apps.length === 0 && <Empty />}
    </div>
  );
}

function Empty() {
  return (
    <div className="empty">
      <div className="empty-glyph">▯</div>
      <div className="empty-text">Keine Bewerbungen gefunden.</div>
      <div className="empty-sub">Filter zurücksetzen oder neue Bewerbung hinzufügen.</div>
    </div>
  );
}

function TableView({ direction, apps, onOpen, sortKey, dir, onSort, activeId }) {
  const sorted = sortApps(apps, sortKey, dir);
  if (direction === "log")   return <LogView apps={sorted} onOpen={onOpen} activeId={activeId} />;
  if (direction === "cards") return <CardView apps={sorted} onOpen={onOpen} activeId={activeId} />;
  return <DataTable apps={sorted} onOpen={onOpen} sortKey={sortKey} dir={dir} onSort={onSort} activeId={activeId} />;
}

export { TableView, sortApps, COLUMNS }
