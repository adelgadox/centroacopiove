import { auth } from "@/auth"
import { NextRequest, NextResponse } from "next/server"

const API_URL = process.env.API_URL ?? "http://localhost:8000"

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ gtin: string }> }
) {
  const session = await auth()
  if (!session?.accessToken) return NextResponse.json({ error: "Unauthenticated" }, { status: 401 })

  const { gtin } = await params

  const res = await fetch(`${API_URL}/v1/product-types/barcode/${encodeURIComponent(gtin)}`, {
    headers: { Authorization: `Bearer ${session.accessToken}` },
    next: { revalidate: 0 },
  })

  const data = await res.json()
  return NextResponse.json(data, { status: res.status })
}
