# skysurvey-skyfield
Skysurvey extension containing 3D density-velocity fields for accurate 3D-sky distribution

# Installation
using pip:
```bash
pip install skysurvey-skyfield
```

# Concept 
skysurvey-skyfield top level functions are expected to returns RA, Dec, zcosmo, vpec etc. that can be then be used in a skysurvey target model.

```python
import skysurvey
import skysurvey_skyfield

model_3d = {"radecz": {"func": func_returning___ra_dec_z_vpec,
                      #"kwargs": {}, # function's options
                       "as":["ra", "dec", "z", "vpec"] # stroring names
					   }
          }
snia = skysurvey.SNIa.from_draw(5_000, model=model_3d)
```


## Example

Draw RA, Dec, zcosmo and vpec, and then get "z" the observed redshift. 

```python
import skysurvey
import skysurvey_skyfield
import numpy as np

def get_random_3d(size, rate, 
                  zmin=0, zmax=1, zstep=1e-4, # redshift
                  skyarea=None, ra_range=[0, 360], dec_range=[-90, 90], # radec
                  vpec_prop = {"loc": 0, "scale":300},
                  **kwargs
                 ):
    """ randomly drawing ra, dec, zcosmo and vpec independently """
    from skysurvey.tools.utils import random_radec
    from skysurvey.target import rates
    
    # random draw in the sky
    ra, dec = random_radec(size=size, skyarea=skyarea, ra_range=ra_range, dec_range=dec_range)

    # redshift follow the rate
    zcosmo = rates.draw_redshift(size, rate, zmin=zmin, zmax=zmax, zstep=zstep, skyarea=skyarea, **kwargs)

    # random vpec
    vpec = np.random.normal(size=size, **vpec_prop)
    return ra, dec, zcosmo, vpec

def zcosmo_to_zobs(zcosmo, vpec):
    """ transform zcosmo into observed redshift given peculiar velocity """
    from astropy.constants import c
    return (1 + zcosmo) * (1+vpec/c.to("km/s").value) - 1

    
# build the model
model_3d = {"radecz": {"func": get_random_3d,
                      #"kwargs": {}, # function's options
                       "as":["ra", "dec", "zcosmo", "vpec"] # stroring names
					   },
            "z": {"func": zcosmo_to_zobs,
                 "kwargs": {"zcosmo":"@zcosmo", "vpec":"@vpec"},
                 }
          }

snia = skysurvey.SNeIa.from_draw(5_000, model=model_3d, zmax=0.1)
snia.data.head(5)
```
|    |     x1 |     c |      t0 |       ra |      dec |   zcosmo |     vpec |   magabs |         z |   magobs |          x0 | template   |
|---:|-------:|------:|--------:|---------:|---------:|---------:|---------:|---------:|----------:|---------:|------------:|:-----------|
|  0 | -0.235 | 0.093 | 56144.2 |  85.6558 | -17.7259 |  0.07105 | -376.761 | -19.1435 | 0.069704  |  18.4155 | 0.000683036 | salt2      |
|  1 |  0.6   | 0.141 | 56038   | 107.037  | -16.8615 |  0.08895 | -710.863 | -19.0464 | 0.0863679 |  19.0028 | 0.000397679 | salt2      |
|  2 |  0.37  | 0.064 | 56148.8 | 219.088  |  51.774  |  0.07595 |  284.344 | -19.062  | 0.0769705 |  18.7232 | 0.000514477 | salt2      |
|  3 |  0.4   | 0.081 | 56049.1 | 278.101  | -47.1459 |  0.08795 |  205.612 | -19.175  | 0.0886962 |  18.9354 | 0.000423146 | salt2      |
|  4 | -0.57  | 0.049 | 56071.4 | 186.988  |  28.0833 |  0.08375 |  341.405 | -19.0145 | 0.0849842 |  18.9976 | 0.000399589 | salt2      |
