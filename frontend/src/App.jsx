import { useCallback, useEffect, useState } from 'react'
import {
  adjustStock,
  createItem,
  deleteItem,
  errorMessage,
  getItems,
  getStats,
  updateItem,
} from './api'
import InventoryTable from './components/InventoryTable'
import ItemForm from './components/ItemForm'
import StatsBar from './components/StatsBar'
import Toast from './components/Toast'
import Toolbar from './components/Toolbar'

function App() {
  const [items, setItems] = useState([])
  const [stats, setStats] = useState(null)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [category, setCategory] = useState('')
  const [brand, setBrand] = useState('')
  const [editing, setEditing] = useState(null)
  const [formOpen, setFormOpen] = useState(false)
  const [toasts, setToasts] = useState([])

  const pushToast = (message, type = 'success') => {
    const id = Date.now()
    setToasts((t) => [...t, { id, message, type }])
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 3500)
  }

  const refresh = useCallback(async () => {
    try {
      const [itemsData, statsData] = await Promise.all([
        getItems({
          search: search || undefined,
          status: status || undefined,
          category: category || undefined,
          brand: brand || undefined,
        }),
        getStats(),
      ])
      setItems(itemsData)
      setStats(statsData)
    } catch (err) {
      pushToast(errorMessage(err), 'error')
    }
  }, [search, status, category, brand])

  useEffect(() => {
    const timer = setTimeout(refresh, 250)
    return () => clearTimeout(timer)
  }, [refresh])

  const handleSave = async (data) => {
    try {
      if (editing) {
        await updateItem(editing.id, data)
        pushToast('Ítem actualizado')
      } else {
        await createItem(data)
        pushToast('Ítem agregado')
      }
      setFormOpen(false)
      setEditing(null)
      refresh()
    } catch (err) {
      pushToast(errorMessage(err), 'error')
    }
  }

  const handleAdjust = async (id, delta) => {
    try {
      await adjustStock(id, delta)
      refresh()
    } catch (err) {
      pushToast(errorMessage(err), 'error')
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteItem(id)
      pushToast('Ítem eliminado')
      refresh()
    } catch (err) {
      pushToast(errorMessage(err), 'error')
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📦 Gestión de Inventario</h1>
      </header>

      <StatsBar stats={stats} />

      <Toolbar
        search={search}
        onSearch={setSearch}
        status={status}
        onStatus={setStatus}
        category={category}
        onCategory={setCategory}
        brand={brand}
        onBrand={setBrand}
        brands={stats?.brands ?? []}
        onAdd={() => {
          setEditing(null)
          setFormOpen(true)
        }}
      />

      <InventoryTable
        items={items}
        onAdjust={handleAdjust}
        onEdit={(item) => {
          setEditing(item)
          setFormOpen(true)
        }}
        onDelete={handleDelete}
      />

      {formOpen && (
        <ItemForm
          item={editing}
          onSave={handleSave}
          onClose={() => {
            setFormOpen(false)
            setEditing(null)
          }}
        />
      )}

      <Toast toasts={toasts} />
    </div>
  )
}

export default App
