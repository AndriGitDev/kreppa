# kreppa.is

`kreppa.is` is a static-first Iceland economic stress dashboard. It pulls public Statistics Iceland data, normalizes observations, computes a deterministic 0-100 `Kreppumaelir` score, and explains the main drivers.

It is not a prediction engine, investment tool, bank-risk monitor, or financial advice product.

## Local development

```bash
npm install
python3 -m pip install -e .[dev]
python3 scripts/fetch_data.py
python3 scripts/score.py
npm run dev
```

The web app is in `apps/web` and reads static JSON from `apps/web/public/data`.

## Data update

```bash
python3 scripts/fetch_data.py
python3 scripts/score.py
python3 scripts/validate_outputs.py
```

The pipeline writes normalized observations to `data/snapshots/observations.json`, score outputs to `data/snapshots`, and web-ready JSON to `apps/web/public/data`.

## Scoring

Scoring model `0.2.0` maps each indicator to a 0-100 stress score using a 70/30 blend of percentile stress and configured threshold stress where thresholds exist. Higher scores mean higher public-data stress. Missing or stale indicators are excluded from component scoring and reduce confidence.

Component weights and indicator definitions live in `data/catalog/indicators.yaml`.

## Adding an indicator

1. Verify the official endpoint and record it in `data_source_audit.md`.
2. Add the PX-Web source definition to `data/catalog/sources.yaml`.
3. Add the indicator, transform, direction, threshold, and freshness rule to `data/catalog/indicators.yaml`.
4. Run the fetch, score, validation, and tests.

## Source attribution

Initial MVP data comes from Statistics Iceland PX-Web tables. Statistics Iceland published content is reused under CC BY 4.0 with attribution. Central Bank sources are documented as pending where stable machine-readable endpoints have not yet been wired.

## License

MIT for the application code. Data remains governed by the source providers' terms and attribution requirements.
