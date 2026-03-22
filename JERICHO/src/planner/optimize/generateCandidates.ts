import type { ScheduleAssignment } from '../scoring/scoreSchedule.ts';

type CandidateInput = {
  baselineAssignments: ScheduleAssignment[];
  frozenReservations?: Array<{ actionId: string; chunkIndex: number }>;
  maxPerDay?: number;
  slotStepMin?: number;
};

function keyOf(assignment: ScheduleAssignment) {
  return `${assignment.actionId}#${assignment.chunkIndex}`;
}

function sortAssignments(assignments: ScheduleAssignment[]) {
  return [...assignments].sort((a, b) => {
    if (a.dayKey !== b.dayKey) return a.dayKey.localeCompare(b.dayKey);
    if (a.startMin !== b.startMin) return a.startMin - b.startMin;
    if (a.actionId !== b.actionId) return a.actionId.localeCompare(b.actionId);
    return a.chunkIndex - b.chunkIndex;
  });
}

function stableHash(assignments: ScheduleAssignment[]) {
  return sortAssignments(assignments)
    .map((a) => `${a.actionId}:${a.chunkIndex}:${a.dayKey}:${a.startMin}`)
    .join('|');
}

export function generateCandidates({
  baselineAssignments,
  frozenReservations = [],
  maxPerDay = 5,
  slotStepMin = 30
}: CandidateInput): ScheduleAssignment[][] {
  const baseline = sortAssignments(baselineAssignments || []);
  const frozen = new Set(frozenReservations.map((r) => `${r.actionId}#${r.chunkIndex}`));
  const emitted = new Set<string>();
  const candidates: ScheduleAssignment[][] = [];

  const byDay = new Map<string, ScheduleAssignment[]>();
  baseline.forEach((a) => {
    const row = byDay.get(a.dayKey) || [];
    row.push(a);
    byDay.set(a.dayKey, row);
  });

  [...byDay.keys()].sort().forEach((dayKey) => {
    const dayItems = sortAssignments(byDay.get(dayKey) || []);

    // Adjacent swap
    for (let i = 0; i < dayItems.length - 1 && i < maxPerDay; i += 1) {
      const left = dayItems[i];
      const right = dayItems[i + 1];
      if (left.durationMin !== right.durationMin) continue;
      if (frozen.has(keyOf(left)) || frozen.has(keyOf(right))) continue;
      const next = baseline.map((a) => {
        if (a.actionId === left.actionId && a.chunkIndex === left.chunkIndex) {
          return { ...a, startMin: right.startMin };
        }
        if (a.actionId === right.actionId && a.chunkIndex === right.chunkIndex) {
          return { ...a, startMin: left.startMin };
        }
        return { ...a };
      });
      const hash = stableHash(next);
      if (!emitted.has(hash)) {
        emitted.add(hash);
        candidates.push(sortAssignments(next));
      }
    }

    // Local +/- shift
    dayItems.forEach((item) => {
      if (frozen.has(keyOf(item))) return;
      [-slotStepMin, slotStepMin].forEach((delta) => {
        const startMin = item.startMin + delta;
        if (startMin < 0) return;
        const endMin = startMin + item.durationMin;
        if (endMin > 24 * 60) return;
        const conflict = dayItems.some((other) => {
          if (other.actionId === item.actionId && other.chunkIndex === item.chunkIndex) return false;
          const otherStart = other.startMin;
          const otherEnd = other.startMin + other.durationMin;
          return !(endMin <= otherStart || startMin >= otherEnd);
        });
        if (conflict) return;
        const next = baseline.map((a) =>
          a.actionId === item.actionId && a.chunkIndex === item.chunkIndex ? { ...a, startMin } : { ...a }
        );
        const hash = stableHash(next);
        if (!emitted.has(hash)) {
          emitted.add(hash);
          candidates.push(sortAssignments(next));
        }
      });
    });
  });

  return candidates;
}
