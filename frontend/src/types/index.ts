// ── Platform user ─────────────────────────────────────────────────────────────

export interface User {
  id: string
  email: string
  username: string
  full_name: string | null
  avatar_url: string | null
  role: "user" | "admin" | "superadmin"
  plan: "free" | "pro"
  is_active: boolean
  is_verified: boolean
  created_at: string
}

// ── Domain ────────────────────────────────────────────────────────────────────

export type CenterRole = "national_admin" | "coordinator" | "volunteer"

export type ProductCategory =
  | "MEDICINE"
  | "MEDICAL_SUPPLY"
  | "FOOD"
  | "WATER"
  | "HYGIENE"
  | "TOOL"
  | "RESCUE_GEAR"
  | "OTHER"

export interface Center {
  id: string
  name: string
  address: string | null
  contact_name: string | null
  contact_email: string | null
  contact_phone: string | null
  is_active: boolean
  created_at: string
}

export type BoxStatus = "DRAFT" | "SEALED" | "SHIPPED" | "REJECTED"
export type PalletStatus = "OPEN" | "CLOSED" | "SHIPPED"
export type ShipmentStatus = "OPEN" | "CLOSED" | "SHIPPED"

export interface ProductType {
  id: string
  category: ProductCategory
  display_name: string
  unspsc_code: string | null
  inn_name: string | null
  brand: string | null
  strength: string | null
  form: string | null
  gtin: string | null
  default_unit: string | null
  is_controlled: boolean
  min_shelf_life_days: number | null
  created_at: string
}

export interface BoxOut {
  id: string
  code: string
  product_type_id: string
  quantity: number
  unit: string
  batch: string | null
  expiry_date: string | null
  weight_kg: string | null
  status: BoxStatus
  reject_reason: string | null
  created_at: string
}

export interface IntakeOut {
  id: string
  center_id: string
  donante_libre: string | null
  notes: string | null
  created_at: string
  boxes: BoxOut[]
}

export interface BoxPublicOut {
  code: string
  status: string
  category: string
  display_name: string
  quantity: number
  unit: string
  expiry_date: string | null
  sealed_at: string | null
}

export interface PalletOut {
  id: string
  code: string
  center_id: string
  shipment_id: string | null
  status: PalletStatus
  notes: string | null
  closed_at: string | null
  created_at: string
}

export interface PalletDetailOut extends PalletOut {
  boxes: BoxOut[]
}

export interface PalletPublicOut {
  code: string
  status: PalletStatus
  center_name: string
  box_count: number
  closed_at: string | null
}

export interface ShipmentOut {
  id: string
  center_id: string | null
  destination: string
  carrier: string | null
  reference: string | null
  status: ShipmentStatus
  notes: string | null
  closed_at: string | null
  shipped_at: string | null
  created_at: string
}

export interface ShipmentDetailOut extends ShipmentOut {
  pallets: PalletDetailOut[]
}
