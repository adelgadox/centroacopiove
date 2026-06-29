"use client"

import { useActionState } from "react"
import { loginAction } from "@/lib/actions"

export default function LoginPage() {
  const [error, formAction, isPending] = useActionState(loginAction, null)

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-50">
      <div className="w-full max-w-sm bg-white rounded-2xl shadow-sm border border-zinc-200 p-8">
        <h1 className="text-2xl font-semibold text-zinc-900 mb-1">Acopio</h1>
        <p className="text-sm text-zinc-500 mb-6">Centro de coordinación humanitaria</p>

        <form action={formAction} className="space-y-4">
          <input type="hidden" name="callbackUrl" value="/dashboard" />

          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-1">
              Email o usuario
            </label>
            <input
              name="identifier"
              type="text"
              autoComplete="username"
              required
              className="w-full rounded-lg border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-700 mb-1">
              Contraseña
            </label>
            <input
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="w-full rounded-lg border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
            />
          </div>

          {error?.error && (
            <p className="text-sm text-red-600">
              {error.error === "email_not_verified"
                ? "Verifica tu email antes de iniciar sesión."
                : error.error === "account_disabled"
                ? "Tu cuenta está desactivada."
                : "Credenciales inválidas."}
            </p>
          )}

          <button
            type="submit"
            disabled={isPending}
            className="w-full rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-700 disabled:opacity-50"
          >
            {isPending ? "Entrando…" : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  )
}
