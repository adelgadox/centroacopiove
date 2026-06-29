import { auth } from "@/auth"

export default async function DashboardPage() {
  const session = await auth()
  const centerRole = session?.centerRole

  return (
    <div>
      <h1 className="text-2xl font-semibold text-zinc-900 mb-1">Panel de control</h1>
      <p className="text-sm text-zinc-500 mb-8">
        {centerRole === "national_admin"
          ? "Vista agregada nacional — todos los centros."
          : centerRole === "coordinator"
          ? "Vista de coordinador — tu centro."
          : "Vista de voluntario — tu centro."}
      </p>
      <div className="rounded-xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600">
        Fase 0 completada. Las secciones de intake, cajas, tarimas y envíos se activarán en las siguientes fases.
      </div>
    </div>
  )
}
