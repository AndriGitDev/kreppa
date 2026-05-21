import { SourceTable } from "../../components/SourceTable";
import { allIndicators, readData, type Latest } from "../../lib/data";

type Sources = {
  sources: Array<{ id: string; attribution: string; page_url: string; api_url: string; license: string; frequency: string }>;
  pending_sources: Array<{ id: string; status: string; reason: string; page_url: string }>;
};

export default function DataPage() {
  const latest = readData<Latest>("latest.json");
  const sources = readData<Sources>("sources.json");
  return (
    <main className="shell">
      <section className="section">
        <h1>Gögn</h1>
        <p className="subtitle">Allt sem mælirinn notar á að vera rekjanlegt. Engin leynileg Excel-skammarkrókagögn.</p>
        <p>
          <a href="/api/latest">/api/latest</a> | <a href="/api/history">/api/history</a> | <a href="/api/sources">/api/sources</a> |{" "}
          <a href="/api/methodology">/api/methodology</a>
        </p>
      </section>
      <section className="section">
        <h2>Núverandi athuganir</h2>
        <SourceTable indicators={allIndicators(latest)} />
      </section>
      <section className="section">
        <h2>Heimildir</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Heimild</th>
                <th>Tidni</th>
                <th>Leyfi</th>
                <th>API</th>
              </tr>
            </thead>
            <tbody>
              {sources.sources.map((source) => (
                <tr key={source.id}>
                  <td>{source.id}</td>
                  <td><a href={source.page_url}>{source.attribution}</a></td>
                  <td>{source.frequency}</td>
                  <td>{source.license}</td>
                  <td><a href={source.api_url}>PX-Web</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="section">
        <h2>Biðan</h2>
        {sources.pending_sources.map((source) => (
          <p key={source.id}>
            <strong>{source.id}:</strong> {source.reason} <a href={source.page_url}>source page</a>
          </p>
        ))}
      </section>
    </main>
  );
}
