"""
Copyright 2018 SuperDARN Canada, Univeristy Saskatchewan
Author(s): Marina Schmidt

Licensed under GNU v3.0

__init__.py
2018-11-05
Init file to setup the logging configuration and linking pyDARN's
module, classes, and functions.
"""
# KEEP THIS FILE AS MINIMAL AS POSSIBLE!

import os

# Importing pydarn exception classes
from .exceptions import dmap_exceptions
from .exceptions import superdarn_exceptions
from .exceptions import borealis_exceptions
from .exceptions import radar_exceptions
from .exceptions.warning_formatting import standard_warning_format
from .exceptions.warning_formatting import only_message_warning_format

# Importing pydarn pydmap data structure classes
from .dmap.datastructures import DmapScalar
from .dmap.datastructures import DmapArray
from .dmap import superdarn_formats

# importing utils
from .utils.conversions import dict2dmap
from .utils.conversions import dmap2dict

# Importing pydarn dmap classes
from .dmap.dmap import DmapRead
from .dmap.dmap import DmapWrite

# Importing pydarn superdarn classes
from .dmap.superdarn import SDarnRead
from .dmap.superdarn import SDarnWrite
from .dmap.superdarn import SDarnUtilities

# Importing pydarn borealis classes
from .borealis import borealis_formats
from .borealis.borealis import BorealisRead
from .borealis.borealis import BorealisWrite
from .borealis.borealis_convert import BorealisConvert
