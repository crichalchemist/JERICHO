import { dayKeyFromISO } from './time/time.ts';
import { getContractStartDayKey, filterSuggestionsByStartDayKey, normalizeSuggestionDayKey } from './suggestionFilters.js';
import { scoreSchedule } from '../planner/scoring/scoreSchedule.ts';
import { optimizeSchedule } from '../planner/optimize/optimizeSchedule.ts';
import { computePolicySelection } from '../planner/scoring/policySelector.ts';

const ensureISO = (dayKey, time = '09:00') => {
  if (!dayKey) return null;
  return `${dayKey}T${time}:00.000Z`;
};

const sortDraftItems = (items = []) =>
  [...items].sort((a, b) => {
    if (a.dayKey !== b.dayKey) return a.dayKey.localeCompare(b.dayKey);
    if (a.startISO !== b.startISO) return (a.startISO || '').localeCompare(b.startISO || '');
    return (a.title || '').localeCompare(b.title || '');
  });

const sortAssignments = (assignments = []) =>
  [...assignments].sort((a, b) => {
    if (a.dayKey !== b.dayKey) return a.dayKey.localeCompare(b.dayKey);
    if (a.startMin !== b.startMin) return a.startMin - b.startMin;
    if (a.actionId !== b.actionId) return a.actionId.localeCompare(b.actionId);
    return (a.chunkIndex || 0) - (b.chunkIndex || 0);
  });

function minutesFromISO(iso) {
  if (!iso) return 0;
  const parsed = new Date(iso);
  if (!Number.isFinite(parsed.getTime())) return 0;
  return parsed.getUTCHours() * 60 + parsed.getUTCMinutes();
}

function toAssignments(suggestedBlocks = [], timeZone = 'UTC') {
  return sortAssignments(
    (suggestedBlocks || [])
      .filter((s) => s && s.status === 'suggested')
      .map((s, idx) => ({
        actionId: `${s.goalId || 'goal'}:${s.id || idx}`,
        chunkIndex: 0,
        chunkCount: 1,
        dayKey: normalizeSuggestionDayKey(s, timeZone) || dayKeyFromISO(s.startISO, timeZone) || '',
        startMin: minutesFromISO(s.startISO),
        durationMin: Number(s.durationMinutes) || 30,
        category: s.domain || 'FOCUS',
      }))
      .filter((a) => a.dayKey)
  );
}

export function buildPolicyAndQualityDiagnostics({
  suggestedBlocks = [],
  planDraft = null,
  contract = null,
  timeZone = 'UTC',
  policyState = null,
}) {
  const assignments = toAssignments(suggestedBlocks, timeZone);
  const qualityPolicyIdRequested = planDraft?.qualityPolicyId || 'BALANCED';
  const minPolicyHoldDays = Number.isFinite(planDraft?.minPolicyHoldDays) ? planDraft.minPolicyHoldDays : 7;

  const unplacedEstimateMinTotal = 0;
  const outsideExecutionHorizonEstimateMinTotal = 0;
  const totalEstimate = assignments.reduce((sum, a) => sum + (a.durationMin || 0), 0);
  const scoreBaselineRequested = scoreSchedule({
    assignments,
    constraints: { executionHorizonDays: contract?.horizonDays || planDraft?.horizonDays || 30 },
    horizons: {
      executionWindowStartDayKey: contract?.startDayKey || '',
      executionWindowEndDayKey: contract?.endDayKey || '',
      feasibilityWindowEndDayKey: contract?.endDayKey || '',
    },
    metricsContext: {
      unplacedMinutes: unplacedEstimateMinTotal,
      outsideExecutionHorizonMinutes: outsideExecutionHorizonEstimateMinTotal,
      goalDeadlineDayKey: contract?.endDayKey || '',
    },
    policyId: qualityPolicyIdRequested,
  });

  const selectionSignals = {
    horizonDays: contract?.horizonDays || planDraft?.horizonDays || 30,
    executionHorizonDays: contract?.horizonDays || planDraft?.horizonDays || 30,
    hasMilestones: false,
    milestoneCount: 0,
    unplacedEstimateMinTotal,
    outsideExecutionHorizonEstimateMinTotal,
    scheduleCoverageRatio: totalEstimate > 0 ? 1 : 0,
    scheduleTruthRatio: totalEstimate > 0 ? 1 : 0,
    capacityPressureRatio: undefined,
    deadlineRisk: scoreBaselineRequested.components.deadlineRisk,
    milestoneRisk: scoreBaselineRequested.components.milestoneRisk,
    dependencyRisk: scoreBaselineRequested.components.dependencyRisk,
    contextSwitching: scoreBaselineRequested.components.contextSwitching,
    loadSmoothness: scoreBaselineRequested.components.loadSmoothness,
    deferralPenalty: scoreBaselineRequested.components.deferralPenalty,
    milestoneAtRiskCount: scoreBaselineRequested.evidence.milestoneAtRiskCount || 0,
    depTightCount: scoreBaselineRequested.evidence.depTightCount || 0,
    contextSwitchCount: scoreBaselineRequested.evidence.contextSwitchCount || 0,
    dailyLoadStdDev: scoreBaselineRequested.evidence.dailyLoadStdDev || 0,
  };

  const policySelectionDecision =
    planDraft?.autoPolicySelection === true
      ? computePolicySelection(selectionSignals, {
          priorPolicyId: policyState?.currentPolicyId,
          priorPolicyAgeDays: policyState?.policyAgeDays,
          minPolicyHoldDays,
          priorSignalsSnapshot: policyState?.priorSignalsSnapshot,
        })
      : {
          selectedPolicyId: qualityPolicyIdRequested,
          reasonCodes: ['AUTO_SELECTION_DISABLED'],
          signals: selectionSignals,
          hysteresis: {
            priorPolicyId: policyState?.currentPolicyId,
            stickyPolicyId: qualityPolicyIdRequested,
            changed: false,
          },
        };

  const qualityPolicyIdUsed = policySelectionDecision.hysteresis?.stickyPolicyId || policySelectionDecision.selectedPolicyId;

  const scoreBaseline = scoreSchedule({
    assignments,
    constraints: { executionHorizonDays: contract?.horizonDays || planDraft?.horizonDays || 30 },
    horizons: {
      executionWindowStartDayKey: contract?.startDayKey || '',
      executionWindowEndDayKey: contract?.endDayKey || '',
      feasibilityWindowEndDayKey: contract?.endDayKey || '',
    },
    metricsContext: {
      unplacedMinutes: unplacedEstimateMinTotal,
      outsideExecutionHorizonMinutes: outsideExecutionHorizonEstimateMinTotal,
      goalDeadlineDayKey: contract?.endDayKey || '',
    },
    policyId: qualityPolicyIdUsed,
  });

  const optimizationEnabled = planDraft?.enableQualityOptimizer === true;
  const optimizationResult = optimizationEnabled
    ? optimizeSchedule({
        baselineAssignments: assignments,
        policyId: qualityPolicyIdUsed,
        constraints: { executionHorizonDays: contract?.horizonDays || planDraft?.horizonDays || 30 },
        horizons: {
          executionWindowStartDayKey: contract?.startDayKey || '',
          executionWindowEndDayKey: contract?.endDayKey || '',
          feasibilityWindowEndDayKey: contract?.endDayKey || '',
        },
        metricsContext: {
          unplacedMinutes: unplacedEstimateMinTotal,
          outsideExecutionHorizonMinutes: outsideExecutionHorizonEstimateMinTotal,
          goalDeadlineDayKey: contract?.endDayKey || '',
        },
        maxIterations: planDraft?.optimizerMaxIterations || 2,
        maxCandidatesPerIter: planDraft?.optimizerMaxCandidates || 30,
      })
    : null;

  const scoreOptimized = optimizationResult?.bestScore || scoreBaseline;

  return {
    assignments,
    qualityPolicyIdRequested,
    qualityPolicyIdUsed,
    policySelectionDecision,
    policySelectionReasonCodes: [...(policySelectionDecision.reasonCodes || [])],
    policySelectionSignalsSnapshot: selectionSignals,
    qualityScoreBaseline: scoreBaseline.total,
    qualityScoreBaselineByComponent: { ...scoreBaseline.components },
    qualityScoreOptimized: scoreOptimized.total,
    qualityScoreOptimizedByComponent: { ...scoreOptimized.components },
    qualityImprovementDelta: optimizationResult ? optimizationResult.improvement.deltaTotal : 0,
    optimizerRejectedCandidatesSummary: optimizationResult
      ? optimizationResult.rejectedCandidatesSummary
      : {
          DEADLINE_GUARDRAIL: 0,
          MILESTONE_GUARDRAIL: 0,
          DEFERRAL_GUARDRAIL: 0,
          DEPENDENCY_GUARDRAIL: 0,
          NO_IMPROVEMENT: 0,
        },
  };
}

export function buildDraftScheduleItems({
  suggestedBlocks = [],
  routeSuggestions = [],
  contract = null,
  timeZone = 'UTC',
  defaults = {},
  contractStartDayKey: contractStartDayKeyOverride = null
} = {}) {
  const startDayKey = contractStartDayKeyOverride || getContractStartDayKey(contract, timeZone);
  const normalizedSuggested = filterSuggestionsByStartDayKey(suggestedBlocks, startDayKey, timeZone);
  const items = [];

  normalizedSuggested.forEach((suggestion) => {
    const dayKey = normalizeSuggestionDayKey(suggestion, timeZone) || defaults.todayKey || '';
    const startISO =
      suggestion.startISO ||
      suggestion.start ||
      ensureISO(dayKey, '09:00') ||
      `${dayKey}T09:00:00.000Z`;
    const minutes = Number(suggestion.durationMinutes) || Number(suggestion.minutes) || 30;
    const title = suggestion.title || suggestion.label || 'Suggested block';
    items.push({
      id: `suggested:${suggestion.id || `${dayKey}-${title}`}`,
      source: 'suggestedPath',
      dayKey,
      startISO,
      minutes,
      domainKey: suggestion.domain || 'FOCUS',
      title,
      detail: suggestion.detail || suggestion.description || '',
      reason: 'Suggested path',
      payload: suggestion
    });
  });

  const route = routeSuggestions.map((entry) => {
    const dayKey = entry?.dayKey || defaults.todayKey || '';
    const total = Number(entry?.totalBlocks) || 0;
    return {
      id: `route:${dayKey}`,
      source: 'coldPlan',
      dayKey,
      startISO: ensureISO(dayKey, '09:00'),
      minutes: defaults.routeMinutes || 30,
      domainKey: defaults.primaryDomain || 'FOCUS',
      title: `${total} forecast block${total !== 1 ? 's' : ''}`,
      detail: entry?.summary || '',
      reason: 'Cold plan',
      payload: entry
    };
  });

  const merged = sortDraftItems([...items, ...route]);
  if (!startDayKey && !contract?.deadline?.dayKey) return merged;
  return merged.filter((item) => {
    if (!item.dayKey) return false;
    if (startDayKey && item.dayKey < startDayKey) return false;
    if (contract?.deadline?.dayKey && contract.deadline.dayKey && item.dayKey > contract.deadline.dayKey) return false;
    return true;
  });
}

export function filterDraftItemsByDay(items = [], dayKey) {
  if (!dayKey) return [];
  return (items || []).filter((item) => item.dayKey === dayKey);
}
