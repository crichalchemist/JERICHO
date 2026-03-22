import { describe, expect, it } from 'vitest';
import { computePolicySelection } from '../../src/planner/scoring/policySelector.ts';

const base = {
  horizonDays: 90,
  executionHorizonDays: 30,
  hasMilestones: false,
  milestoneCount: 0,
  unplacedEstimateMinTotal: 0,
  outsideExecutionHorizonEstimateMinTotal: 0,
  scheduleCoverageRatio: 1,
  scheduleTruthRatio: 1,
  capacityPressureRatio: 0.5,
  deadlineRisk: 10,
  milestoneRisk: 10,
  dependencyRisk: 10,
  contextSwitching: 70,
  loadSmoothness: 40,
  deferralPenalty: 10,
  milestoneAtRiskCount: 0,
  depTightCount: 0,
  contextSwitchCount: 12,
  dailyLoadStdDev: 10,
};

describe('policy selector hysteresis', () => {
  it('blocks switch under min hold', () => {
    const out = computePolicySelection(base, {
      priorPolicyId: 'BALANCED',
      priorPolicyAgeDays: 2,
      minPolicyHoldDays: 7,
    });
    expect(out.selectedPolicyId).toBe('BALANCED');
    expect(out.hysteresis.blockedBy).toBe('HYSTERESIS_MIN_DURATION');
  });

  it('allows switch when hold satisfied', () => {
    const out = computePolicySelection(base, {
      priorPolicyId: 'BALANCED',
      priorPolicyAgeDays: 9,
      minPolicyHoldDays: 7,
    });
    expect(out.selectedPolicyId).toBe('DEEP_WORK');
  });
});
