export const RISK_THRESHOLDS = {
  LOW: 0.30,
  HIGH: 0.70
};

export const CUMULATIVE_THRESHOLD = 1.0;

export const getRiskColor = (score) => {
  if (score < RISK_THRESHOLDS.LOW) return 'text-green-500';
  if (score < RISK_THRESHOLDS.HIGH) return 'text-orange-500';
  return 'text-red-500';
};

export const getRiskBgColor = (score) => {
  if (score < RISK_THRESHOLDS.LOW) return 'bg-green-100 text-green-700';
  if (score < RISK_THRESHOLDS.HIGH) return 'bg-orange-100 text-orange-700';
  return 'bg-red-100 text-red-700';
};
