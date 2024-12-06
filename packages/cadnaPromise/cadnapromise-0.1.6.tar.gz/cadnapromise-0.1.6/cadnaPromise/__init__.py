from .promise import Promise 
import os
import warnings

__version__ = '0.1.6'

curr_loc = os.path.dirname(os.path.realpath(__file__))

set_cadna_env = False

if not os.path.isfile(curr_loc+'/cadna/a.out'):
    if 'CADNA_PATH' in os.environ:
         set_cadna_env = False
    else:
        import logging
        logging.basicConfig()
        log = logging.getLogger(__file__)

        log.warning(f"\nHave not found CADNA path." 
                    f"\nPlease ensure CADNA is installed in this machine.")
        
else:
    set_cadna_env = True
    
if set_cadna_env:
    os.environ["CADNA_PATH"] = curr_loc+'/cadna/'

if 'CADNA_PATH' in os.environ:
    if not os.path.isfile(os.environ["CADNA_PATH"]+'/lib/flexfloat.a'):
        import subprocess
        if os.path.isfile(curr_loc+'/extra/libflexfloat.a'):
            subprocess.call('cp ' +curr_loc+'/extra/flexfloat.h ' +os.environ["CADNA_PATH"]+'/include', shell=True)
            subprocess.call('cp ' +curr_loc+'/extra/flexfloat.hpp ' +os.environ["CADNA_PATH"]+'/include', shell=True)
            subprocess.call('cp ' +curr_loc+'/extra/flexfloat_config.h ' +os.environ["CADNA_PATH"]+'/include', shell=True)
            subprocess.call('cp ' +curr_loc+'/extra/flexfloat_config.h.in ' +os.environ["CADNA_PATH"]+'/include', shell=True)
            subprocess.call('cp ' +curr_loc+'/extra/libflexfloat.a ' +os.environ["CADNA_PATH"]+'/lib', shell=True)
        else:
            subprocess.call('bash ' +curr_loc+'/extra/run_unix.sh', shell=True)
            subprocess.call('bash ' +curr_loc+'/extra/run_unix_copy.sh', shell=True)


cachePath = "/cache"
__compiler__ = 'g++'

if os.path.exists(curr_loc + cachePath):
    if os.path.isfile(curr_loc + cachePath + '/.CXX.txt'):
        with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
            __compiler__ = file.read()

