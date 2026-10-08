from .base import registry
from .radar import RadarAdapter
from .rf import RFAdapter
from .eoir import EOIRAdapter
from .acoustic import AcousticAdapter

registry.register(RadarAdapter())
registry.register(RFAdapter())
registry.register(EOIRAdapter())
registry.register(AcousticAdapter())

__all__ = ["registry"]
