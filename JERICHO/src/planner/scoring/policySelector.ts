import { POLICY_SELECTOR_THRESHOLDS, type PolicySelectorThresholds } from './policySelectorThresholds.ts';
import type { QualityPolicyId } from './policy.ts';

export type PolicySelectionSignals = {
  horizonDays: number;
  executionHorizonDays: number;
  hasMilestones: boolean;
  milestoneCount: number;
  unplacedEstimateMinTotal: number;
  outsideExecutionHorizonEstimateMinTotal: number;
  scheduleCoverageRatio: number;
  scheduleTruthRatio: number;
  capacityPressureRatio?: number;
  deadlineRisk: number;
  milestoneRisk: number;
  dependencyRisk: number;
  contextSwitching: number;
  loadSmoothness: number;
  deferralPenalty: number;
  milestoneAtRiskCount: number;
  depTightCount: number;
  contextSwitchCount: number;
  dailyLoadStdDev: number;
};

export type PolicySelectionDecision = {
  selectedPolicyId: QualityPolicyId;
  reasonCodes: string[];
  signals: PolicySelectionSignals;
  hysteresis: {
    priorPolicyId?: string;
    stickyPolicyId?: string;
    changed: boolean;
    blockedBy?: string;
  };
};

type PolicySelectorOpts = {
  priorPolicyId?: string;
  priorPolicyAgeDays?: number;
  minPolicyHoldDays?: number;
  switchThresholds?: Partial<PolicySelectorThresholds>;
  priorSignalsSnapshot?: Partial<PolicySelectionSignals>;
};

function mergeThresholds(overrides?: Partial<PolicySelectorThresholds>): PolicySelectorThresholds {
  return {
    ...POLICY_SELECTOR_THRESHOLDS,
    ...(overrides || {})
  };
}

function chooseByRules(signals: PolicySelectionSignals, t: PolicySelectorThresholds): { policy: QualityPolicyId; reason: string } {
  if (signals.hasMilestones && (signals.milestoneAtRiskCount > 0 || signals.milestoneRisk >= t.milestoneRiskHigh)) {
    return { policy: 'DEADLINE_FIRST', reason: 'MILESTONE_AT_RISK' };
  }
  if (signals.deadlineRisk >= t.deadlineRiskHigh) {
    return { policy: 'DEADLINE_FIRST', reason: 'DEADLINE_RISK_HIGH' };
  }
  if (signals.depTightCount >= t.depTightCountHigh || signals.dependencyRisk >= t.dependencyRiskHigh) {
    return { policy: 'DEPENDENCY_SAFETY', reason: 'DEPENDENCY_TIGHT' };
  }
  if (
    signals.contextSwitchCount >= t.contextSwitchCountHigh &&
    signals.deadlineRisk <= t.deadlineRiskLow &&
    signals.milestoneRisk <= t.milestoneRiskLow
  ) {
    return { policy: 'DEEP_WORK', reason: 'CONTEXT_SWITCHING_HIGH' };
  }
  if (
    (signals.outsideExecutionHorizonEstimateMinTotal >= t.outsideHorizonMinHigh || signals.deferralPenalty >= t.deferralPenaltyHigh) &&
    signals.deadlineRisk <= t.deadlineRiskMid &&
    signals.milestoneRisk <= t.milestoneRiskMid
  ) {
    return { policy: 'THROUGHPUT', reason: 'DEFERRAL_HIGH' };
  }
  return { policy: 'BALANCED', reason: 'DEFAULT_BALANCED' };
}

function deltaSatisfied(
  current: PolicySelectionSignals,
  prior: Partial<PolicySelectionSignals> | undefined,
  t: PolicySelectorThresholds
): boolean {
  if (!prior) return true;
  const dDeadline = Math.abs(current.deadlineRisk - Number(prior.deadlineRisk || 0));
  const dMilestone = Math.abs(current.milestoneRisk - Number(prior.milestoneRisk || 0));
  const dDependency = Math.abs(current.dependencyRisk - Number(prior.dependencyRisk || 0));
  const dContext = Math.abs(current.contextSwitchCount - Number(prior.contextSwitchCount || 0));
  return (
    dDeadline >= t.switchDeltaDeadlineRisk ||
    dMilestone >= t.switchDeltaMilestoneRisk ||
    dDependency >= t.switchDeltaDependencyRisk ||
    dContext >= t.switchDeltaContext
  );
}

export function computePolicySelection(signals: PolicySelectionSignals, opts: PolicySelectorOpts = {}): PolicySelectionDecision {
  const thresholds = mergeThresholds(opts.switchThresholds);
  const minPolicyHoldDays = Number.isFinite(opts.minPolicyHoldDays) ? Number(opts.minPolicyHoldDays) : 7;
  const priorPolicyId = opts.priorPolicyId;
  const priorPolicyAgeDays = Number.isFinite(opts.priorPolicyAgeDays) ? Number(opts.priorPolicyAgeDays) : minPolicyHoldDays;

  const rulePick = chooseByRules(signals, thresholds);
  const reasonCodes = [rulePick.reason];
  let finalPolicy: QualityPolicyId = rulePick.policy;
  let blockedBy: string | undefined;

  if (priorPolicyId) {
    if (priorPolicyId === rulePick.policy) {
      finalPolicy = priorPolicyId as QualityPolicyId;
    } else if (priorPolicyAgeDays < minPolicyHoldDays) {
      finalPolicy = priorPolicyId as QualityPolicyId;
      blockedBy = 'HYSTERESIS_MIN_DURATION';
      reasonCodes.push(blockedBy);
    } else if (!deltaSatisfied(signals, opts.priorSignalsSnapshot, thresholds)) {
      finalPolicy = priorPolicyId as QualityPolicyId;
      blockedBy = 'HYSTERESIS_DELTA_TOO_SMALL';
      reasonCodes.push(blockedBy);
    }
  }

  return {
    selectedPolicyId: finalPolicy,
    reasonCodes,
    signals: { ...signals },
    hysteresis: {
      priorPolicyId,
      stickyPolicyId: finalPolicy,
      changed: Boolean(priorPolicyId && priorPolicyId !== finalPolicy),
      blockedBy
    }
  };
}
