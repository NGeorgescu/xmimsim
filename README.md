

# XMIMSIM


XMIMSIM (the python package) is a front-end to XMI-MSIM, XRF open-source simulation software, for running in python.


## Installation

### MacOS
On mac, acquire XMIMSIM through [homebrew](http://brew.sh). To install do **not** use the brewsci/science tap

    brew tap tschoonj/tap
    brew cask install tschoonj/tap/xmi-msim

### Linux/Windows
Follow the instructions [here](https://github.com/tschoonj/xmimsim/wiki/Installation-instructions).


### Python

Install the python utility with

    pip install xmimsim

## Getting started

The examples folder contains the following example: 

    import xmimsim as xmi    

There is only one class currently in xmimsim, so one could just as easily use `from xmimsim import model`.

From there, the parameters can be defined as a dictionary:

    parameters = {'n_photons_interval' : 1,'n_photons_line' : 100000,'n_interactions_trajectory' : 1,
           'reference_layer' : 2,'d_sample_source' : 100,'area_detector' : 0.5,
           'collimator_height' : 0,'collimator_diameter' : 0,'d_source_slit' : 100,
           'slit_size_x' : 0.001,'slit_size_y' : 0.001,'detector_type' : 'SiLi',
           'detector_live_time' : 1500,'detector_pulse_width' : 1e-05,'detector_nchannels' : 2048,
           'detector_gain' : 0.0182138,'detector_zero' : 0,'detector_fano' : 0.12,'detector_noise' : 0.1}
    
to be injected into the code. The model is initialized with:
    
    xm = xmi.model()

from there the model, `xm`, can be added to, e.g.:

    xm.set_parameters(**parameters)
    xm.add_source(
        energy = 13.5,
        horizontal_intensity = '1e+012',
        vertical_intensity = '1e+009',
        gaussian=0.14)

All these classes return self, so one can actually do this all with one line, i.e. `xm.set_parameters(**parameters).add_source(....)`

The beampath layers are added: 

    xm.add_excitation_path_layer(atomic_numbers=[4], masses=[100], density=1.85, thickness=0.02)
    xm.add_detector_path_layer(atomic_numbers=[4], masses=[100], density=1.85, thickness=0.0025)
    xm.add_crystal_layer(atomic_numbers=[14], masses=[100], density=2.33, thickness=0.35)

Which behave like regular analyte layers:

    xm.add_layer(symbols=['N','O','Ar'],masses=[70,29,1],density=.00122,thickness=3)
    xm.add_layer(symbols=['As','Fe'],masses=[50,50],density=7.31,thickness=0.01)

Orientations are defined:

    xm.sample_orientation(rthetaphi=[1,270+65,0])
    xm.detector_orientation(rthetaphi=[1,135,0])
    xm.detector_window(xyz=[0,5.6,0])

The filename is defined for this, although this is not strictly necessary:

    xm.set_filename('xmsi_testfile')

And the calculation is run, discarding the massive xmso in favor of the csv file (default): 

    xm.calculate(M_lines=False, auger_cascade=True,radiative_cascade=False)

We can print out the number of photons from each of the following bands.

    print(xm.count_photons(**{'k_a_Fe':[6.098,6.744],'k_b_Fe':[6.7801,7.340],'k_a_As':[10.196,10.890],'k_b_As':[11.472,11.999]}))    

`xm.get_spectrum()` also returns a plottable spectrum from the xmi file.

If you simply copy the blocks of code together into one file and run it it should give you an output.

## Changelog

### 0.0.1

 - Initial Release

### 0.0.2

 - Fixed windows command, but it requires some changing of environment variables to make it run.
 - Fixed some header issues with the readme
 - Cleaned up example.py file

### 0.1.0

 - Fixing the windows problem broke *nix versions. Fixed.

### 0.1.1

 - Added default of no collimator or detector offset
 - Fixed a minor bug in the code (should not change any answers) with element arrays normalizations

## Contributing
Thanks to [Tom Schoonjans](https://github.com/tschoonj) for creating XMI-MSIM. Special thanks to the [vapory](https://github.com/Zulko/vapory) package, which some of the inspiration for this code comes from (also a python interface for a third-party utility).

Report problems to my gmail: nsgeorgescu

NGeorgescu : [https://github.com/NGeorgescu](https://github.com/NGeorgescu)

Github : [https://github.com/NGeorgescu/xmimsim.git](https://github.com/NGeorgescu/xmimsim.git)
