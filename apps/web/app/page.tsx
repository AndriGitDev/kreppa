import { ComponentCard } from "../components/ComponentCard";
import { DriverList } from "../components/DriverList";
import { Gauge } from "../components/Gauge";
import { MiniHistoryChart } from "../components/MiniHistoryChart";
import { SourceTable } from "../components/SourceTable";
import { copy } from "../lib/copy";
import { allIndicators, readData, type Latest } from "../lib/data";

export default function HomePage() {
  const latest = readData<Latest>("latest.json");
  const history = readData<{ history: Array<{ date: string; score: number }> }>("history.json");
  const indicators = allIndicators(latest);
  return (
    <main className="shell">
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow">Opið gagnamælaborð með kvíða</div>
          <h1>
            <span>Kreppu-</span>
            <span>mælirinn</span>
          </h1>
          <p className="subtitle">{copy.heroSubtitle}</p>
          <div className="status-line">
            <div className="score-callout">
              <span className="score-dot" aria-hidden="true" />
              <strong>{latest.overall.level.label_is}</strong>
            </div>
          </div>
          <div className="meta-row" aria-label="Staða gagna">
            <span className="pill">Síðast uppfært: {new Date(latest.generated_at).toISOString().slice(0, 10)}</span>
            <span className="pill">Gagnatraust: {latest.overall.confidence_label}</span>
          </div>
        </div>
        <Gauge score={latest.overall.score} />
      </section>

      <section className="section">
        <h2>Af hverju er mælirinn hér?</h2>
        <div className="drivers">
          <DriverList title="Það sem ýtir upp kvíðanum" drivers={latest.drivers.up} />
          <DriverList title="Það sem heldur aftur af kreppunni" drivers={latest.drivers.down} />
        </div>
      </section>

      <section className="section">
        <h2>Hlutar mælisins</h2>
        <div className="grid">
          {latest.components.map((component) => (
            <ComponentCard key={component.id} component={component} />
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Lítil sögulína</h2>
        <MiniHistoryChart history={history.history} />
      </section>

      <section className="section">
        <h2>Gögnin á bakvið mælinn</h2>
        <SourceTable indicators={indicators} />
      </section>

      <section className="section">
        <div className="disclaimer">
          <h2>Ekki fjármálaráðgjöf</h2>
          <p>{copy.notAdviceIs}</p>
          <p className="muted">{copy.notAdviceEn}</p>
        </div>
        {latest.warnings.length ? (
          <div style={{ marginTop: 18 }}>
            <h2>Viðvaranir</h2>
            {latest.warnings.map((warning) => (
              <p key={warning} className="muted">{warning}</p>
            ))}
          </div>
        ) : null}
        <p>
          <a href="/methodology">Skoða aðferðafræði</a>
        </p>
      </section>
    </main>
  );
}
