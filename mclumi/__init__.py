__all__ = [
    'align',
    'deduplicate',
    'fastq',
    'network',
    'trim',
    'util',
]

from .deduplicate import *
from .align import *
from .fastq import *
from .network import *
from .trim import *
from .util import *
from .Main import *
from .Path import *

# ## /*** block. local ***/
# try:
#     from mclumi.deduplicate import *
#     from mclumi.align import *
#     from mclumi.fastq import *
#     from mclumi.network import *
#     from mclumi.trim import *
#     from mclumi.util import *
#     from mclumi.Main import *
#     from mclumi.Path import *
# except ImportError:
#     pass