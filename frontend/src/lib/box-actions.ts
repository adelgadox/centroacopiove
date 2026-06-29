"use server"

import { auth } from "@/auth"
import { apiFetch } from "@/lib/api"
import { revalidatePath } from "next/cache"

export async function sealBoxAction(boxId: string) {
  const session = await auth()
  if (!session?.accessToken) return { error: "No autenticado" }

  try {
    const data = await apiFetch(`/v1/boxes/${boxId}/seal`, {
      method: "POST",
      token: session.accessToken,
    })
    revalidatePath("/dashboard/boxes")
    return { data }
  } catch (err: unknown) {
    return { error: err instanceof Error ? err.message : "Error al sellar caja" }
  }
}

export async function downloadLabelsPdfAction(status: string = "DRAFT") {
  const session = await auth()
  if (!session?.accessToken) return { error: "No autenticado" }

  try {
    const API_URL = process.env.API_URL ?? "http://localhost:8000"
    const res = await fetch(`${API_URL}/v1/boxes/labels/pdf?status=${status}`, {
      headers: { Authorization: `Bearer ${session.accessToken}` },
    })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      return { error: body.error?.message ?? "Error al generar PDF" }
    }
    // Return the PDF as base64 so the client can trigger download
    const buffer = await res.arrayBuffer()
    const base64 = Buffer.from(buffer).toString("base64")
    return { pdf: base64, filename: `etiquetas-${status.toLowerCase()}.pdf` }
  } catch (err: unknown) {
    return { error: err instanceof Error ? err.message : "Error al generar PDF" }
  }
}
