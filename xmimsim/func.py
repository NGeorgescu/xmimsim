import os
from math import sin, cos, pi


XMIMSIM_BINARY = ("xmimsim-cli.exe" if os.name=='nt' else "xmimsim")

def rtp(input_list):
    r,theta,phi = input_list
    theta = theta*pi/180
    phi = phi*pi/180
    x = round(r*sin(phi),7)
    y = round(r*cos(phi)*cos(theta),7)
    z = round(r*cos(phi)*sin(theta),7)
    return [x,y,z]



def xyz_update(parameters,string,kwargs):
    if 'rthetaphi' in kwargs:
        kwargs['xyz']=rtp(kwargs['rthetaphi'])    
    for n,d in enumerate(['x','y','z']):
        sub_string = string + "_" + d
        parameters.update({sub_string:kwargs['xyz'][n]})


    

atomic_n={'H':1,'He':2,'Li':3,'Be':4,'B':5,'C':6,'N':7,'O':8,'F':9,'Ne':10,
          'Na':11,'Mg':12,'Al':13,'Si':14,'P':15,'S':16,'Cl':17,'Ar':18,'K':19,
          'Ca':20,'Sc':21,'Ti':22,'V':23,'Cr':24,'Mn':25,'Fe':26,'Co':27,
          'Ni':28,'Cu':29,'Zn':30,'Ga':31,'Ge':32,'As':33,'Se':34,'Br':35,
          'Kr':36,'Rb':37,'Sr':38,'Y':39,'Zr':40,'Nb':41,'Mo':42,'Tc':43,
          'Ru':44,'Rh':45,'Pd':46,'Ag':47,'Cd':48,'In':49,'Sn':50,'Sb':51,
          'Te':52,'I':53,'Xe':54,'Cs':55,'Ba':56,'La':57,'Ce':58,'Pr':59,
          'Nd':60,'Pm':61,'Sm':62,'Eu':63,'Gd':64,'Tb':65,'Dy':66,'Ho':67,
          'Er':68,'Tm':69,'Yb':70,'Lu':71,'Hf':72,'Ta':73,'W':74,'Re':75,
          'Os':76,'Ir':77,'Pt':78,'Au':79,'Hg':80,'Tl':81,'Pb':82,'Bi':83,
          'Po':84,'At':85,'Rn':86,'Fr':87,'Ra':88,'Ac':89,'Th':90,'Pa':91,
          'U':92,'Np':93,'Pu':94,'Am':95,'Cm':96,'Bk':97,'Cf':98,'Es':99,
          'Fm':100,'Md':101,'No':102,'Lr':103,'Rf':104,'Db':105,'Sg':106,
          'Bh':107,'Hs':108,'Mt':109,'Ds':110,'Rg':111,'Cn':112,'Nh':113,
          'Fl':114,'Mc':115,'Lv':116,'Ts':117,'Og':118}



def get_elements(args,kwargs):
    try:
        element_numbers = list(kwargs['elements'])
        element_masses = [kwargs['elements'][element] for element in element_numbers]        
    except:
        try: element_masses=kwargs['masses']
        except: element_masses=args
        finally:
            if len(element_masses) == 0:
                raise Exception('element masses are empty: did you use the right keywords?')    
        try: element_numbers = kwargs['atomic_numbers']
        except: element_numbers = [atomic_n[sym] for sym in kwargs['symbols']]
    try:element_numbers = [atomic_n[sym] for sym in element_numbers]        
    except:pass
    element_masses=[100*(e/(sum(element_masses))) for e in element_masses]
    elementdict = {k:v for [k,v] in zip(element_numbers,element_masses)}
    kwargs.update({'elements':elementdict})
    return kwargs # {'element':{7:70,8:29,18:1},'density':val,'thickness':val}



    

