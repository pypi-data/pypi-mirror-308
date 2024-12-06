import numpy as np
from astropy.cosmology import Planck18

from ..tools.utils import surface_of_skyarea

def draw_redshift(size, rate, zmin=0., zmax=2., zstep=1e-4, skyarea=None, **kwargs):
    """ random redshift draw following the given rate

    Parameters
    ----------
    size: int
        number of target to draw
    
    rate: func, float
        func: a function that takes as input an array or redshift "z"
        float: number of targets per Gpc3
        If float, get_volumetric_rate() is used.

    zmin, zmax: float
        redshift limits

    zstep: flaot
        sampling of the redshift.

    skyarea: None, str, float, geometry
        sky area (in deg**2).
        - None or 'full': 4pi
        - "extra-galactic": 4pi - (milky-way b<5)
        - float: area in deg**2
        - geometry: shapely.geometry.area is used (assumed in deg**2)

    kwargs goes to get_redshift_pdf() -> get_rate()

    Returns
    -------
    list
    """
    xx = np.arange(zmin, zmax, zstep)
    pdf = get_redshift_pdf(xx, rate=rate, **kwargs)
    return np.random.choice(np.mean([xx[1:],xx[:-1]], axis=0),
                            size=size, p=pdf/pdf.sum())

def get_rate(z, rate, skyarea=None, **kwargs):
    """ get the rate as a function of redshift

    z: array
        array of redshifts. 

    rate: float or func
        func: a function that takes as input an array or redshift "z"
        float: number of targets per Gpc3
        If float, get_volumetric_rate() is used.

    skyarea: None, str, float, geometry
        sky area (in deg**2).
        - None or 'full': 4pi
        - "extra-galactic": 4pi - (milky-way b<5)
        - float: area in deg**2
        - geometry: shapely.geometry.area is used (assumed in deg**2)

    **kwargs rate options.
        if rate is a float, these are that of get_volumetric_rate.
        (cosmology=Planck18, skyarea=None)
    """
    # specified rate function or volumetric rate ?
    if callable(rate): # function
        target_rate = rate(z, **kwargs)
    else: # volumetric
        target_rate = get_volumetric_rate(z, n_per_gpc3=rate, **kwargs)

    skyarea = surface_of_skyarea(skyarea) # in deg**2 or None
    if skyarea is not None:
        full_sky = 4*np.pi * (180/np.pi)**2 # 4pi in deg**2
        target_rate *= (skyarea/full_sky)

    return target_rate

def get_redshift_pdf(z, rate, skyarea=None, **kwargs):
    """ get the redshift pdf given the rate (function or volumetric)
    
    z: array
        array of redshifts. 

    rate: float or func
        func: a function that takes as input an array or redshift "z"
        float: number of targets per Gpc3
        If float, get_volumetric_rate() is used.

    skyarea: None, str, float, geometry
        sky area (in deg**2).
        - None or 'full': 4pi
        - "extra-galactic": 4pi - (milky-way b<5)
        - float: area in deg**2
        - geometry: shapely.geometry.area is used (assumed in deg**2)

    **kwargs rate options.
        if rate is a float, these are that of get_volumetric_rate.
        (cosmology=Planck18)

    Returns
    -------
    array
    """
    target_rate = get_rate(z, rate, skyarea=skyarea, **kwargs)
    
    rates = np.diff(target_rate)
    return rates/np.nansum(rates)

def get_volumetric_rate(z, n_per_gpc3, cosmology=Planck18):
    """ number of target (per year) up to the given redshift

    Parameters
    ----------
    z: float
        redshift

    n_per_gpc3: float
        number of targets per Gpc3
    
    cosmology: astropy.Cosmology
        cosmology used to get the comiving_volume
    Returns
    -------
    float
    """
    volume = cosmology.comoving_volume(z).to("Gpc**3").value
    z_rate = volume * n_per_gpc3
    return z_rate
