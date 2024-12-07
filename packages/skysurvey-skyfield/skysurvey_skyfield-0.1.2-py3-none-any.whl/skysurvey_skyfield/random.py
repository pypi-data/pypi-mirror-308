import numpy as np
from skysurvey.tools.utils import random_radec
from skysurvey.target import rates


def get_random_3d(size, rate, 
                  zmin=0, zmax=1, zstep=1e-4, # redshift
                  skyarea=None, ra_range=[0, 360], dec_range=[-90, 90], # radec
                  vpec_prop = {"loc": 0, "scale":300},
                  **kwargs
                 ):
    """ dumb function calling ra, dec, z and vpec independently and returning them all at once. """    
    ra, dec = random_radec(size=size, skyarea=skyarea, ra_range=ra_range, dec_range=dec_range)
    zcosmo = rates.draw_redshift(size, rate, zmin=zmin, zmax=zmax, zstep=zstep, skyarea=skyarea, **kwargs)
    vpec = np.random.normal(size=size, **vpec_prop)
    return ra, dec, zcosmo, vpec
