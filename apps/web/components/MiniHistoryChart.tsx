export function MiniHistoryChart({ history }: { history: Array<{ date: string; score: number }> }) {
  if (history.length < 2) {
    return <p className="muted">Saga byrjar þegar cron byrjar að mala. Mjög dramatísk lína kemur seinna.</p>;
  }
  const points = history
    .map((item, index) => {
      const x = (index / Math.max(1, history.length - 1)) * 100;
      const y = 100 - item.score;
      return `${x},${y}`;
    })
    .join(" ");
  return (
    <svg className="history" viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Kreppumælir history">
      <polyline points={points} fill="none" stroke="#d94f2b" strokeWidth="3" />
    </svg>
  );
}
