from .common import *

from .dockerenv import *

INSTALLED_APPS += ["taiga_contrib_slack"]

# THROTTLING
#REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
#    "anon": "20/min",
#    "user": "200/min",
#    "import-mode": "20/sec"
#}
