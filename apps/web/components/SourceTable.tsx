import type { Indicator } from "../lib/data";

export function SourceTable({ indicators }: { indicators: Indicator[] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Vísir</th>
            <th>Tímabil</th>
            <th>Gildi</th>
            <th>Eining</th>
            <th>Heimild</th>
            <th>Sótt</th>
          </tr>
        </thead>
        <tbody>
          {indicators.map((indicator) => (
            <tr key={indicator.id}>
              <td>{indicator.label_is}</td>
              <td>{indicator.period}</td>
              <td>{indicator.value}</td>
              <td>{indicator.unit}</td>
              <td>
                <a href={indicator.source_url}>{indicator.source_name}</a>
              </td>
              <td>{new Date(indicator.retrieved_at).toISOString().slice(0, 10)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
