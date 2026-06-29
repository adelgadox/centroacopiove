import { auth } from "@/auth"
import { redirect } from "next/navigation"
import { apiFetch } from "@/lib/api"
import type { Center } from "@/types"

export default async function CentersPage() {
  const session = await auth()
  if (session?.centerRole !== "national_admin") redirect("/dashboard")

  let centers: Center[] = []
  try {
    centers = await apiFetch<Center[]>("/v1/centers", {
      token: session.accessToken,
      next: { revalidate: 60, tags: ["centers"] },
    })
  } catch {
    centers = []
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-zinc-900">Centros de acopio</h1>
        <span className="text-sm text-zinc-500">{centers.length} centro{centers.length !== 1 ? "s" : ""}</span>
      </div>

      {centers.length === 0 ? (
        <div className="rounded-xl border border-zinc-200 bg-white p-8 text-center text-sm text-zinc-500">
          No hay centros registrados aún.
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {centers.map((c) => (
            <div key={c.id} className="rounded-xl border border-zinc-200 bg-white p-4">
              <div className="flex items-start justify-between">
                <span className="font-medium text-zinc-900">{c.name}</span>
                <span
                  className={`ml-2 shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${
                    c.is_active
                      ? "bg-green-100 text-green-700"
                      : "bg-zinc-100 text-zinc-500"
                  }`}
                >
                  {c.is_active ? "Activo" : "Inactivo"}
                </span>
              </div>
              {c.address && (
                <p className="mt-1 text-xs text-zinc-500 truncate">{c.address}</p>
              )}
              {c.contact_email && (
                <p className="mt-0.5 text-xs text-zinc-400 truncate">{c.contact_email}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
