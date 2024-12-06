"""
LibSrd 1.0.5
==================
Sam Davis 

Commands
------------------
1. ```mergepdfs```  
Will merge all pdf's found in the current directory, and save the result at: ./Output/Output.pdf  
  
2. ```imgconvert [InitalFormat] [FinalFormat]```  
Will convert all images of ```InitalFormat``` in current directory to ```FinalFormat``` in ./Output/

"""

from libsrd.__version__ import __version__
from libsrd.table import Table
from libsrd.merge_pdf import merge_pdfs
from libsrd.image_convert import convert_images


def _script():
	print(__doc__.replace("```", ""))