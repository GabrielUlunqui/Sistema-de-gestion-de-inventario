import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getItems = (params = {}) =>
  api.get('/items/', { params }).then((r) => r.data)

export const getStats = () => api.get('/stats/').then((r) => r.data)

export const createItem = (item) => api.post('/items/', item).then((r) => r.data)

export const updateItem = (id, item) =>
  api.put(`/items/${id}`, item).then((r) => r.data)

export const adjustStock = (id, delta) =>
  api.patch(`/items/${id}/stock`, { delta }).then((r) => r.data)

export const deleteItem = (id) => api.delete(`/items/${id}`)

export const errorMessage = (err) =>
  err.response?.data?.detail?.[0]?.msg ||
  err.response?.data?.detail ||
  'Error de conexión con el servidor'
