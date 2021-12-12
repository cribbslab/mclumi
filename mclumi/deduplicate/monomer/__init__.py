# ## /*** block. remote ***/
from .Adjacency import *
from .Build_test import *
from .DedupBasic import *
from .DedupPos_test import *
from .DedupGene import *
from .DedupSC import *
from .Cluster import *
from .Directional import *
from .MarkovClustering import *


# ## /*** block. local ***/
# try:
#     from mclumi.deduplicate.monomer.Adjacency import *
#     from mclumi.deduplicate.monomer.Parse import *
#     from mclumi.deduplicate.monomer.DedupBasic import *
#     from mclumi.deduplicate.monomer.Cluster import *
#     from mclumi.deduplicate.monomer.Directional import *
#     from mclumi.deduplicate.monomer.MarkovClustering import *
# except ImportError:
#     pass