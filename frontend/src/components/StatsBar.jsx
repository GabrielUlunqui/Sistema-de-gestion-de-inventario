function StatsBar({ stats }) {
  const cards = [
    { label: 'Productos', value: stats?.total_items ?? '—', cls: '' },
    { label: 'Unidades totales', value: stats?.total_units ?? '—', cls: '' },
    {
      label: 'Valor del stock',
      value: stats ? `$${stats.total_value.toLocaleString('es-AR')}` : '—',
      cls: '',
    },
    { label: 'Stock bajo', value: stats?.low_stock_count ?? '—', cls: 'warn' },
    { label: 'Sin stock', value: stats?.out_of_stock_count ?? '—', cls: 'danger' },
  ]

  return (
    <div className="stats-bar">
      {cards.map((c) => (
        <div key={c.label} className={`stat-card ${c.cls}`}>
          <span className="stat-value">{c.value}</span>
          <span className="stat-label">{c.label}</span>
        </div>
      ))}
    </div>
  )
}

export default StatsBar
