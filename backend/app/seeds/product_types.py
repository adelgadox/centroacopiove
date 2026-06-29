"""Semilla de ProductType con productos humanitarios comunes.

Basado en UNSPSC segmento 51 (medicamentos), 42 (insumos médicos), 50 (alimentos),
47 (higiene/agua) y categorías de rescate. Cubre los ítems más frecuentes en
envíos humanitarios México → Venezuela.

Uso:
    cd backend
    python -m app.seeds.product_types
"""

from app.database import SessionLocal
from app.models.product_type import ProductType

SEED_DATA = [
    # ── MEDICINE ──────────────────────────────────────────────────────────────
    dict(category="MEDICINE", display_name="Ibuprofeno 400mg tableta",
         inn_name="Ibuprofeno", strength="400mg", form="tableta",
         unspsc_code="51102200", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Ibuprofeno 600mg tableta",
         inn_name="Ibuprofeno", strength="600mg", form="tableta",
         unspsc_code="51102200", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Paracetamol 500mg tableta",
         inn_name="Paracetamol", strength="500mg", form="tableta",
         unspsc_code="51102100", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Paracetamol 250mg/5ml jarabe",
         inn_name="Paracetamol", strength="250mg/5ml", form="jarabe",
         unspsc_code="51102100", default_unit="frascos", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Amoxicilina 500mg cápsula",
         inn_name="Amoxicilina", strength="500mg", form="cápsula",
         unspsc_code="51111500", default_unit="cápsulas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Amoxicilina 250mg/5ml suspensión",
         inn_name="Amoxicilina", strength="250mg/5ml", form="suspensión",
         unspsc_code="51111500", default_unit="frascos", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Metformina 850mg tableta",
         inn_name="Metformina", strength="850mg", form="tableta",
         unspsc_code="51181700", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Omeprazol 20mg cápsula",
         inn_name="Omeprazol", strength="20mg", form="cápsula",
         unspsc_code="51191600", default_unit="cápsulas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Sales de rehidratación oral sobres",
         inn_name="Sales de rehidratación oral", strength="OMS", form="polvo sobre",
         unspsc_code="51102700", default_unit="sobres", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Vitamina C 500mg tableta",
         inn_name="Ácido ascórbico", strength="500mg", form="tableta",
         unspsc_code="51171500", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Ácido fólico 5mg tableta",
         inn_name="Ácido fólico", strength="5mg", form="tableta",
         unspsc_code="51171500", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Sulfato ferroso 300mg tableta",
         inn_name="Sulfato ferroso", strength="300mg", form="tableta",
         unspsc_code="51171500", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Loratadina 10mg tableta",
         inn_name="Loratadina", strength="10mg", form="tableta",
         unspsc_code="51141600", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Metronidazol 500mg tableta",
         inn_name="Metronidazol", strength="500mg", form="tableta",
         unspsc_code="51111700", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Ciprofloxacino 500mg tableta",
         inn_name="Ciprofloxacino", strength="500mg", form="tableta",
         unspsc_code="51111600", default_unit="tabletas", min_shelf_life_days=365),
    dict(category="MEDICINE", display_name="Insulina NPH 100UI/ml vial",
         inn_name="Insulina isofana", strength="100UI/ml", form="solución inyectable",
         unspsc_code="51181500", default_unit="viales", min_shelf_life_days=365,
         is_controlled=False),

    # ── MEDICAL_SUPPLY ────────────────────────────────────────────────────────
    dict(category="MEDICAL_SUPPLY", display_name="Gasas estériles 10x10cm",
         unspsc_code="42311500", default_unit="paquetes"),
    dict(category="MEDICAL_SUPPLY", display_name="Vendas elásticas 10cm",
         unspsc_code="42311500", default_unit="unidades"),
    dict(category="MEDICAL_SUPPLY", display_name="Guantes de látex talla M caja",
         unspsc_code="42131600", default_unit="cajas"),
    dict(category="MEDICAL_SUPPLY", display_name="Jeringas desechables 5ml",
         unspsc_code="42142500", default_unit="unidades"),
    dict(category="MEDICAL_SUPPLY", display_name="Alcohol isopropílico 70% 1L",
         unspsc_code="51241500", default_unit="botellas"),
    dict(category="MEDICAL_SUPPLY", display_name="Agua oxigenada 3% 250ml",
         unspsc_code="51241500", default_unit="botellas"),
    dict(category="MEDICAL_SUPPLY", display_name="Termómetro digital",
         unspsc_code="41111500", default_unit="unidades"),
    dict(category="MEDICAL_SUPPLY", display_name="Glucómetro + tiras reactivas",
         unspsc_code="41116100", default_unit="kits"),
    dict(category="MEDICAL_SUPPLY", display_name="Mascarillas quirúrgicas caja x50",
         unspsc_code="42131600", default_unit="cajas"),

    # ── FOOD ──────────────────────────────────────────────────────────────────
    dict(category="FOOD", display_name="Arroz blanco 1kg",
         unspsc_code="50201700", default_unit="kg", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Pasta/espagueti 500g",
         unspsc_code="50201900", default_unit="paquetes", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Frijoles negros 1kg",
         unspsc_code="50201800", default_unit="kg", min_shelf_life_days=365),
    dict(category="FOOD", display_name="Lentejas 1kg",
         unspsc_code="50201800", default_unit="kg", min_shelf_life_days=365),
    dict(category="FOOD", display_name="Atún en lata 170g",
         unspsc_code="50192100", default_unit="latas", min_shelf_life_days=365),
    dict(category="FOOD", display_name="Sardinas en lata 425g",
         unspsc_code="50192100", default_unit="latas", min_shelf_life_days=365),
    dict(category="FOOD", display_name="Leche en polvo 400g",
         unspsc_code="50151500", default_unit="latas", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Leche de fórmula infantil 400g",
         unspsc_code="50151500", default_unit="latas", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Aceite vegetal 1L",
         unspsc_code="50171900", default_unit="botellas", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Harina de maíz precocida 1kg",
         unspsc_code="50201700", default_unit="kg", min_shelf_life_days=180),
    dict(category="FOOD", display_name="Azúcar blanca 1kg",
         unspsc_code="50221000", default_unit="kg", min_shelf_life_days=365),
    dict(category="FOOD", display_name="Sal yodada 1kg",
         unspsc_code="50221100", default_unit="kg", min_shelf_life_days=730),
    dict(category="FOOD", display_name="Avena en hojuelas 500g",
         unspsc_code="50201700", default_unit="paquetes", min_shelf_life_days=180),

    # ── WATER ─────────────────────────────────────────────────────────────────
    dict(category="WATER", display_name="Agua purificada 500ml",
         unspsc_code="47131700", default_unit="botellas", min_shelf_life_days=180),
    dict(category="WATER", display_name="Agua purificada 1.5L",
         unspsc_code="47131700", default_unit="botellas", min_shelf_life_days=180),
    dict(category="WATER", display_name="Pastillas purificadoras de agua (Aquatabs)",
         unspsc_code="47131700", default_unit="tabletas"),

    # ── HYGIENE ───────────────────────────────────────────────────────────────
    dict(category="HYGIENE", display_name="Jabón en barra 150g",
         unspsc_code="53131600", default_unit="barras"),
    dict(category="HYGIENE", display_name="Shampoo 400ml",
         unspsc_code="53131500", default_unit="botellas"),
    dict(category="HYGIENE", display_name="Pasta dental 75ml",
         unspsc_code="53131700", default_unit="tubos"),
    dict(category="HYGIENE", display_name="Cepillo dental",
         unspsc_code="53131700", default_unit="unidades"),
    dict(category="HYGIENE", display_name="Toallas sanitarias paquete x10",
         unspsc_code="53102500", default_unit="paquetes"),
    dict(category="HYGIENE", display_name="Pañales talla M paquete",
         unspsc_code="53102400", default_unit="paquetes"),
    dict(category="HYGIENE", display_name="Papel higiénico 4 rollos",
         unspsc_code="14111700", default_unit="paquetes"),
    dict(category="HYGIENE", display_name="Desinfectante multiusos 1L",
         unspsc_code="47131600", default_unit="botellas"),

    # ── TOOL ──────────────────────────────────────────────────────────────────
    dict(category="TOOL", display_name="Linterna LED recargable",
         unspsc_code="39111600", default_unit="unidades"),
    dict(category="TOOL", display_name="Pilas AA paquete x4",
         unspsc_code="26111700", default_unit="paquetes"),
    dict(category="TOOL", display_name="Cobija/frazada polar 1.5x2m",
         unspsc_code="52121500", default_unit="unidades"),

    # ── RESCUE_GEAR ───────────────────────────────────────────────────────────
    dict(category="RESCUE_GEAR", display_name="Botiquín de primeros auxilios básico",
         unspsc_code="42171500", default_unit="kits"),
    dict(category="RESCUE_GEAR", display_name="Chaleco salvavidas",
         unspsc_code="46181600", default_unit="unidades"),
]


def seed(db=None) -> None:
    close = db is None
    if db is None:
        db = SessionLocal()
    try:
        from sqlalchemy import select
        existing = set(
            r[0] for r in db.execute(
                select(ProductType.display_name)
            ).all()
        )
        added = 0
        for item in SEED_DATA:
            if item["display_name"] not in existing:
                db.add(ProductType(**item))
                added += 1
        db.commit()
        print(f"Seed complete: {added} product types added ({len(existing)} already existed).")
    finally:
        if close:
            db.close()


if __name__ == "__main__":
    seed()
