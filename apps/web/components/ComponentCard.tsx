import type { Component } from "../lib/data";

export function ComponentCard({ component }: { component: Component }) {
  const score = component.score ?? 0;
  const pending = component.score === null;
  return (
    <article className="card">
      <div className="card-header">
        <div>
          <h3>{component.label_is}</h3>
          <p className="muted">{component.label_en}</p>
        </div>
        <span className={pending ? "component-pending" : "component-score"}>
          {pending ? "Bíður" : Math.round(score)}
        </span>
      </div>
      <div className="bar" aria-label={`Score ${score}`}>
        <span style={{ width: `${score}%` }} />
      </div>
      <p className="muted">Vigt: {Math.round(component.weight * 100)}% | Traust: {Math.round(component.confidence * 100)}%</p>
      {pending ? (
        <p className="pending-note">Ekki reiknað enn. Opinber vélræn heimild þarf að vera staðfest áður en þessi hluti fær að stressa mælinn.</p>
      ) : null}
    </article>
  );
}
