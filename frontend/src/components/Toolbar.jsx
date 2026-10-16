import { CATEGORIES } from '../constants'

function Toolbar({
  search,
  onSearch,
  status,
  onStatus,
  category,
  onCategory,
  brand,
  onBrand,
  brands,
  onAdd,
}) {
  return (
    <div className="toolbar">
      <input
        type="text"
        className="search-input"
        placeholder="Buscar por nombre, SKU, categoría o marca..."
        value={search}
        onChange={(e) => onSearch(e.target.value)}
      />

      <select value={category} onChange={(e) => onCategory(e.target.value)}>
        <option value="">Todas las categorías</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>

      <select value={brand} onChange={(e) => onBrand(e.target.value)}>
        <option value="">Todas las marcas</option>
        {brands.map((b) => (
          <option key={b} value={b}>
            {b}
          </option>
        ))}
      </select>

      <select value={status} onChange={(e) => onStatus(e.target.value)}>
        <option value="">Todos los estados</option>
        <option value="ok">En stock</option>
        <option value="low">Stock bajo</option>
        <option value="out">Sin stock</option>
      </select>

      <button className="btn primary" onClick={onAdd}>
        + Agregar ítem
      </button>
    </div>
  )
}

export default Toolbar
