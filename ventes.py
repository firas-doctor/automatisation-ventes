import csv
import os
import sys

# Vérification de la disponibilité de matplotlib
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

TVA_TAUX = 0.20  # 20 %

def generer_ventes_csv(chemin: str = "ventes.csv") -> None:
    """Génère un fichier ventes.csv avec des données d'exemple."""
    donnees = [
        ["ID", "Prix", "Quantite", "Remise"],
        [101, 15.0,  3, 10],
        [102, 25.0,  2,  5],
        [103, 10.0,  5,  0],
        [104, 50.0,  1, 20],
        [105, 8.50,  8,  0],
        [106, 30.0,  4, 15],
        [107, 12.0,  6,  5],
        [108, 75.0,  2, 25],
    ]
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(donnees)
    print(f"[OK] Fichier '{chemin}' généré avec {len(donnees) - 1} produits.")
 
def calculer_resultats(chemin_csv: str) -> list[dict]:
    """
    Lit un CSV et calcule pour chaque ligne :
      - CA Brut  = Prix × Quantité
      - CA Net   = CA Brut × (1 - Remise/100)
      - TVA      = CA Net × TVA_TAUX
      - CA TTC   = CA Net + TVA
    Retourne une liste de dicts.
    """
    resultats = []
    with open(chemin_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for ligne in reader:
            prix      = float(ligne["Prix"])
            quantite  = int(ligne["Quantite"])
            remise    = float(ligne["Remise"])          # en %
 
            ca_brut   = prix * quantite
            ca_net    = ca_brut * (1 - remise / 100)
            tva       = ca_net * TVA_TAUX
            ca_ttc    = ca_net + tva
 
            resultats.append({
                "ID"       : ligne["ID"],
                "Prix"     : prix,
                "Quantite" : quantite,
                "Remise"   : remise,
                "CA_Brut"  : round(ca_brut, 2),
                "CA_Net"   : round(ca_net,  2),
                "TVA"      : round(tva,     2),
                "CA_TTC"   : round(ca_ttc,  2),
            })
    return resultats
 
 
# ── 5. CA Total ───────────────────────────────────────────────────────────────
 
def afficher_ca_total(resultats: list[dict]) -> float:
    total = sum(r["CA_TTC"] for r in resultats)
    print(f"\n{'='*45}")
    print(f"  CA Total (TTC) de l'entreprise : {total:.2f} €")
    print(f"{'='*45}")
    return total
 
 
# ── 6. Produit le plus rentable ───────────────────────────────────────────────
 
def identifier_top_produit(resultats: list[dict]) -> dict:
    top = max(resultats, key=lambda r: r["CA_Net"])
    print(f"\n[TOP] Produit avec le plus gros bénéfice :")
    print(f"       ID={top['ID']}  |  CA Net={top['CA_Net']:.2f} €  |  CA TTC={top['CA_TTC']:.2f} €")
    return top
 
 
# ── 7. Export resultats_final.csv ─────────────────────────────────────────────
 
def exporter_resultats(resultats: list[dict], chemin: str = "resultats_final.csv") -> None:
    colonnes = ["ID", "Prix", "Quantite", "Remise", "CA_Brut", "CA_Net", "TVA", "CA_TTC"]
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(resultats)
    print(f"\n[OK] Résultats exportés dans '{chemin}'.")
 
 
# ── Bonus : Graphiques Matplotlib ────────────────────────────────────────────
 
def afficher_graphiques(resultats: list[dict]) -> None:
    if not MATPLOTLIB_AVAILABLE:
        print("[SKIP] Matplotlib absent — graphiques non générés.")
        return
 
    ids    = [r["ID"]     for r in resultats]
    ca_net = [r["CA_Net"] for r in resultats]
    ca_ttc = [r["CA_TTC"] for r in resultats]
 
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Analyse des Ventes", fontsize=14, fontweight="bold")
 
    # Graphique 1 : CA Net par produit (barres)
    axes[0].bar(ids, ca_net, color="steelblue", edgecolor="white")
    axes[0].set_title("CA Net par produit")
    axes[0].set_xlabel("ID Produit")
    axes[0].set_ylabel("CA Net (€)")
    axes[0].grid(axis="y", linestyle="--", alpha=0.5)
 
    # Graphique 2 : Répartition CA TTC (camembert)
    axes[1].pie(
        ca_ttc,
        labels=ids,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Paired.colors,
    )
    axes[1].set_title("Répartition du CA TTC")
 
    plt.tight_layout()
    plt.savefig("graphiques_ventes.png", dpi=150)
    plt.show()
    print("[OK] Graphique sauvegardé dans 'graphiques_ventes.png'.")
 
 def exporter_excel(resultats: list[dict], chemin: str = "resultats_final.xlsx") -> None:
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Résultats Ventes"
        colonnes = ["ID","Prix","Quantite","Remise","CA_Brut","CA_Net","TVA","CA_TTC"]
        ws.append(colonnes)
        for r in resultats:
            ws.append([r[c] for c in colonnes])
        wb.save(chemin)
        print(f"[OK] Export Excel → '{chemin}'")
    except ImportError:
        print("[SKIP] openpyxl absent — export Excel ignoré.")
# ── Point d'entrée ────────────────────────────────────────────────────────────
 
def main():
    # Bonus : lecture dynamique — accepte un chemin en argument
    chemin_csv = sys.argv[1] if len(sys.argv) > 1 else "ventes.csv"
 
    # Étape 1 : générer le CSV seulement s'il n'existe pas encore
    if not os.path.exists(chemin_csv):
        generer_ventes_csv(chemin_csv)
    else:
        print(f"[INFO] Fichier '{chemin_csv}' déjà présent — lecture directe.")
 
    # Étapes 2-4 : calculs
    resultats = calculer_resultats(chemin_csv)
 
    # Aperçu console
    print(f"\n{'ID':>5} {'Prix':>8} {'Qté':>5} {'Rem%':>6} "
          f"{'CA Brut':>10} {'CA Net':>10} {'TVA':>8} {'CA TTC':>10}")
    print("-" * 67)
    for r in resultats:
        print(f"{r['ID']:>5} {r['Prix']:>8.2f} {r['Quantite']:>5} {r['Remise']:>6.1f} "
              f"{r['CA_Brut']:>10.2f} {r['CA_Net']:>10.2f} {r['TVA']:>8.2f} {r['CA_TTC']:>10.2f}")
 
    # Étape 5 : CA Total
    afficher_ca_total(resultats)
 
    # Étape 6 : Top produit
    identifier_top_produit(resultats)
 
    # Étape 7 : Export
    exporter_resultats(resultats)
 
    # Bonus : graphiques
    afficher_graphiques(resultats)
 
 
if __name__ == "__main__":
    main()