import { auth } from "@/auth"
import { apiFetch } from "@/lib/api"
import { NextResponse } from "next/server"

export async function GET(request: Request) {
  const session = await auth()
  const { searchParams } = new URL(request.url)
  const activeOnly = searchParams.get("active_only") === "true"
  try {
    const data = await apiFetch(
      `/v1/campaigns${activeOnly ? "?active_only=true" : ""}`,
      { token: session?.accessToken }
    )
    return NextResponse.json(data)
  } catch {
    return NextResponse.json([], { status: 200 })
  }
}
