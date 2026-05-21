import { readData } from "../../lib/data";

type Methodology = {
  score_version: string;
  components: Record<string, { label_is: string; label_en: string; weight: number }>;
  indicators: Array<{ id: string; label_is: string; label_en: string; source_id: string; direction: string; transform: string; threshold?: { good: number; bad: number } }>;
  normalization: Record<string, string>;
  missing_data: string;
  disclaimer: string;
};

export default function MethodologyPage() {
  const methodology = readData<Methodology>("methodology.json");
  return (
    <main className="shell">
      <section className="section">
        <h1>Aðferðafræði</h1>
        <p className="subtitle">Útgáfa {methodology.score_version}. Kreppumælirinn er streituvísir úr opinberum gögnum, ekki kristalskúla.</p>
      </section>

      <section className="section">
        <h2>Vigtir</h2>
        <div className="grid">
          {Object.entries(methodology.components).map(([id, component]) => (
            <article className="card" key={id}>
              <h3>{component.label_is}</h3>
              <p className="muted">{component.label_en}</p>
              <strong>{Math.round(component.weight * 100)}%</strong>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Visar</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Heiti</th>
                <th>Umbreyting</th>
                <th>Átt</th>
                <th>Þröskuldar</th>
              </tr>
            </thead>
            <tbody>
              {methodology.indicators.map((indicator) => (
                <tr key={indicator.id}>
                  <td>{indicator.id}</td>
                  <td>{indicator.label_is}</td>
                  <td>{indicator.transform}</td>
                  <td>{indicator.direction}</td>
                  <td>{indicator.threshold ? `${indicator.threshold.good} / ${indicator.threshold.bad}` : "Percentile only"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="section">
        <h2>Normalisering</h2>
        {Object.entries(methodology.normalization).map(([key, value]) => (
          <p key={key}>
            <strong>{key}:</strong> {value}
          </p>
        ))}
        <p>{methodology.missing_data}</p>
        <div className="disclaimer">{methodology.disclaimer}</div>
      </section>
    </main>
  );
}
