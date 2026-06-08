// addform.jsx — modal to create a new application
import { useState } from 'react'
import { STATUS_META, STATUS_ORDER } from './data.jsx'

function AddForm({ onAdd, onClose }) {
  const [company, setCompany] = useState("");
  const [position, setPosition] = useState("");
  const [url, setUrl] = useState("");
  const [source, setSource] = useState("");
  const [status, setStatus] = useState("APPLIED");
  const [comments, setComments] = useState("");
  const [mot, setMot] = useState(false);
  const [err, setErr] = useState("");

  function submit(e) {
    e.preventDefault();
    if (!company.trim() || !position.trim()) {
      setErr("Firma und Position sind erforderlich.");
      return;
    }
    onAdd({
      company: company.trim(),
      position: position.trim(),
      url: url.trim() || null,
      source: source.trim() || null,
      status,
      comments: comments.trim() || null,
      requires_motivation_letter: mot,
    });
  }

  return (
    <div className="drawer-scrim" onClick={onClose}>
      <aside className="drawer addform" onClick={(e) => e.stopPropagation()}>
        <div className="drawer-head">
          <div className="drawer-head-id">// NEUE BEWERBUNG</div>
          <button className="drawer-close" onClick={onClose} aria-label="Schließen">[ ESC ]</button>
        </div>

        <form onSubmit={submit} className="form">
          <label className="form-row">
            <span className="form-label">Firma <em>*</em></span>
            <input className="input" value={company} onChange={e => setCompany(e.target.value)} autoFocus placeholder="z. B. Helios Systems" />
          </label>
          <label className="form-row">
            <span className="form-label">Position <em>*</em></span>
            <input className="input" value={position} onChange={e => setPosition(e.target.value)} placeholder="z. B. Backend Engineer" />
          </label>
          <label className="form-row">
            <span className="form-label">Status</span>
            <select className="input" value={status} onChange={e => setStatus(e.target.value)}>
              {STATUS_ORDER.map(s => <option key={s} value={s}>{STATUS_META[s].label}</option>)}
            </select>
          </label>
          <div className="form-2col">
            <label className="form-row">
              <span className="form-label">Quelle</span>
              <input className="input" value={source} onChange={e => setSource(e.target.value)} placeholder="LinkedIn …" />
            </label>
            <label className="form-row form-check">
              <span className="form-label">Motivationsschreiben</span>
              <button type="button" className={`toggle ${mot ? "toggle-on" : ""}`} onClick={() => setMot(m => !m)}>
                <span className="toggle-knob" />
                <span className="toggle-text">{mot ? "erforderlich" : "nicht nötig"}</span>
              </button>
            </label>
          </div>
          <label className="form-row">
            <span className="form-label">Inserat-URL</span>
            <input className="input" value={url} onChange={e => setUrl(e.target.value)} placeholder="https://…" />
          </label>
          <label className="form-row">
            <span className="form-label">Notizen</span>
            <textarea className="input" rows={3} value={comments} onChange={e => setComments(e.target.value)} placeholder="Optionale Notizen …" />
          </label>

          {err && <div className="form-err">! {err}</div>}

          <div className="form-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>Abbrechen</button>
            <button type="submit" className="btn btn-primary">+ Hinzufügen</button>
          </div>
        </form>
      </aside>
    </div>
  );
}

export { AddForm }
