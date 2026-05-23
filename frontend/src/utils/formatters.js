import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

export const formatDateTime = (dateString) => {
  if (!dateString) return ''
  return format(new Date(dateString), 'HH:mm', { locale: ru })
}

export const formatFullDate = (dateString) => {
  if (!dateString) return ''
  return format(new Date(dateString), 'd MMMM yyyy, HH:mm', { locale: ru })
}

export const formatPercent = (value) => {
  return (value * 100).toFixed(0) + '%'
}

export const truncateId = (id) => {
  if (!id) return ''
  return id.substring(0, 8) + '...'
}
