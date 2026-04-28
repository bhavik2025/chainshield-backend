"""
Seed the database on first run.
Creates ONE admin account and populates lookup tables.
Safe to call multiple times — skips if any user already exists.
"""
import uuid
import random
from sqlalchemy.orm import Session
import models
from auth import hash_password


def _gen_chat_number(db) -> str:
    for _ in range(200):
        num = str(random.randint(10000, 99999))
        if not db.query(models.User).filter(models.User.chat_number == num).first():
            return num
    return "10000"


def seed(db: Session):
    if db.query(models.User).count() > 0:
        return

    print("[ChainShield] Seeding initial data...")

    # Single admin account
    admin = models.User(
        id=f"USR-{uuid.uuid4().hex[:8].upper()}",
        name="Bhavik Visani",
        email="bhavik@gmail.com",
        password_hash=hash_password("Chain@123"),
        role="admin",
        company="ChainShield",
        active=True,
        chat_number=_gen_chat_number(db),
    )
    db.add(admin)

    # Base logistics hubs
    hubs = [
        ("Shanghai",    "China",       31.2304,  121.4737),
        ("Singapore",   "Singapore",    1.3521,  103.8198),
        ("Rotterdam",   "Netherlands", 51.9244,    4.4777),
        ("Los Angeles", "USA",         34.0522, -118.2437),
        ("Dubai",       "UAE",         25.2048,   55.2708),
        ("Mumbai",      "India",       19.0760,   72.8777),
        ("Frankfurt",   "Germany",     50.1109,    8.6821),
        ("Tokyo",       "Japan",       35.6762,  139.6503),
        ("New York",    "USA",         40.7128,  -74.0060),
        ("Hamburg",     "Germany",     53.5511,    9.9937),
        ("Hong Kong",   "China",       22.3193,  114.1694),
        ("London",      "UK",          51.5074,   -0.1278),
        ("Paris",       "France",      48.8566,    2.3522),
        ("Delhi",       "India",       28.6139,   77.2090),
        ("Detroit",     "USA",         42.3314,  -83.0458),
        ("Istanbul",    "Turkey",      41.0082,   28.9784),
        ("Sydney",      "Australia",  -33.8688,  151.2093),
        ("Sao Paulo",   "Brazil",     -23.5505,  -46.6333),
        ("Chicago",     "USA",         41.8781,  -87.6298),
        ("Osaka",       "Japan",       34.6937,  135.5023),
    ]
    db.add_all([models.BaseCity(city=c, country=cn, lat=la, lng=ln) for c, cn, la, ln in hubs])

    # Cargo types
    cargo_types = [
        "Consumer Electronics", "Pharmaceuticals", "Automotive Components", "Textiles",
        "Agriculture / Food", "Luxury Goods", "Medical Devices", "Machinery / Industrial",
        "Chemicals", "Oil & Gas", "Construction Materials", "Apparel / Fashion",
        "Furniture", "Plastics", "Paper / Pulp", "Raw Materials",
        "Refrigerated Goods", "Hazardous Materials", "E-Commerce Parcels", "Other",
    ]
    db.add_all([models.CargoType(name=n) for n in cargo_types])

    db.commit()
    print("[ChainShield] Seed complete. Admin: bhavik@gmail.com / Chain@123")
