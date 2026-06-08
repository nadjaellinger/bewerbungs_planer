import type { Application } from '../types/application'
import { ACTIVE_STATUSES } from '../config/statusConfig'

interface Props {
  applications: Application[]
}

interface TileProps {
  label: string
  value: number
  bg: string
  iconColor: string
  icon: string
}

function Tile({ label, value, bg, iconColor, icon }: TileProps) {
  return (
    <div
      className="flex items-center gap-3 px-4 py-3 rounded-xl border border-slate-700 min-w-[105px]"
      style={{ background: bg }}
    >
      <span style={{ color: iconColor, fontSize: '1.6rem', lineHeight: 1 }}>{icon}</span>
      <div className="flex flex-col gap-0">
        <span className="text-slate-100 font-bold text-2xl leading-none">{value}</span>
        <span className="text-slate-400 text-[0.65rem] uppercase tracking-wider">{label}</span>
      </div>
    </div>
  )
}

export default function StatsBar({ applications }: Props) {
  const total    = applications.length
  const active   = applications.filter(a => ACTIVE_STATUSES.includes(a.status)).length
  const offers   = applications.filter(a => a.status === 'OFFERED').length
  const accepted = applications.filter(a => a.status === 'ACCEPTED').length
  const rejected = applications.filter(a => a.status === 'REJECTED').length

  return (
    <div className="flex flex-wrap gap-3 px-7 py-4">
      <Tile label="Gesamt"     value={total}    icon="🗂️" bg="rgba(99,102,241,0.18)"  iconColor="#818cf8" />
      <Tile label="Aktiv"      value={active}   icon="📈" bg="rgba(245,158,11,0.18)"  iconColor="#fbbf24" />
      <Tile label="Angebote"   value={offers}   icon="🎉" bg="rgba(13,148,136,0.18)"  iconColor="#2dd4bf" />
      <Tile label="Angenommen" value={accepted} icon="✅" bg="rgba(34,197,94,0.18)"   iconColor="#86efac" />
      <Tile label="Abgelehnt"  value={rejected} icon="❌" bg="rgba(239,68,68,0.15)"   iconColor="#f87171" />
    </div>
  )
}
