export default function Header() {
  return (
    <div
      className="flex items-center gap-3 px-7 py-4 border-b border-slate-700 flex-shrink-0"
      style={{ background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1a3a6c 100%)' }}
    >
      <span className="text-indigo-300 text-3xl select-none">💼</span>
      <div className="flex flex-col gap-0.5">
        <span className="text-slate-100 font-bold text-xl leading-tight">Bewerbungsplaner</span>
        <span className="text-indigo-300 text-xs">Deine Bewerbungsübersicht</span>
      </div>
    </div>
  )
}
