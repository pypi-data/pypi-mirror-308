import site
import sys
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

import setuptools
setuptools.setup()
