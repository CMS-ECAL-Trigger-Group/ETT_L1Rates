# Generate a new TP mode

Just put the wanted options in a text file similar to EcalTPGTPMode_Run2_default.txt and then use the `updateTPGTPMode.py` script to generate a new condDB tag.  

	cmsRun updateTPGTPMode.py inputTxtFile=EcalTPGTPMode_Run3_zeroing.txt TPModeTag=test outputDBFile=my_fancy_tag.db
  
The available TPmodes are described in these slides https://indico.cern.ch/event/995229/contributions/4189814/attachments/2173034/3669116/21_01_18%20-%20ECAL%20Trigger%20meeting%20-%20Emulator%20configuration.pdf
