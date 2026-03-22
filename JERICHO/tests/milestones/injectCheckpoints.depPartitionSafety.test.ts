import { describe, expect, it } from 'vitest';
import { injectCheckpoints } from '../../src/planner/milestones/injectCheckpoints.ts';

function checkpointIndex(id: string) {
  const match = id.match(/::S(\d+)$/);
  return match ? Number(match[1]) : null;
}

describe('injectCheckpoints dependency partition safety', () => {
  it('maintains monotonic checkpoint chain dependencies', () => {
    const out = injectCheckpoints({
      actions: [
        { id: 'A0001', estimateMin: 60, category: 'FOCUS', dependencies: [] },
        { id: 'A0002', estimateMin: 60, category: 'FOCUS', dependencies: ['A0001'] },
        { id: 'A0003', estimateMin: 60, category: 'FOCUS', dependencies: ['A0002'] },
        { id: 'A0004', estimateMin: 60, category: 'FOCUS', dependencies: ['A0003'] },
      ],
      milestones: [
        {
          milestoneId: 'M01',
          windowStartDayKey: '2026-01-01',
          windowEndDayKey: '2026-06-30',
          actionIds: ['A0001', 'A0002', 'A0003', 'A0004'],
        },
      ],
      constraints: { maxScheduledMinutesPerDay: 240 },
      horizons: { startDayKey: '2026-01-01', endDayKey: '2026-12-31' },
      policy: { cadenceMode: 'adaptive' },
    });

    const checkpoints = out.actionsWithCheckpoints
      .filter((a) => a.isCheckpoint)
      .sort((a, b) => a.id.localeCompare(b.id));

    checkpoints.forEach((cp) => {
      const idx = checkpointIndex(cp.id);
      if (!idx || idx <= 1) return;
      const prev = `CHECKPOINT::M01::S${String(idx - 1).padStart(2, '0')}`;
      expect((cp.dependencies || []).includes(prev)).toBe(true);
    });
  });
});
