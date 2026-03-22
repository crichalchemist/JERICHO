import { describe, expect, it } from 'vitest';
import { computePolicySelection } from '../../src/planner/scoring/policySelector.ts';

const signals = {
  horizonDays: 90,
  executionHorizonDays: 30,
  hasMilestones: true,
  milestoneCount: 1,
  unplacedEstimateMinTotal: 0,
  outsideExecutionHorizonEstimateMinTotal: 0,
  scheduleCoverageRatio: 1,
  scheduleTruthRatio: 1,
  capacityPressureRatio: 0.8,
  deadlineRisk: 40,
  milestoneRisk: 40,
  dependencyRisk: 20,
  contextSwitching: 50,
  loadSmoothness: 20,
  deferralPenalty: 10,
  milestoneAtRiskCount: 0,
  depTightCount: 0,
  contextSwitchCount: 8,
  dailyLoadStdDev: 15,
};

describe('policy selector determinism', () => {
  it('same signals + prior produce same decision', () => {
    const one = computePolicySelection(signals, { priorPolicyId: 'BALANCED', priorPolicyAgeDays: 10 });
    const two = computePolicySelection(signals, { priorPolicyId: 'BALANCED', priorPolicyAgeDays: 10 });
    expect(two).toEqual(one);
  });
});
