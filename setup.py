# This will try to import setuptools. If not here, it will reach for the embedded
# ez_setup (or the ez_setup package). If none, it fails with a message
try:
    from setuptools import setup
except ImportError:
    try:
        import ez_setup
        ez_setup.use_setuptools()
    except ImportError:
        raise ImportError("Xmimsim could not be installed, probably because"
            " neither setuptools nor ez_setup are installed on this computer."
            "\nInstall ez_setup ([sudo] pip install ez_setup) and try again.")

from setuptools import setup, find_packages

exec(open('xmimsim/version.py').read()) # loads __version__

setup(name='xmimsim',
      version=__version__,
      author='NGeorgescu',
    description='Toolkit for making and processing X-ray fluoresence simulations via XMI-MSIM',
    long_description=open('README.md').read(),
    license='see LICENSE.txt',
    keywords="xmimsim xmi msim xrf fluorescence x-ray xray simulation",
    packages= find_packages(exclude='docs'))
