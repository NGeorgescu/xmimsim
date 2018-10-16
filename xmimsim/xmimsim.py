import subprocess, hashlib, os, re
from .strings import s_main, s_layer, s_element, s_source, s_header
from .func import XMIMSIM_BINARY, get_elements, xyz_update


class model():
    """xm = xmi.model()"""
    def __init__(self):
        self.parameters = {'collimator_height' : 0, 'collimator_diameter' : 0, 'detector_zero' : 0}
        self.layers = []
        self.sources = []
        self.excitation_path = []
        self.detector_path = []
        self.crystal = []
        
    def set_parameters(self,**kwargs): 
        """
        Usage
        ------------
        define parameters with xmimsim.model.set_parameters(param=val, ...)
         or alternatively xmimsim.model.set_parameters(**{'param':'val',...})
         see example file
        
        Direct Definitions
        ------------
        you will need to define all of the following:
         n_photons_interval, n_photons_line, n_interactions_trajectory, reference_layer, 
         d_sample_source, area_detector, collimator_height, collimator_diameter, 
         d_source_slit, slit_size_x, slit_size_y, detector_type, detector_live_time, detector_pulse_width, 
         detector_nchannels, detector_gain, detector_zero, detector_fano, detector_noise
        all distances specified in cm.
        
        Defaults
        ------------
        The defaults are:
         - 'collimator_height' = 0
         - 'collimator_diameter' = 0
         - 'detector_zero' : 0}
        
        Orientation Definitions
        ------------
        You may directly define the following with set_parameters but the respective
        interfaces are MUCH nicer.  See e.g. xmimsim.model.sample_orientation() for more info
         n_sample_orientation_x, n_sample_orientation_y, n_sample_orientation_z, 
         p_detector_window_x, p_detector_window_y, p_detector_window_z, 
         n_detector_orientation_x, n_detector_orientation_y, n_detector_orientation_z,
        
        Layers and Sources
        ------------
        added via:
            xmimsim.model.add_layer()
            xmimsim.model.add_excitation_path_layer()
            xmimsim.model.add_detector_path_layer()
            xmimsim.model.add_crystal_layer()
            xmimsim.model.add_source()
        
        """
        self.parameters.update(kwargs)
        return self
       
    def add_layer(self,*args, **kwargs): 
        """
        Add a layer to the simulation starting with the topmost        
        All three of the following must be contained or the model
        will fail to build: 'elements', 'thickness', and 'density'

        Components
        ---------------
        density and thickness are added rather straightforwardly:
          add_layer(..., density=value, thickness=value)
        Adding elements requires some specification of the following:

        Elements
        ---------------
        Elements can be added using the following keywords:
         elements: this is a straightforward dictionary of {atomic number:mass} values
         atomic_numbers: accepts atomic number as input
         symbols: accepts symbol as input 
         masses: input the masses (all masses are normalized to 100%)
        
        e.g. for atmospheric air, one would write any one of the following:
         add_layer(elements={7:70,8:29,18:1}, ...)
         add_layer(symbols=['N','O','Ar'],masses=[70,29,1], ...)
         add_layer([70,29,1],atomic_numbers=[7,8,18], ...)"""         
        self.layers.append(get_elements(args,kwargs))
        return self

    def add_excitation_path_layer(self,*args, **kwargs):
        """
        Add a layer to the simulation starting with the topmost        
        All three of the following must be contained or the model
        will fail to build: 'elements', 'thickness', and 'density'

        Components
        ---------------
        density and thickness are added rather straightforwardly:
          add_layer(..., density=value, thickness=value)
        Adding elements requires some specification of the following:

        Elements
        ---------------
        Elements can be added using the following keywords:
         elements: this is a straightforward dictionary of {atomic number:mass} values
         atomic_numbers: accepts atomic number as input
         symbols: accepts symbol as input 
         masses: input the masses (all masses are normalized to 100%)
        
        e.g. for atmospheric air, one would write any one of the following:
         add_layer(elements={7:70,8:29,18:1}, ...)
         add_layer(symbols=['N','O','Ar'],masses=[70,29,1], ...)
         add_layer([70,29,1],atomic_numbers=[7,8,18], ...)""" 
        self.excitation_path.append(get_elements(args,kwargs))
        return self

    def add_detector_path_layer(self,*args, **kwargs):
        """
        Add a layer to the simulation starting with the topmost        
        All three of the following must be contained or the model
        will fail to build: 'elements', 'thickness', and 'density'

        Components
        ---------------
        density and thickness are added rather straightforwardly:
          add_layer(..., density=value, thickness=value)
        Adding elements requires some specification of the following:

        Elements
        ---------------
        Elements can be added using the following keywords:
         elements: this is a straightforward dictionary of {atomic number:mass} values
         atomic_numbers: accepts atomic number as input
         symbols: accepts symbol as input 
         masses: input the masses (all masses are normalized to 100%)
        
        e.g. for atmospheric air, one would write any one of the following:
         add_layer(elements={7:70,8:29,18:1}, ...)
         add_layer(symbols=['N','O','Ar'],masses=[70,29,1], ...)
         add_layer([70,29,1],atomic_numbers=[7,8,18], ...)""" 
        self.detector_path.append(get_elements(args,kwargs))
        return self
        
    def add_crystal_layer(self,*args, **kwargs):
        """
        Add a layer to the simulation starting with the topmost        
        All three of the following must be contained or the model
        will fail to build: 'elements', 'thickness', and 'density'

        Components
        ---------------
        density and thickness are added rather straightforwardly:
          add_layer(..., density=value, thickness=value)
        Adding elements requires some specification of the following:

        Elements
        ---------------
        Elements can be added using the following keywords:
         elements: this is a straightforward dictionary of {atomic number:mass} values
         atomic_numbers: accepts atomic number as input
         symbols: accepts symbol as input 
         masses: input the masses (all masses are normalized to 100%)
        
        e.g. for atmospheric air, one would write any one of the following:
         add_layer(elements={7:70,8:29,18:1}, ...)
         add_layer(symbols=['N','O','Ar'],masses=[70,29,1], ...)
         add_layer([70,29,1],atomic_numbers=[7,8,18], ...)""" 
        self.crystal.append(get_elements(args,kwargs))
        return self
    
    def add_source(self, **kwargs): 
        """
        You can add multiple sources with this module.
        
        Example
        -------------
        a typical source might look like
        xm.add_source(energy = 13.5, horizontal_intensity = '1e+012', vertical_intensity = '1e+009',gaussian = 0.14)

        Omitted values
        -------------
        if you omit sigma_x, sigma_y, sigma_xp, or sigma_yp, they default to 0

        """                
        self.sources.append(kwargs)
        # sigma zero by default
        return self

    def sample_orientation(self,**kwargs):
        """
        Orientations/Positions
        -------------
        you need to defined the detector orientation and the detector window position
        as well as the sample orientation (sample position is set by d_source_sample
        within xmimsim.model.set_parameters()))
         
        They can be set with the following:
        
        xyz=[X, Y, Z]
        -------------
        The position/orientation is set with sample_orientation(xyz=[x,y,z]), 
        wherein + and -x is up and down, +y is in the direction of the source, 
        and +/- z is left to right.  Unless you've tilted your sample at an oblique 
        angle, x probably will remain at zero. For a picture, see the user guide at 
        https://github.com/tschoonj/xmimsim/wiki/User-guide or look at the assistant
        within the program itself
        
        rthetaphi=[R, theta, phi (in degrees)]
        -------------
        the position can be set with sample_orientation(rthetaphi=[r,theta,phi]),         
        wherein r is the vector length (for orientations, keep this at 1), and
        theta represents turning left and right in the YZ plane. If your eyeballs
        are the source, then your right points to theta = 0, you are looking at 
        theta = 90, and your left is theta = 270.  If you look up that's + phi 
        and if you look down that's -phi
        
        you can run xmimsim.rtp([r,theta,phi]) to see what [r,theta,phi] gives you
        a desired x, y, z
        
        """
        xyz_update(self.parameters,'n_sample_orientation',kwargs)
        return self

    def detector_orientation(self,**kwargs):
        """
        Orientations/Positions
        -------------
        you need to defined the detector orientation and the detector window position
        as well as the sample orientation (sample position is set by d_source_sample
        within xmimsim.model.set_parameters()))
         
        They can be set with the following:
        
        xyz=[X, Y, Z]
        -------------
        The position/orientation is set with sample_orientation(xyz=[x,y,z]), 
        wherein + and -x is up and down, +y is in the direction of the source, 
        and +/- z is left to right.  Unless you've tilted your sample at an oblique 
        angle, x probably will remain at zero. For a picture, see the user guide at 
        https://github.com/tschoonj/xmimsim/wiki/User-guide or look at the assistant
        within the program itself
        
        rthetaphi=[R, theta, phi (in degrees)]
        -------------
        the position can be set with sample_orientation(rthetaphi=[r,theta,phi]),         
        wherein r is the vector length (for orientations, keep this at 1), and
        theta represents turning left and right in the YZ plane. If your eyeballs
        are the source, then your right points to theta = 0, you are looking at 
        theta = 90, and your left is theta = 270.  If you look up that's + phi 
        and if you look down that's -phi
        
        you can run xmimsim.rtp([r,theta,phi]) to see what [r,theta,phi] gives you
        a desired x, y, z
        
        """
        xyz_update(self.parameters,'n_detector_orientation',kwargs)
        return self

    def detector_window(self,**kwargs):
        """
        Orientations/Positions
        -------------
        you need to defined the detector orientation and the detector window position
        as well as the sample orientation (sample position is set by d_source_sample
        within xmimsim.model.set_parameters()))
         
        They can be set with the following:
        
        xyz=[X, Y, Z]
        -------------
        The position/orientation is set with sample_orientation(xyz=[x,y,z]), 
        wherein + and -x is up and down, +y is in the direction of the source, 
        and +/- z is left to right.  Unless you've tilted your sample at an oblique 
        angle, x probably will remain at zero. For a picture, see the user guide at 
        https://github.com/tschoonj/xmimsim/wiki/User-guide or look at the assistant
        within the program itself
        
        rthetaphi=[R, theta, phi (in degrees)]
        -------------
        the position can be set with sample_orientation(rthetaphi=[r,theta,phi]),         
        wherein r is the vector length (for orientations, keep this at 1), and
        theta represents turning left and right in the YZ plane. If your eyeballs
        are the source, then your right points to theta = 0, you are looking at 
        theta = 90, and your left is theta = 270.  If you look up that's + phi 
        and if you look down that's -phi
        
        you can run xmimsim.rtp([r,theta,phi]) to see what [r,theta,phi] gives you
        a desired x, y, z
        
        """
        xyz_update(self.parameters,'p_detector_window',kwargs)
        return self

    def remove_all_sources(self):
        self.sources=[]
        return self

    def remove_all_layers(self):
        self.layers
        return self

    def remove_all_excitation_path(self):
        self.excitation_path = []
        return self

    def remove_all_detector_path(self):
        self.detector_path = []
        return self
        
    def remove_all_crystal(self):
        self.crystal = []
        return self    

    def set_filename(self,name):
        """
        You may set a filename with xmimsim.model.set_filename()
         n.b.: force_overwrite when it comes time to calculate will look for
         the same file name, not file parameters.  Hence, if you pick two files
         with the same name, you will overwrite the second file with the first
        
        If you don't set a filename then the default filename assigned at
        calculation is an sha224 hash of the parameters. This doesn't help you
        find that csv file you're looking for easily, BUT it will keep you from
        overwriting your data.
        """
        self.filename = name
        return self

    def remove_filename(self):
        try:
            del self.filename
        except:
            print('no filename defined')
        return self        

    def full_parameters(self):
        def parameterupdate(parameters,layer_str,layers):
            layers_string = ''
            for layer in layers:
                layer['elements'] = ''.join([s_element.format(atom,weight) for atom,weight in layer['elements'].items()])
                layers_string += s_layer.format(**layer)
            parameters.update({layer_str:layers_string})
        parameterupdate(self.parameters,'layers',self.layers)
        parameterupdate(self.parameters,'excitation_path',self.excitation_path)
        parameterupdate(self.parameters,'detector_path',self.detector_path)
        parameterupdate(self.parameters,'crystal',self.crystal)
        sourcestring = ''
        for sourceupdate in self.sources:
            source = {'sigma_x':0,'sigma_y':0,'sigma_xp':0,'sigma_yp':0}
            other_string=''
            if 'gaussian' in source:
                string='\n      <scale_parameter distribution_type="gaussian">{}</scale_parameter>'    
                other_string += string.format(source['gaussian'])
            source.update({'other':other_string})
            source.update(sourceupdate)
            sourcestring += s_source.format(**source)
        self.parameters.update({'excitation':sourcestring})
        return self
    
    def generate_base_xmsi(self,**kwargs):        
        self.full_parameters()
        self.base_xmsi = s_main.format(**self.parameters)
        return self.base_xmsi

    def calculate(self, xmifolder='xmi' , save_xmsi=True, save_xmso=False , export='csv-file',
                  force_overwrite = False, M_lines=True, auger_cascade=True, 
                  radiative_cascade=True, variance_reduction=True, pile_up=False, 
                  escape_peaks=True, poisson=False, opencl=False, 
                  advanced_compton=False, default_seeds=False, set_threads='max',**kwargs):
        """
        Calculation Options
        ------------
        This part actually does the calculating.  There are a lot of options:
        
        
        I/O Functions
        ------------
        xmifolder= 'string' (or None)
         will save your data to a folder xmi subfolder rather than cluttering cwd

        save_xmsi = Bool
         hold on to the .xmsi file after calculation

        save_xmso = Bool
         hold on to the .xmso file after calculation.  Obviously if you choose this
         you will want to use the export command below
         
        force_overwrite = Bool
         -if True, then it will run the calculation no matter what
         -if False, it will check for the export (if you set an export) or the .xmso
         first, if it encounters one of them it does not run the calculation. Use
         xmso2csv for csv conversion, for example, rather than running again.
         
        export = 'string'
         - will export the file for you at the end of calculation.  
         - Probably also a good idea to use save_xmso=False; xmso files are huge
         - possible options are 'spe-file', 'csv-file', 'svg-file' or 'htm-file'
         - add '-unconvoluted' to save w/o detector conv. e.g. export = 'csv-file-unconvoluted'

        Physics
        ------------
        The following options will change your answer:
         - M_lines=False:  Disable M lines
         - auger_cascade=False: Disable Auger (non radiative) cascade effects
         - radiative_cascade=False:  Disable radiative cascade effects
         - variance_reduction=False: Disable variance reduction
         - pile_up=True: Enable pile-up
         - escape_peaks=False: Enable escape peaks
         - poisson=True: Generate Poisson noise in the spectra
        
        Computation
        -------------
        Will change how the calculation is performed
         - opencl=True: Enable OpenCL
         - advanced-compton=True: Enable advanced yet slower Compton simulation
         - set-threads=NTHREADS: Sets the number of threads to NTHREADS (default=max)
         - default-seeds=True: Use default seeds for reproducible simulation results

            
        """
        #find folder and make it if it doesn't exist
        if xmifolder!=None:
            xmipath = os.path.join(os.getcwd(),xmifolder)
        else:
            xmipath = os.getcwd()
        if not os.path.exists(xmipath):
            os.mkdir(xmipath)
        #make the full file
        #make base_xmsi if that hasn't been done yet
        try: self.base_xmsi
        except: self.generate_base_xmsi()
        #set the filename
        try: self.filename
        except:
            base_string=self.base_xmsi.encode()
            #add these tags to the sha to avoid using files made under different assumptions
            if not M_lines:             base_string += ' --disable-M-lines'
            if not auger_cascade:       base_string += ' --disable-auger-cascade'
            if not radiative_cascade:   base_string += ' --disable-radiative-cascade'
            if not variance_reduction:  base_string += ' --disable-variance-reduction'
            if pile_up:                 base_string += ' --enable-pile-up'
            if not escape_peaks:        base_string += ' --disable-escape-peaks'
            if poisson:                 base_string += ' --enable-poisson'
            self.filename=hashlib.sha224(base_string).hexdigest()
        filename = os.path.join(xmipath,self.filename)
        self.full_xmsi=s_header.format(filename)+self.base_xmsi
        self.filelocation = filename    
            
        cmd = [XMIMSIM_BINARY, filename+'.xmsi']
        if M_lines==False:              cmd.append('--disable-M-lines')
        if auger_cascade==False:        cmd.append('--disable-auger-cascade')
        if radiative_cascade==False:    cmd.append('--disable-radiative-cascade')
        if variance_reduction==False:   cmd.append('--disable-variance-reduction')
        if pile_up==True:               cmd.append('--enable-pile-up')
        if escape_peaks==False:         cmd.append('--disable-escape-peaks')
        if poisson==True:               cmd.append('--enable-poisson')
        if opencl==True:                cmd.append('--enable-opencl')
        if advanced_compton==True:      cmd.append('--enable-advanced-compton')
        if default_seeds==True:         cmd.append('--enable-default-seeds')
        if not set_threads=='max':      cmd.append('--set-threads=%'%set_threads)
        
        output_file_exists=os.path.isfile(filename+'.xmso')
        if not export==None:
            exportformat = re.findall(r'\w+',export)[0]
            cmd.append('--{}'.format(export))
            cmd.append('{}.{}'.format(filename,exportformat))
            output_file_exists=any([output_file_exists,os.path.isfile(filename+'.'+exportformat)])
        with open(filename+'.xmsi', 'w+') as f:
            try:
                f.write(self.full_xmsi)
            except:
                f.write(self.generate_xmsi())

        if any([force_overwrite,not output_file_exists]):
            try:
                process = subprocess.Popen(cmd, shell=(True if os.name=='nt' else False),
                                           stderr=subprocess.PIPE,
                                           stdout=subprocess.PIPE)        
                stdout, stderr = process.communicate()
                if len(stdout)>0: print(stdout)
                if len(stderr)>0: print(stderr)
            except:
                if os.name=='nt':
                    print('Error: XMI-MSIM simulation software could not be located by your machine.',
                    '',  
                    'If you installed XMI-MSIM (the software, not this python package),', 
                    'You must insert xmimsim-cli.exe into the enviroment variable path.', 
                    'Go to My computer (right click) -> properties -> advanced -> advanced',
                    '-> environment variables... -> Path and edit path by adding xmimsim-cli.exe',
                    'directory into path (probably the path is something like',
                    '"C:/Program Files/XMI-MSIM 64-bit/Bin/xmimsim-cli.exe" ',
                    'but you will have to use "browse" to look for it at the exact location.',
                    '',
                    'Otherwise it will not be able to run on windows.',sep='\n')
                else:
                     print('Error:XMI-MSIM command not found (try running xmimsim --help from the command line)')
            else:                        
                #cleanup
                if not save_xmsi:
                    os.remove(filename+'.xmsi')
                if not save_xmso:
                    os.remove(filename+'.xmso')
     
                
    def get_spectrum(self):
        """
        gets the spectrum and returns it for an arbitrary calculation
        
        
        """
        try:
            file = self.filelocation + '.csv'
            with open(file,'r') as filedata:                       
                self.spectrum = [[float(j) for j in re.findall(r'(?<=\,)[^\,]+',line)] for line in filedata.readlines()]
        except:
            try: 
                file = self.filelocation + '.xmso'
            except: return None
            else:
                tag = 'spectrum_conv' #use spectrum_unconv for a spectrum that does not have the detector convolution (not recommended)
                try:
                    with open(file,'r') as filedata:                       
                        xml_output_spectrum = filedata.read().split('<'+tag+'>')[1].split('</'+tag+'>')[0] #cuts the interesting part out
                    spec_x = re.compile(r'(?<=\<energy\>)[\d\.e\-\+]+').findall(xml_output_spectrum) #looking for x data
                    spec_y = re.compile(r'(?<=\<counts interaction_number\=\"\d\"\>)[\d\.e\-\+]+').findall(xml_output_spectrum) #looking for y data
                    spec_x, spec_y = [[float (j) for j in i] for i in [spec_x,spec_y]]
                    self.spectrum = zip(spec_x,spec_y)
                except:
                    print("critical error in data analysis: spectrum not found") #not good if the x and y are different lengths, that means something is wrong with the last 4 lines of code above
        return self.spectrum

    def count_photons(self,*args,**kwargs):
        """
        Returns the count of photons between two values from a calculation, either
        csv or xmso. If it cannot find the calculation results, returns None                
        
        Usage
        -------------
        xmimsim.model.countphotons(val1,val2) returns a number of photons calculated
        from val1 to val2
        
        xmimsim.model.countphotons(**{'item':[val1,val2], ...}) returns the dictionary:
        {'item':n_photons, ...}        
        
        runs by default on unconvoluted spectra
        
        Warning
        -------------
        Requires running .calculate() first, however, if force_overwrite = False and you
        have output data in the export of your choice, then this will take no time as the
        output file will be detected.

        """
        try:
            self.spectrum
        except:
            self.get_spectrum()
        if len([*args])>0:
            span=[*args]
            counts = sum([int(y) for [x,y] in self.spectrum if min(span) <= x <= max(span)])
            return counts
        else:
            output_dict = {}
            for name,span in kwargs.items():
                counts = sum([int(y) for [x,y] in self.spectrum if min(span) <= x <= max(span)])
                output_dict.update({name:counts})
            return output_dict                                
        
        
        
            
        
  
