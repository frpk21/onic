import pandas as pd
from dashboard.models import ChiaDataset

def get_dataframe():
    qs = ChiaDataset.objects.all().values()
    return pd.DataFrame(list(qs))

def piramide_poblacional(df):
    df = df[df["edad"].notna()]
    df["edad"] = df["edad"].astype(int)

    bins = list(range(0, 90, 5)) + [150]
    labels = [f"{i}-{i+4}" for i in range(0, 85, 5)] + ["85+"]

    df["grupo"] = pd.cut(df["edad"], bins=bins, labels=labels, right=False)

    pivot = df.groupby(["grupo", "sexo"]).size().unstack(fill_value=0)
    return pivot.reset_index()

def dependencia(df):
    df = df[df["edad"].notna()]
    df["edad"] = df["edad"].astype(int)

    p0_14 = df[df["edad"] < 15].shape[0]
    p15_64 = df[(df["edad"] >= 15) & (df["edad"] <= 64)].shape[0]
    p65 = df[df["edad"] >= 65].shape[0]

    return {
        "dependencia_juvenil": round(p0_14 / p15_64 * 100, 2) if p15_64 else 0,
        "dependencia_senil": round(p65 / p15_64 * 100, 2) if p15_64 else 0,
        "dependencia_total": round((p0_14 + p65) / p15_64 * 100, 2) if p15_64 else 0,
    }

def indice_myers(df):
    df = df[df["edad"].notna()]
    df["edad"] = df["edad"].astype(int)
    digits = df["edad"] % 10
    N = len(df)
    obs = digits.value_counts().sort_index()
    obs_pct = obs / N * 100
    expected = 10
    return round(abs(obs_pct - expected).sum() / 2, 2)
