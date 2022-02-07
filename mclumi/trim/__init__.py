# ## /*** block. remote ***/
from .Fixed import *
from .Filter import *
from .Reader import *
from .Template import *
from .BCRuleOut import *
from .SeqRuleOut import *
from .UMIRuleOut import *

# ## /*** block. local ***/
# try:
#     from mclumi.trim.Fixed import *
#     from mclumi.trim.Filter import *
#     from mclumi.trim.Reader import *
#     from mclumi.trim.SeqRuleOut import *
#     from mclumi.trim.Template import *
#     from mclumi.trim.UMIRuleOut import *
# except ImportError:
#     pass