import numpy as np

def trapezoidal_integrate(initial_values=(0,0,0), sample1=(0,0,0), sample2=(0,0,0), sampling_time=0.2):
	initial_values = np.array(initial_values)
	sample1 = np.array(sample1)
	sample2 = np.array(sample2)

	bottom_rect = sample1*sampling_time
	upper_trig = (sample2-sample1)*sampling_time/2

	area = bottom_rect + upper_trig

	final_value = initial_values + area
	return final_value

def orientation_tf(raw_data):
	#TODO: find actual mapping
	return raw_data[0], raw_data[1]


def integrate_1_tf(raw_data,previous_acc,mouse_pos):
	new_acc = (raw_data[0],raw_data[1])
 	prev_acc = (previous_acc[0],previous_acc[1])

 	mouse_pos_x, mouse_pos_y = tf.trapezoidal_integrate(mouse_pos,new_acc,prev_acc)
 	return mouse_pos_x, mouse_pos_y
  
 def integrate_2_tf(raw_data,previous_acc,previous_vel,mouse_pos):
 	new_acc = (raw_data[0],raw_data[1])
	prev_acc = (previous_acc[0],previous_acc[1])
	prev_vel = (previous_vel[0],previous_vel[1])

	mouse_vel_x,mouse_vel_y = tf.trapezoidal_integrate(prev_vel,new_acc,prev_acc,0.1)

	new_vel = (mouse_vel_x, mouse_vel_y)
	mouse_pos_x, mouse_pos_y = tf.trapezoidal_integrate(mouse_pos,new_vel,prev_vel,0.1)

	return mouse_pos_x, mouse_pos_y, mouse_vel_x, mouse_vel_y
