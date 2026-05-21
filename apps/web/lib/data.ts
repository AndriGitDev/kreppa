import fs from "node:fs";
import path from "node:path";

export type Indicator = {
  id: string;
  label_is: string;
  label_en: string;
  value: number;
  unit: string;
  period: string;
  stress_score: number;
  source_id: string;
  source_name: string;
  source_url: string;
  retrieved_at: string;
};

export type Component = {
  id: string;
  label_is: string;
  label_en: string;
  score: number | null;
  weight: number;
  confidence: number;
  indicators: Indicator[];
  missing_or_stale: string[];
};

export type Latest = {
  schema_version: string;
  score_version: string;
  generated_at: string;
  as_of: string;
  overall: {
    score: number;
    raw_score: number;
    confidence: number;
    confidence_label: string;
    level: { label_is: string; label_en: string; emoji: string };
  };
  components: Component[];
  drivers: {
    up: Array<{ indicator_id: string; label_is: string; reason_is: string; contribution: number }>;
    down: Array<{ indicator_id: string; label_is: string; reason_is: string; contribution: number }>;
  };
  warnings: string[];
  attribution: string[];
};

export function readData<T>(file: string): T {
  const fullPath = path.join(process.cwd(), "apps/web/public/data", file);
  return JSON.parse(fs.readFileSync(fullPath, "utf8")) as T;
}

export function allIndicators(latest: Latest): Indicator[] {
  return latest.components.flatMap((component) => component.indicators);
}
