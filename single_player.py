# G2_T08
# Members: Brian Goh Jun Wei, Lee Pei Yi

import numpy as np

def get_route(p, v, flags):
	flag_dict = generate_flags_dict(flags)

	start = ['start', '0', '0', '0']
	list_of_routes = []
	
	for i in range(25):
		flag_pool = flags.copy()
		points = 0
		route = [start]

		while points < p and flag_pool:
			last_flag = route[-1]

			lowest_dist_over_value = get_dist_over_value(route[0], flag_pool[0])
			# list which stores all dist_over_value from last_flag LOWER than stored flag
			lowest_dist_over_value_list = [[flag_pool[0], lowest_dist_over_value]]

			for flag_candidate in flag_pool:
				this_dist_over_value = get_dist_over_value(route[-1], flag_candidate)
				if(this_dist_over_value < lowest_dist_over_value):
					lowest_dist_over_value_list.append([flag_candidate, this_dist_over_value])
					lowest_dist_over_value = this_dist_over_value

			# keep best 2 flags
			flags_to_choose = lowest_dist_over_value_list[-2:]

			if len(flags_to_choose) == 2:
				flag1, flag2 = flags_to_choose
				flag1_dist_over_value = flag1[1]
				flag2_dist_over_value = flag2[1]

				perc_diff = get_change(flag1_dist_over_value, flag2_dist_over_value)

				if perc_diff < 30:
					# randomly select 1 flag
					rand_int = np.random.randint(len(flags_to_choose))
					chosen_flag = flags_to_choose[rand_int][0]
				else:
					if flag1_dist_over_value < flag2_dist_over_value:
						chosen_flag = flag1[0]
					else:
						chosen_flag = flag2[0]
			else:
				chosen_flag = flags_to_choose[0][0]

			route.append(chosen_flag)
			flag_pool.remove(chosen_flag)
			points += float(chosen_flag[1])

		list_of_routes.append(route)

	best_route = list_of_routes[0]
	lowest_dist_of_all_routes = get_route_dist(list_of_routes[0], flag_dict, v)

	for route in list_of_routes[1:]:
		this_dist = get_route_dist(route, flag_dict, v)
		if(this_dist < lowest_dist_of_all_routes):
			lowest_dist_of_all_routes = this_dist
			best_route = route

	best_route = randomised_two_opt(best_route, flag_dict, v)
	best_route.remove(start)
	
	return ([flag[0] for flag in best_route])

def get_dist_over_value(old_node, new_node):
	return get_distance(old_node, new_node) / float(new_node[1])

def get_distance(node_A, node_B):
	return ((float(node_A[2]) - float(node_B[2])) ** 2 + (float(node_A[3]) - float(node_B[3])) ** 2) ** 0.5

def get_route_dist(your_route, flags_dict, v):
	route = your_route.copy()

	dist = 0

	start_node = route[0]
	last_node = start_node

	for flag in route[1:]:
		flagID = flag[0]
		curr_node = flags_dict[flagID]
		dist_to_curr_node = get_distance(last_node, curr_node)
		dist += dist_to_curr_node

		last_node = curr_node

	if v == 2:
		dist += get_distance(last_node, start_node)

	return dist

def generate_flags_dict(flags_list):
  d = {'start': ['start', 0, 0, 0]}
  for item in flags_list:
    #             flagID,  points,       x,              y
    d[item[0]] = [item[0], int(item[1]), float(item[2]), float(item[3])]
  return d

def randomised_two_opt(route, flag_dict, v):
	if v == 2:
		route = route[:]
		start_point_idx = route.index(['start', '0', '0', '0'])
		route = route[start_point_idx:] + route[:start_point_idx]

	overall_best_route = route
	best_route_dist = get_route_dist(overall_best_route, flag_dict, v)

	for iteration in range(len(route)*10):
		i = np.random.randint(1, len(route)-2)
		j = np.random.randint(i+2, len(route))
		
		new_route = overall_best_route.copy()
		new_route[i:j+1] = new_route[j:i-1:-1]
		this_dist = get_route_dist(new_route, flag_dict, v)

		if this_dist < best_route_dist:
			overall_best_route = new_route
			best_route_dist = this_dist

	return overall_best_route

def get_change(current, previous):
	if current == previous:
		return 100.0
	return (abs(current - previous) / previous) * 100.0