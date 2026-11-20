"""
Charte graphique commune (P1-10) : couleurs, textes et enregistrement des figures.

Règles :
- un seul message par graphique, annoncé dans son titre ;
- couleurs lisibles par les personnes daltoniennes : palette catégorielle
  validée, utilisée dans un ordre fixe (jamais recyclée) ;
- une seule couleur forte pour ce qui compte, le reste en bleu ou en gris ;
- textes en noir ou en gris, jamais dans la couleur d'une série.
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

# Palette catégorielle, dans l'ordre d'utilisation
CATEGORIES = [
    "#2a78d6",  # bleu
    "#eb6834",  # orange
    "#1baf7a",  # turquoise
    "#eda100",  # jaune
    "#e87ba4",  # rose
    "#008300",  # vert
    "#6250d6",  # violet
    "#e34948",  # rouge
]
BLUE = CATEGORIES[0]
ORANGE = CATEGORIES[1]

# Rampe séquentielle (une seule teinte, du clair au foncé) pour les cartes de chaleur
BLUE_RAMP = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
    "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
# Divergente : bleu (moins que la moyenne), gris (neutre), rouge (plus que la moyenne)
DIVERGING = ["#2a78d6", "#f0efec", "#e34948"]

TEXT = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
SURFACE = "#fcfcfb"
NEUTRAL = "#b8b6af"

FIGURES_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"


def apply_style():
    """Applique la charte à tous les graphiques matplotlib qui suivent."""
    mpl.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.labelsize": 10,
            "axes.labelcolor": TEXT_SECONDARY,
            "axes.edgecolor": NEUTRAL,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": TEXT_SECONDARY,
            "ytick.color": TEXT_SECONDARY,
            "text.color": TEXT,
            "lines.linewidth": 2,
            "legend.frameon": False,
            "axes.prop_cycle": mpl.cycler(color=CATEGORIES),
        }
    )


def sequential_cmap():
    """Carte de couleurs séquentielle bleue."""
    return LinearSegmentedColormap.from_list("bleu", BLUE_RAMP)


def diverging_cmap():
    """Carte de couleurs divergente bleu, gris, rouge."""
    return LinearSegmentedColormap.from_list("bleu_gris_rouge", DIVERGING)


def thousands(x, _pos=None):
    """Nombre avec une espace entre les milliers : 1 234 567."""
    return f"{x:,.0f}".replace(",", " ")


THOUSANDS = FuncFormatter(thousands)


def decimal_comma(x, _pos=None):
    """Nombre décimal avec une virgule : 1,5."""
    return f"{x:g}".replace(".", ",")


DECIMALS = FuncFormatter(decimal_comma)


def save_figure(fig, name):
    """Enregistre la figure dans docs/figures/<name>.png pour le rapport et les diapositives."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path
