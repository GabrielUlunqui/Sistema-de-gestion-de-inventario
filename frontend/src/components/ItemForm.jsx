import { useState } from 'react'
import { BRAND_SUGGESTIONS, CATEGORIES } from '../constants'

const EMPTY = {
  name: '',
  sku: '',
  category: '',
  brand: '',
  quantity: 0,
  price: 0,
  min_stock: 5,
}

function ItemForm({ item, onSave, onClose }) {
  const [form, setForm] = useState(
    item
      ? {
          name: item.name,
          sku: item.sku ?? '',
          category: item.category ?? '',
          brand: item.brand ?? '',
          quantity: item.quantity,
          price: item.price,
          min_stock: item.min_stock,
        }
      : EMPTY
  )
  const [error, setError] = useState('')

  const brandSuggestions = BRAND_SUGGESTIONS[form.category] ?? []

  const set = (field) => (e) =>
    setForm((f) => ({ ...f, [field]: e.target.value }))

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.name.trim()) {
      setError('El nombre es obligatorio.')
      return
    }
    const quantity = Number(form.quantity)
    const price = Number(form.price)
    const minStock = Number(form.min_stock)
    if (quantity < 0 || price < 0 || minStock < 0) {
      setError('Los valores no pueden ser negativos.')
      return
    }
    const payload = {
      name: form.name.trim(),
      sku: form.sku.trim() || null,
      category: form.category.trim() || null,
      brand: form.brand.trim() || null,
      price,
      min_stock: minStock,
      ...(item ? {} : { quantity }),
    }
    onSave(payload)
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{item ? 'Editar ítem' : 'Agregar ítem'}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Nombre *
            <input value={form.name} onChange={set('name')} autoFocus />
          </label>
          <div className="form-row">
            <label>
              Categoría
              <input
                list="category-options"
                value={form.category}
                onChange={set('category')}
                placeholder="Ej: Cámaras"
              />
              <datalist id="category-options">
                {CATEGORIES.map((c) => (
                  <option key={c} value={c} />
                ))}
              </datalist>
            </label>
            <label>
              Marca
              <input
                list="brand-options"
                value={form.brand}
                onChange={set('brand')}
                placeholder={
                  form.category === 'Sensores'
                    ? 'DSC, Paradox, Hikvision...'
                    : 'Ej: Hikvision'
                }
              />
              <datalist id="brand-options">
                {brandSuggestions.map((b) => (
                  <option key={b} value={b} />
                ))}
              </datalist>
            </label>
          </div>
          <div className="form-row">
            <label>
              SKU
              <input value={form.sku} onChange={set('sku')} />
            </label>
            <label>
              Precio
              <input
                type="number"
                min="0"
                step="0.01"
                value={form.price}
                onChange={set('price')}
              />
            </label>
          </div>
          <div className="form-row">
            {!item && (
              <label>
                Stock inicial
                <input
                  type="number"
                  min="0"
                  value={form.quantity}
                  onChange={set('quantity')}
                />
              </label>
            )}
            <label>
              Stock mínimo
              <input
                type="number"
                min="0"
                value={form.min_stock}
                onChange={set('min_stock')}
              />
            </label>
          </div>
          {error && <p className="form-error">{error}</p>}
          <div className="form-actions">
            <button type="button" className="btn" onClick={onClose}>
              Cancelar
            </button>
            <button type="submit" className="btn primary">
              {item ? 'Guardar cambios' : 'Agregar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ItemForm
