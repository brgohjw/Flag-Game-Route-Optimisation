import numpy as np

def get_routes(p, v, flags, n):
	flag_dict = generate_flags_dict(flags)
	flag_dict['start'] = ['start', 0, 0, 0]
	flag_pool = flags
	list_of_route_lists = []
	round_robin = list(range(1, n+1))

	start = ['start', '0', '0', '0']

	for i in range(10):
		route_dict = {}

		for i in range(1, n+1):
			route_dict[i] = [['start', '0', '0', '0']]

		flag_pool = flags.copy()
		points = 0
		# route = [start]

		while points < p and flag_pool:
			player_idx = round_robin[0]
			this_route = route_dict[player_idx]

			last_flag = this_route[-1]

			lowest_dist_over_value = get_dist_over_value(this_route[0], flag_pool[0])
			# list which stores all dist_over_value from last_flag LOWER than stored flag
			lowest_dist_over_value_list = [[flag_pool[0], lowest_dist_over_value]]

			for flag_candidate in flag_pool:
				this_dist_over_value = get_dist_over_value(this_route[-1], flag_candidate)
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

			this_route.append(chosen_flag)
			flag_pool.remove(chosen_flag)
			points += float(chosen_flag[1])


		this_list_of_routes = []
		for i in range(1, len(route_dict) + 1):
			this_list_of_routes.append(route_dict[i])

		list_of_route_lists.append(this_list_of_routes)

	best_route_list = list_of_route_lists[0]
	lowest_dist_of_all_routes = get_q2_total_dist(list_of_route_lists[0], flag_dict, v, n)

	for route_list in list_of_route_lists[1:]:
		this_dist = get_q2_total_dist(route_list, flag_dict, v, n)
		if(this_dist < lowest_dist_of_all_routes):
			lowest_dist_of_all_routes = this_dist
			best_route_list = route_list

	for i in range(len(best_route_list)):
		this_route = best_route_list[i]
		if len(this_route) >= 4:
			this_route = randomised_two_opt(this_route, flag_dict, v)
		this_route.remove(start)
		best_route_list[i] = [flag[0] for flag in this_route]

	return best_route_list;

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

	if v == 2:   # cycle back to SP
		dist += get_distance(last_node, start_node)

	return dist # no error

def get_q2_total_dist(your_routes, flags_dict, v, n):
	# need to call get_dist_and_points_q1 for every route in your_routes
	tot_dist = 0
	tot_points = 0
  
	for route in your_routes:
		curr_dist = get_route_dist(route, flags_dict, v)

	tot_dist += curr_dist

	return tot_dist

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
