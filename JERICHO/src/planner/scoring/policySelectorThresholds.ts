export const POLICY_SELECTOR_THRESHOLDS = {
  milestoneRiskHigh: 160,
  deadlineRiskHigh: 160,
  dependencyRiskHigh: 80,
  depTightCountHigh: 2,
  contextSwitchCountHigh: 6,
  deadlineRiskLow: 70,
  deadlineRiskMid: 110,
  milestoneRiskLow: 70,
  milestoneRiskMid: 110,
  outsideHorizonMinHigh: 180,
  deferralPenaltyHigh: 60,
  switchDeltaDeadlineRisk: 20,
  switchDeltaMilestoneRisk: 20,
  switchDeltaDependencyRisk: 20,
  switchDeltaContext: 2
} as const;

export type PolicySelectorThresholds = typeof POLICY_SELECTOR_THRESHOLDS;
