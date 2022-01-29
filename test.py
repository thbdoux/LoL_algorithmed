import numpy as np
import scipy.stats

## récupération des données WIN / LOOSE dans un tableau de contingence

observed = [[70,39],
            [50,50],
            [69,69],
            [40,40],
            [150,150]]

            ## tableau contingence 5 * 2 
result = scipy.stats.chi2_contingency(np.array(observed))

print(result)
