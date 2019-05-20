import numpy as np

def trapezoidal_integrate(initial_values=(0,0,0), sample1=(0,0,0), sample2=(0,0,0), sampling_time=0.1):
	initial_values = np.array(initial_values)
	sample1 = np.array(sample1)
	sample2 = np.array(sample2)

	bottom_rect = sample1*sampling_time
	upper_trig = (sample2-sample1)*sampling_time/2

	area = bottom_rect + upper_trig

	final_value = initial_values + area
	return final_value