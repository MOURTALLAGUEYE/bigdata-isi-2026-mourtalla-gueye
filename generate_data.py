#!/usr/bin/env python3
"""Génère les fichiers de données du TP Big Data Engineering."""
from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


def build_dataset(scale: float, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    np.random.seed(42)

    n_customers = int(5000 * scale)
    n_orders = int(50000 * scale)
    n_order_items = int(113000 * scale)
    n_events = int(330000 * scale)

    customers = []
    for i in range(1, n_customers + 1):
        customers.append(
            {
                "customer_id": i,
                "nom": f"Client {i}",
                "email": f"client{i}@example.com",
                "ville": random.choice(["Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor"]),
                "date_naissance": f"19{random.randint(80, 99)}-0{random.randint(1, 9)}-0{random.randint(1, 9)}",
                "date_inscription": "2024-01-01",
            }
        )
    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(outdir / "customers.csv", index=False)

    orders = []
    for i in range(1, n_orders + 1):
        amount = random.randint(1000, 50000)
        montant = str(amount) if random.random() > 0.01 else f"{amount} FCFA"
        orders.append(
            {
                "order_id": i,
                "customer_id": (i % n_customers) + 1,
                "date_commande": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "statut": random.choices(["livrée", "annulée", "en_cours", "retournée"], weights=[0.78, 0.09, 0.08, 0.05])[0],
                "canal": random.choice(["mobile_app", "site_web", "boutique", "call_center"]),
                "montant_total_fcfa": montant,
            }
        )
    df_orders = pd.DataFrame(orders)
    df_orders.to_csv(outdir / "orders.csv", index=False)

    order_items = []
    for i in range(1, n_order_items + 1):
        order_items.append(
            {
                "order_id": (i % n_orders) + 1,
                "product_id": f"SKU-{random.randint(1, 1000)}",
                "quantite": random.randint(1, 3),
                "prix_unitaire": round(random.uniform(5, 200), 2),
            }
        )
    df_order_items = pd.DataFrame(order_items)
    df_order_items.to_csv(outdir / "order_items.csv", index=False)

    events = []
    for i in range(1, n_events + 1):
        events.append(
            {
                "event_id": i,
                "order_id": (i % n_orders) + 1,
                "customer_id": (i % n_customers) + 1,
                "event_type": random.choice(["view", "click", "purchase", "refund"]),
                "ts": f"2024-01-01T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
                "amount": round(random.uniform(0, 5000), 2),
            }
        )
    with (outdir / "events.json").open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event) + "\n")

    print(f"Données générées dans {outdir}")
    print(f"- customers: {len(df_customers)}")
    print(f"- orders: {len(df_orders)}")
    print(f"- order_items: {len(df_order_items)}")
    print(f"- events: {len(events)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=float, default=0.1)
    parser.add_argument("--outdir", type=str, default="data")
    args = parser.parse_args()

    outdir = Path(args.outdir).resolve()
    build_dataset(args.scale, outdir)


if __name__ == "__main__":
    main()
