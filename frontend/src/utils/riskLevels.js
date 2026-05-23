export const RISK_THRESHOLDS = {
  LOW: 0.30,
  HIGH: 0.70
}

export const CUMULATIVE_THRESHOLD = 1.0

export const getRiskColor = (score) => {
  if (score < RISK_THRESHOLDS.LOW) return 'text-green-600'
  if (score < RISK_THRESHOLDS.HIGH) return 'text-amber-600'
  return 'text-red-600'
}

export const getRiskBgColor = (score) => {
  if (score < RISK_THRESHOLDS.LOW) return 'bg-green-50 text-green-700'
  if (score < RISK_THRESHOLDS.HIGH) return 'bg-amber-50 text-amber-700'
  return 'bg-red-50 text-red-700'
}
