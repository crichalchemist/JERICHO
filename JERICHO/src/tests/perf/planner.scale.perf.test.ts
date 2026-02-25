import { describe, expect, it } from 'vitest';
import { runPerfScenario } from './runPerfScenario.ts';
import type { ScaleScenarioConfig } from './scaleScenarioFactory.ts';

const S1: ScaleScenarioConfig = {
  scenarioId: 'scale_500_actions_180d',
  horizon: { startDayKey: '2026-01-01', endDayKey: '2026-06-29' },
  executionHorizonDays: 180,
  actions: {
    count: 500,
    estimatePatternMin: [30, 45, 60, 90],
    categoryPattern: ['FOCUS', 'CREATION', 'ADMIN'],
    deps: { mode: 'layered', depth: 10, fan: 3 },
  },
  optimizerMode: 'off',
};

const S2: ScaleScenarioConfig = {
  scenarioId: 'scale_2000_actions_365d',
  horizon: { startDayKey: '2026-01-01', endDayKey: '2026-12-31' },
  executionHorizonDays: 365,
  actions: {
    count: 2000,
    estimatePatternMin: [30, 45, 60, 90],
    categoryPattern: ['FOCUS', 'CREATION', 'ADMIN'],
    deps: { mode: 'layered', depth: 20, fan: 4 },
  },
  optimizerMode: 'off',
};

const S3: ScaleScenarioConfig = {
  scenarioId: 'scale_5000_actions_3y_milestones',
  horizon: { startDayKey: '2026-01-01', endDayKey: '2028-12-31' },
  executionHorizonDays: 365,
  actions: {
    count: 5000,
    estimatePatternMin: [30, 45, 60, 90],
    categoryPattern: ['FOCUS', 'CREATION', 'ADMIN'],
    deps: { mode: 'chain', depth: 60, fan: 2 },
  },
  milestones: {
    count: 12,
    windowDays: 21,
    spacingDays: 84,
    attachEveryNActions: 120,
    checkpointActionIds: 'auto',
  },
  optimizerMode: 'off',
};

const S4: ScaleScenarioConfig = {
  scenarioId: 'scale_2000_dense_deps_1y_optimizer_on',
  horizon: { startDayKey: '2026-01-01', endDayKey: '2026-12-31' },
  executionHorizonDays: 365,
  actions: {
    count: 2000,
    estimatePatternMin: [30, 45, 60, 90],
    categoryPattern: ['FOCUS', 'CREATION', 'ADMIN'],
    deps: { mode: 'fan_in', depth: 30, fan: 8 },
  },
  optimizerMode: 'on',
  qualityPolicyId: 'DEEP_WORK',
  autoPolicySelection: false,
};

function assertMemory(value: unknown) {
  if (value == null) return;
  expect(Number.isFinite(Number(value))).toBe(true);
}

describe('planner scale perf', () => {
  it('runs deterministic scale scenarios with parity + perf gates', () => {
    const r1 = runPerfScenario(S1);
    const r2 = runPerfScenario(S2);
    const r3 = runPerfScenario(S3);
    const r4 = runPerfScenario(S4);

    [r1, r2, r3, r4].forEach((r) => {
      expect(r.parity.scheduleParity).toBe(true);
      expect(r.parity.scoreParity).toBe(true);
      expect(r.parity.policyParity).toBe(true);
      assertMemory(r.perf.heapDeltaBytesRebuild);
      assertMemory(r.perf.heapDeltaBytesApply);
    });

    expect(r1.perf.rebuildPreviewMs).toBeLessThan(750);
    expect(r1.perf.applyCommitMs).toBeLessThan(750);

    expect(r2.perf.rebuildPreviewMs).toBeLessThan(2500);
    expect(r2.perf.applyCommitMs).toBeLessThan(2500);

    expect(r3.perf.rebuildPreviewMs).toBeLessThan(8000);
    expect(r3.perf.applyCommitMs).toBeLessThan(8000);

    expect(Number(r4.perf.optimizeMs || 0)).toBeLessThan(2000);
    expect(r4.perf.rebuildPreviewMs).toBeLessThan(2500);
    expect(r4.perf.applyCommitMs).toBeLessThan(2500);

    const ratio21 = r2.perf.rebuildPreviewMs / Math.max(1, r1.perf.rebuildPreviewMs);
    const ratio32 = r3.perf.rebuildPreviewMs / Math.max(1, r2.perf.rebuildPreviewMs);
    expect(ratio21).toBeLessThan(8);
    expect(ratio32).toBeLessThan(5);
  });
});
