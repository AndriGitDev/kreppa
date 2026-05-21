export function DriverList({
  title,
  drivers
}: {
  title: string;
  drivers: Array<{ indicator_id: string; label_is: string; reason_is: string; contribution: number }>;
}) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {drivers.length === 0 ? <p className="muted">Ekkert marktækt ennþá.</p> : null}
      {drivers.map((driver) => (
        <div className="driver" key={driver.indicator_id}>
          <strong>{driver.label_is}</strong>
          <p className="muted">{driver.reason_is}</p>
          <span className="driver-score">{driver.contribution > 0 ? "+" : ""}{driver.contribution.toFixed(2)}</span>
        </div>
      ))}
    </div>
  );
}
