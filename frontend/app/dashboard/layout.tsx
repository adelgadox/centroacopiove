import { auth } from "@/auth"
import { redirect } from "next/navigation"
import { Sidebar } from "@/components/Sidebar"
import { CenterSelector } from "@/components/CenterSelector"
import type { CenterRole } from "@/types"

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const session = await auth()
  if (!session) redirect("/login")

  const centerRole = (session.centerRole as CenterRole | null) ?? null

  return (
    <div className="flex h-screen overflow-hidden bg-zinc-50">
      <div className="flex h-full flex-col">
        {centerRole === "national_admin" && (
          <CenterSelector token={session.accessToken} />
        )}
        <Sidebar centerRole={centerRole} />
      </div>
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  )
}
