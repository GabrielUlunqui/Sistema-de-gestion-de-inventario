function stockBadge(item) {
  if (item.out_of_stock) return <span className="badge danger">Sin stock</span>
  if (item.low_stock) return <span className="badge warn">Stock bajo</span>
  return <span className="badge ok">En stock</span>
}

function InventoryTable({ items, onEdit, onDelete }) {
  if (items.length === 0) {
    return <p className="empty">No hay ítems que coincidan con la búsqueda.</p>
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th>SKU</th>
            <th>Categoría</th>
            <th>Marca</th>
            <th className="num">Precio</th>
            <th className="num">Stock</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td className="name">{item.name}</td>
              <td>{item.sku || '—'}</td>
              <td>{item.category || '—'}</td>
              <td>{item.brand || '—'}</td>
              <td className="num">${item.price.toFixed(2)}</td>
              <td className="num">
                <span className="qty">{item.quantity}</span>
              </td>
              <td>{stockBadge(item)}</td>
              <td>
                <div className="actions">
                  <button className="btn" onClick={() => onEdit(item)}>
                    Editar
                  </button>
                  <button
                    className="btn danger"
                    onClick={() => onDelete(item.id)}
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InventoryTable
