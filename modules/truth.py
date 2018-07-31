# This module reads the input file, and saves all of the information into a dictionary for the other scripts to use.

# ------------------- Read in the Input File -------------------

# format is: [experiment configuration] [distance in kpc] [1n] [2n] [1n] [2n] ..... [1n] [2n]
# example:    halo1 5 72 48 40 12 16 0

def truth(inputfile):
	fi = open(inputfile,'r')

	Truth = {}
	for line in fi:
		line = line.strip()
		line = line.split()
		# get the experiment configuration
		exptconfig = '{0}_{1}kpc'.format(line[0],line[1])
		line.remove(line[0]) # remove configuration name
		line.remove(line[0]) # remove distance
		# get the different truth values
		truth_set = []
		for i in range(0,len(line)//2):
			truth_set.append([int(line[i*2]),int(line[i*2+1])])
		Truth["{0}".format(exptconfig)] = truth_set
	fi.close()
	return Truth


# now Truth holds the different truth values for each experiment configuration and distance
# as specified in the input file
# example:
# for a line in the file :  halo1 5 72 48 40 12 16 0
# Truth holds:              Truth['halo1_5kpc'] =[['72', '48'], ['40', '12'], ['16', '0']] 