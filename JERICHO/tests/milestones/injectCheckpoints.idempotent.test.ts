import { describe, expect, it } from 'vitest';
import { injectCheckpoints } from '../../src/planner/milestones/injectCheckpoints.ts';

const base = {
  actions: [
    { id: 'A0001', estimateMin: 60, category: 'FOCUS', dependencies: [] },
    { id: 'A0002', estimateMin: 45, category: 'FOCUS', dependencies: ['A0001'] },
  ],
  milestones: [
    {
      milestoneId: 'M01',
      windowStartDayKey: '2026-01-01',
      windowEndDayKey: '2026-02-28',
      actionIds: ['A0001', 'A0002'],
    },
  ],
  constraints: { maxScheduledMinutesPerDay: 240 },
  horizons: { startDayKey: '2026-01-01', endDayKey: '2026-12-31' },
  policy: { cadenceMode: 'adaptive' as const },
};

describe('injectCheckpoints idempotent', () => {
  it('does not duplicate checkpoints on second run', () => {
    const first = injectCheckpoints(base);
    const second = injectCheckpoints({ ...base, actions: first.actionsWithCheckpoints });
    expect(second.injected.checkpointCount).toBe(first.injected.checkpointCount);
    expect(second.actionsWithCheckpoints.length).toBe(first.actionsWithCheckpoints.length);
  });
});
