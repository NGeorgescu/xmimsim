import xmimsim as xmi

parameters = {'n_photons_interval' : 1,
   'n_photons_line' : 100000,
   'n_interactions_trajectory' : 1,
   'reference_layer' : 2,
   'd_sample_source' : 100,
   'area_detector' : 0.5,
   'collimator_height' : 0,
   'collimator_diameter' : 0,
   'd_source_slit' : 100,
   'slit_size_x' : 0.001,
   'slit_size_y' : 0.001,
   'detector_type' : 'SiLi',
   'detector_live_time' : 1500,
   'detector_pulse_width' : 1e-05,
   'detector_nchannels' : 2048,
   'detector_gain' : 0.0182138,
   'detector_zero' : 0,
   'detector_fano' : 0.12,
   'detector_noise' : 0.1}


xm = xmi.model()
xm.set_parameters(**parameters)
xm.add_source(
    energy = 13.5,
    horizontal_intensity = '1e+012',
    vertical_intensity = '1e+009',
    gaussian=0.14)
xm.add_excitation_path_layer(atomic_numbers=[4], masses=[100], density=1.85, thickness=0.02)
xm.add_detector_path_layer(atomic_numbers=[4], masses=[100], density=1.85, thickness=0.0025)
xm.add_crystal_layer(atomic_numbers=[14], masses=[100], density=2.33, thickness=0.35)
xm.sample_orientation(rthetaphi=[1,270+65,0])
xm.detector_orientation(rthetaphi=[1,135,0])
xm.detector_window(xyz=[0,5.6,0])
xm.add_layer(symbols=['N','O','Ar'],masses=[70,29,1],density=.00122,thickness=3)
xm.add_layer(symbols=['As','Fe'],masses=[50,50],density=7.31,thickness=0.01)
xm.set_filename('xmsi_testfile3')
xm.calculate(export='csv-file', save_xmso=True, M_lines=False, auger_cascade=True,radiative_cascade=False)
print(xm.count_photons(**{'k_a_Fe':[6.098,6.744],'k_b_Fe':[6.7801,7.340],'k_a_As':[10.196,10.890],'k_b_As':[11.472,11.999]}))


