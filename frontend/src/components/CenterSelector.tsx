"use client"

import { useState, useEffect } from "react"
import { apiFetch } from "@/lib/api"
import type { Center } from "@/types"

interface CenterSelectorProps {
  token: string
}

export function CenterSelector({ token }: CenterSelectorProps) {
  const [centers, setCenters] = useState<Center[]>([])
  const [selected, setSelected] = useState<string>("all")

  useEffect(() => {
    apiFetch<Center[]>("/v1/centers", { token })
      .then(setCenters)
      .catch(() => {})
  }, [token])

  if (centers.length === 0) return null

  return (
    <div className="flex items-center gap-2 px-2 mb-4">
      <label className="text-xs text-zinc-500">Centro:</label>
      <select
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
        className="flex-1 rounded border border-zinc-200 bg-white px-2 py-1 text-xs text-zinc-900 focus:outline-none"
      >
        <option value="all">Todos los centros</option>
        {centers.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>
    </div>
  )
}
