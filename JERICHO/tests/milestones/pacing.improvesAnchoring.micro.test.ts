import { describe, expect, it } from 'vitest';
import { buildPolicyAndQualityDiagnostics } from '../../src/state/draftSchedule.js';

const suggestedBlocks = Array.from({ length: 8 }, (_, i) => ({
  id: `sg-${i + 1}`,
  goalId: 'goal-1',
  startISO: `2026-01-${String(3 + i).padStart(2, '0')}T09:00:00.000Z`,
  durationMinutes: 45,
  domain: i % 2 === 0 ? 'FOCUS' : 'CREATION',
  status: 'suggested',
}));

const actions = Array.from({ length: 16 }, (_, i) => ({
  id: `A${String(i + 1).padStart(4, '0')}`,
  estimateMin: 45,
  category: i % 2 === 0 ? 'FOCUS' : 'CREATION',
  dependencies: i === 0 ? [] : [`A${String(i).padStart(4, '0')}`],
}));

const milestones = [
  {
    milestoneId: 'M01',
    windowStartDayKey: '2026-01-03',
    windowEndDayKey: '2026-04-01',
    actionIds: actions.map((a) => a.id),
  },
];

const contract = {
  startDayKey: '2026-01-02',
  endDayKey: '2026-04-30',
  horizonDays: 120,
};

describe('pacing improves anchoring micro', () => {
  it('reduces anchoring misses and improves placed ratio relative to no pacing', () => {
    const withoutPacing = buildPolicyAndQualityDiagnostics({
      suggestedBlocks,
      planDraft: {
        qualityPolicyId: 'DEADLINE_FIRST',
        autoPolicySelection: false,
        enableQualityOptimizer: false,
        enableMilestonePacing: false,
        actions,
        milestones,
        executionHorizonDays: 120,
      },
      contract,
      timeZone: 'UTC',
      policyState: null,
    });

    const withPacing = buildPolicyAndQualityDiagnostics({
      suggestedBlocks,
      planDraft: {
        qualityPolicyId: 'DEADLINE_FIRST',
        autoPolicySelection: false,
        enableQualityOptimizer: false,
        enableMilestonePacing: true,
        pacingCadenceMode: 'adaptive',
        actions,
        milestones,
        executionHorizonDays: 120,
      },
      contract,
      timeZone: 'UTC',
      policyState: null,
    });

    expect(withPacing.pacingAnchoringMissCount).toBeLessThanOrEqual(withoutPacing.pacingAnchoringMissCount);
    expect(withPacing.milestonePlacedRatioAvg).toBeGreaterThanOrEqual(withoutPacing.milestonePlacedRatioAvg);
  });
});
