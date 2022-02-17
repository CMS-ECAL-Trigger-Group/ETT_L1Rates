import os 
direcs = [d_ for d_ in os.listdir("crab_projects")]
for d in direcs:
    print("===============================================================================")
    c = "crab status -d crab_projects/%s"%(d)
    print("$",c)
    os.system(c)
    print("===============================================================================")
