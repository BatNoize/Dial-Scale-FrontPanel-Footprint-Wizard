try:
    from .Dial_Scale_FrontPanel_FootprintWizard import Dial_Scale_FrontPanel_FootprintWizard
    plugin = Dial_Scale_FrontPanel_FootprintWizard()
    plugin.register()
except Exception as e:
    import logging
    logger = logging.getLogger()
    logger.debug(repr(e))
