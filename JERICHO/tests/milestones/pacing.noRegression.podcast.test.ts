import { describe, expect, it } from 'vitest';
import { buildPolicyAndQualityDiagnostics } from '../../src/state/draftSchedule.js';

const suggestedBlocks = Array.from({ length: 10 }, (_, i) => ({
  id: `sg-${i + 1}`,
  goalId: 'podcast',
  startISO: `2026-01-${String(3 + i).padStart(2, '0')}T09:00:00.000Z`,
  durationMinutes: 45,
  domain: i % 2 === 0 ? 'FOCUS' : 'CREATION',
  status: 'suggested',
}));

const contract = {
  startDayKey: '2026-01-02',
  endDayKey: '2026-02-28',
  horizonDays: 60,
};

describe('pacing no regression on non-milestone scenario', () => {
  it('does not change score or assignments when no milestones are present', () => {
    const baseline = buildPolicyAndQualityDiagnostics({
      suggestedBlocks,
      planDraft: {
        qualityPolicyId: 'BALANCED',
        autoPolicySelection: false,
        enableQualityOptimizer: false,
        enableMilestonePacing: false,
        executionHorizonDays: 60,
      },
      contract,
      timeZone: 'UTC',
      policyState: null,
    });

    const pacing = buildPolicyAndQualityDiagnostics({
      suggestedBlocks,
      planDraft: {
        qualityPolicyId: 'BALANCED',
        autoPolicySelection: false,
        enableQualityOptimizer: false,
        enableMilestonePacing: true,
        pacingCadenceMode: 'adaptive',
        executionHorizonDays: 60,
      },
      contract,
      timeZone: 'UTC',
      policyState: null,
    });

    expect(pacing.assignments).toEqual(baseline.assignments);
    expect(pacing.qualityScoreBaseline).toBe(baseline.qualityScoreBaseline);
    expect(pacing.pacingInjectedCheckpointCount).toBe(0);
  });
});
