import numpy as np
from scipy.special import ive

from .common import normal_density

# Briggs open-country A–F
BY = np.array([0.22, 0.16, 0.11, 0.08, 0.06, 0.04])
BZ = np.array([0.20, 0.12, 0.08, 0.06, 0.03, 0.016])
CZ = np.array([0, 0, 0.0002, 0.0015, 0.0003, 0.0003])
POWER = np.array([0, 0, 0.5, 0.5, 1, 1])

def rural_widths(x, stability):
    i = stability - 1
    return BY[i]*x/np.sqrt(1 + 0.0001*x), BZ[i]*x/(1 + CZ[i]*x)**POWER[i]

def rotate(east, north, toward_deg):
    theta = np.deg2rad(toward_deg)
    return east*np.sin(theta) + north*np.cos(theta), east*np.cos(theta) - north*np.sin(theta)

def gaussian_cross_section(y, z, height, sy, sz):
    return normal_density(y, 0, sy)*(normal_density(z, height, sz) + normal_density(z, -height, sz))

def lattice_cross_section(y, z, height, sy, sz, dy, dz):
    # nearest-neighbor walks: independent +/- Poisson hop counts
    iy = np.floor(y/dy).astype(int)
    wy = y/dy-iy
    vy = (sy/dy)**2
    lateral = (1-wy)*ive(abs(iy), vy) + wy*ive(abs(iy+1), vy)

    # image index -j-1 reflects through the lower cell face
    zg = np.maximum(0, z/dz-0.5)
    hg = np.maximum(0, height/dz-0.5)
    iz, ih = np.floor(zg).astype(int), np.floor(hg).astype(int)
    wz, wh = zg-iz, hg-ih
    vz = (sz/dz)**2
    vertical = np.zeros_like(vz)
    for j, wj in [(iz, 1-wz), (iz+1, wz)]:
        for k, wk in [(ih, 1-wh), (ih+1, wh)]:
            vertical += wj*wk*(ive(abs(j-k), vz) + ive(j+k+1, vz))
    return lateral*vertical/(dy*dz)
