import { apiFetch } from "@/lib/api"
import { NextResponse } from "next/server"
import type { PublicNeedsOut } from "@/types"

export async function GET() {
  const data = await apiFetch<PublicNeedsOut>("/v1/public/needs", {
    next: { revalidate: 300, tags: ["public-needs"] },
  })
  return NextResponse.json(data, {
    headers: { "Cache-Control": "public, max-age=300, stale-while-revalidate=60" },
  })
}
