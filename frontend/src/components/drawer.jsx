// drawer.jsx — per-application detail panel with status-history timeline
import { useEffect } from 'react'
import { STATUS_META, STATUS_ORDER, statusColor } from './data.jsx'
import { StatusBadge, fmtDate, agoLabel } from './ui.jsx'

function Timeline({ history }) {
  if (!history || !history.length) return <div className="tl-empty">Kein Verlauf.</div>;
  return (
    <ol className="timeline">
      {history.map(([date, status], i) => {
        const color = statusColor(status);
        const isLast = i === history.length - 1;
        return (
          <li key={i} className={`tl-item ${isLast ? "tl-current" : ""}`} style={{ "--bc": color }}>
            <span className="tl-node" />
            <div className="tl-body">
              <div className="tl-status" style={{ color }}>{STATUS_META[status].label}</div>
              <div className="tl-date">{fmtDate(date)} <span className="tl-ago">· {agoLabel(date)}</span></div>
            </div>
          </li>
        );
      })}
    </ol>
  );
}

function Field({ label, children, mono }) {
  return (
    <div className="field">
      <div className="field-label">{label}</div>
      <div className={`field-value ${mono ? "mono" : ""}`}>{children}</div>
    </div>
  );
}

function Drawer({ app, onClose, onAdvance, onSetStatus }) {
  useEffect(() => {
    function onKey(e) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  if (!app) return null;
  const color = statusColor(app.status);

  return (
    <div className="drawer-scrim" onClick={onClose}>
      <aside className="drawer" style={{ "--bc": color }} onClick={(e) => e.stopPropagation()}>
        <div className="drawer-head">
          <div className="drawer-head-id">APP_{String(app.id).padStart(3, "0")}</div>
          <button className="drawer-close" onClick={onClose} aria-label="Schließen">[ ESC ]</button>
        </div>

        <div className="drawer-title">
          <h2>{app.company}</h2>
          <div className="drawer-position">{app.position}</div>
          <div className="drawer-badge"><StatusBadge status={app.status} /></div>
        </div>

        <div className="drawer-grid">
          <Field label="Quelle">{app.source || "—"}</Field>
          <Field label="Motivationsschreiben">
            {app.requires_motivation_letter
              ? <span style={{ color: "var(--c-amber)" }}>✉ erforderlich</span>
              : <span style={{ color: "var(--c-mute)" }}>nicht nötig</span>}
          </Field>
          <Field label="Inserat" mono>
            {app.url
              ? <a href={app.url} target="_blank" rel="noreferrer" className="ext-link">{shortUrl(app.url)} ↗</a>
              : "—"}
          </Field>
          <Field label="Schritte">{app.history.length}</Field>
        </div>

        <div className="drawer-section">
          <div className="section-head">// Status ändern</div>
          <div className="status-picker">
            {STATUS_ORDER.map(s => (
              <button key={s} className={`sp-btn ${app.status === s ? "sp-active" : ""}`}
                      style={{ "--bc": statusColor(s) }}
                      onClick={() => onSetStatus(app.id, s)}>
                {STATUS_META[s].label}
              </button>
            ))}
          </div>
        </div>

        <div className="drawer-section">
          <div className="section-head">// Verlauf</div>
          <Timeline history={app.history} />
        </div>

        <div className="drawer-section">
          <div className="section-head">// Notizen</div>
          <div className="drawer-comments">
            {app.comments ? app.comments : <span className="muted">Keine Notizen.</span>}
          </div>
        </div>
      </aside>
    </div>
  );
}

function shortUrl(url) {
  try { const u = new URL(url); return u.hostname.replace(/^www\./, "") + (u.pathname !== "/" ? u.pathname : ""); }
  catch { return url; }
}

export { Drawer, Timeline }
