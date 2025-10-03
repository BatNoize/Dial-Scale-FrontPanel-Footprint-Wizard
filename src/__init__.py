try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from .Dial_Scale_FrontPanel_FootprintWizard import Dial_Scale_FrontPanel_FootprintWizard  # noqa ignore E501 line too long
    plugin = Dial_Scale_FrontPanel_FootprintWizard()
    plugin.register()
except Exception as e:
    import logging
    logger = logging.getLogger()
    logger.debug(repr(e))
