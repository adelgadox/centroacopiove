import { auth } from "@/auth"
import { apiFetch } from "@/lib/api"
import { NextResponse } from "next/server"
import type { NationalDashboardOut } from "@/types"

export async function GET() {
  const session = await auth()
  if (!session?.accessToken) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  const data = await apiFetch<NationalDashboardOut>("/v1/dashboard/national", {
    token: session.accessToken,
    next: { revalidate: 120, tags: ["dashboard"] },
  })
  return NextResponse.json(data)
}
