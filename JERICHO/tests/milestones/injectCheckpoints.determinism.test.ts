import { describe, expect, it } from 'vitest';
import { injectCheckpoints } from '../../src/planner/milestones/injectCheckpoints.ts';

const input = {
  actions: [
    { id: 'A0001', estimateMin: 60, category: 'FOCUS', dependencies: [] },
    { id: 'A0002', estimateMin: 45, category: 'FOCUS', dependencies: ['A0001'] },
    { id: 'A0003', estimateMin: 30, category: 'CREATION', dependencies: ['A0002'] },
  ],
  milestones: [
    {
      milestoneId: 'M01',
      windowStartDayKey: '2026-01-01',
      windowEndDayKey: '2026-03-31',
      actionIds: ['A0001', 'A0002', 'A0003'],
    },
  ],
  constraints: { maxScheduledMinutesPerDay: 240 },
  horizons: { startDayKey: '2026-01-01', endDayKey: '2026-12-31' },
  policy: { cadenceMode: 'adaptive' as const },
};

describe('injectCheckpoints determinism', () => {
  it('returns identical checkpoints for same input', () => {
    const one = injectCheckpoints(input);
    const two = injectCheckpoints(input);
    expect(two).toEqual(one);
  });
});
