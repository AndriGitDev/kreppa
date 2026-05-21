import { NextResponse } from "next/server";
import { readData } from "../../../lib/data";

export function GET() {
  return NextResponse.json(readData("methodology.json"));
}
