s_header="""<?xml version="1.0"?>
<!DOCTYPE xmimsim SYSTEM "http://www.xmi.UGent.be/xml/xmimsim-1.0.dtd">
<!--DO NOT MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING!-->
<xmimsim>
 <general version="1.0">
  <outputfile>{}.xmso</outputfile>
"""


s_main="""  <n_photons_interval>{n_photons_interval}</n_photons_interval>
  <n_photons_line>{n_photons_line}</n_photons_line>
  <n_interactions_trajectory>{n_interactions_trajectory}</n_interactions_trajectory>
  <comments/>
 </general>
 <composition>{layers}
  <reference_layer>{reference_layer}</reference_layer>
 </composition>
 <geometry>
  <d_sample_source>{d_sample_source}</d_sample_source>
  <n_sample_orientation>
   <x>{n_sample_orientation_x}</x>
   <y>{n_sample_orientation_y}</y>
   <z>{n_sample_orientation_z}</z>
  </n_sample_orientation>
  <p_detector_window>
   <x>{p_detector_window_x}</x>
   <y>{p_detector_window_y}</y>
   <z>{p_detector_window_z}</z>
  </p_detector_window>
  <n_detector_orientation>
   <x>{n_detector_orientation_x}</x>
   <y>{n_detector_orientation_y}</y>
   <z>{n_detector_orientation_z}</z>
  </n_detector_orientation>
  <area_detector>{area_detector}</area_detector>
  <collimator_height>{collimator_height}</collimator_height>
  <collimator_diameter>{collimator_diameter}</collimator_diameter>
  <d_source_slit>{d_source_slit}</d_source_slit>
  <slit_size>
   <slit_size_x>{slit_size_x}</slit_size_x>
   <slit_size_y>{slit_size_y}</slit_size_y>
  </slit_size>
 </geometry>
 <excitation>{excitation}
 </excitation>
 <absorbers>
  <excitation_path>{excitation_path}
  </excitation_path>
  <detector_path>{detector_path}
  </detector_path>
 </absorbers>
 <detector>
  <detector_type>{detector_type}</detector_type>
  <live_time>{detector_live_time}</live_time>
  <pulse_width>{detector_pulse_width}</pulse_width>
  <nchannels>{detector_nchannels}</nchannels>
  <gain>{detector_gain}</gain>
  <zero>{detector_zero}</zero>
  <fano>{detector_fano}</fano>
  <noise>{detector_noise}</noise>
  <crystal>{crystal}
  </crystal>
 </detector>
</xmimsim>
"""


s_source="""
  <discrete>
   <energy>{energy}</energy>
   <horizontal_intensity>{horizontal_intensity}</horizontal_intensity>
   <vertical_intensity>{vertical_intensity}</vertical_intensity>
   <sigma_x>{sigma_x}</sigma_x>
   <sigma_xp>{sigma_xp}</sigma_xp>
   <sigma_y>{sigma_y}</sigma_y>
   <sigma_yp>{sigma_yp}</sigma_yp>{other}
  </discrete>"""




s_layer="""
   <layer>{elements}
    <density>{density}</density>
    <thickness>{thickness}</thickness>
   </layer>"""
  
  
s_element="""
    <element>
     <atomic_number>{}</atomic_number>
     <weight_fraction>{}</weight_fraction>
    </element>"""


