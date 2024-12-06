
from astropy.constants import c
    
def zcosmo_to_zobs(zcosmo, vpec):
    """ transform zcosmo into observed redshift given peculiar velocity 

    Parameters
    ----------
    zcosmo: float, array
        cosmological redshift

    vpec: float, array
        perculiar line of sight velocity (in km/s)

    Returns
    -------
    zobs: float, array
        observed redshift.
    """
    return (1 + zcosmo) * (1+vpec/c.to("km/s").value) - 1
