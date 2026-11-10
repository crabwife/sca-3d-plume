from pathlib import Path
import json

import numpy as np
import seaborn as sns
from scipy.special import ndtr


def load_config():
    return json.loads(Path('../input/model_config.json').read_text())


def jump_prob(velocity, diffusivity, spacing, dt):
    # first two central moments in free air
    drift = np.asarray(velocity) * dt / spacing
    second = 2 * diffusivity * dt / spacing**2 + drift**2
    return np.stack([(second - drift) / 2, 1 - second, (second + drift) / 2], axis=-1)


def split_point(centers, point):
    right = int(np.searchsorted(centers, point, side='right'))
    if right == 0:
        return [(0, 1.0)]
    if right == len(centers):
        return [(right - 1, 1.0)]
    fraction = (point - centers[right - 1]) / (centers[right] - centers[right - 1])
    return [(right - 1, 1 - fraction), (right, fraction)]


def normal_density(coordinate, center, sd):
    return np.exp(-0.5 * ((coordinate - center) / sd)**2) / (np.sqrt(2 * np.pi) * sd)


def normal_cell_mass(edges, center, sd):
    return np.diff(ndtr((edges - center) / sd))


def plot_setup():
    sns.set_theme(style='ticks', context='notebook', palette='colorblind')
    return sns.color_palette('colorblind')


def save_figure(fig, output, name):
    fig.savefig(output / f'{name}.png', dpi=160, bbox_inches='tight', facecolor='white')
    fig.savefig(output / f'{name}.pdf', bbox_inches='tight', facecolor='white')
