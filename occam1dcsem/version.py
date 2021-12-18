from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('pyOccam1DCSEM').version
except DistributionNotFound:
    # package is not installed
    __version__ = '0.0.0'
