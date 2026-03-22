export function nowMs(): number {
  if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
    return performance.now();
  }
  return Date.now();
}

export function measure<T>(label: string, fn: () => T): { value: T; ms: number } {
  const _label = label;
  void _label;
  const start = nowMs();
  const value = fn();
  const end = nowMs();
  return { value, ms: Math.max(0, end - start) };
}

export function getHeapUsedBytes(): number | null {
  try {
    if (typeof process === 'undefined' || typeof process.memoryUsage !== 'function') return null;
    const heap = process.memoryUsage().heapUsed;
    return Number.isFinite(heap) ? heap : null;
  } catch {
    return null;
  }
}

export function measureWithMemory<T>(label: string, fn: () => T): { value: T; ms: number; heapDeltaBytes?: number } {
  const before = getHeapUsedBytes();
  const measured = measure(label, fn);
  const after = getHeapUsedBytes();
  if (before == null || after == null) return measured;
  return {
    ...measured,
    heapDeltaBytes: after - before,
  };
}
