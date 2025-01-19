"""Sample data science package."""
from importlib.metadata import version

try:
    __version__ = version("sampledata")
except:
    __version__ = "0.1.0.dev0"
