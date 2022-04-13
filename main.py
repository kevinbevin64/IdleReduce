



import argparse
import sys

sys.setrecursionlimit(70000)








def combo_selectors(max_combo_length, accumulated_combos=None):


    if accumulated_combos == None:
        return combo_selectors(max_combo_length, accumulated_combos=[[], [0]])

    combo = accumulated_combos[-1]


    for element in reversed(combo):
        element_index = combo.index(element)
        # reached_end is True if element cannot be higher. 
        # based on its index
        reached_end = (element == max_combo_length - (len(combo) - element_index - 1) -1)
        if reached_end:
            # if the entire combo cannot be higher
            if element_index == 0:
                # if the combo cannot lengthen
                if len(combo) == max_combo_length: 
                    return accumulated_combos
                # increase the combo size
                # creates a new combo like [0, 1, 2, 3] if size becomes 4
                else:
                    new_combo = []
                    for i in range(0, len(combo) + 1):
                        new_combo.append(i)
                    accumulated_combos.append(new_combo)
                    return combo_selectors(max_combo_length, accumulated_combos)
            else:
                continue
        

        else:
            new_combo = combo.copy()
            # increment the value by one
            # reset the following elements to make them consecutive to the incremented element
            # [0, 1, 9] changes to [0, 2, 3] where '1' is incremented
            new_combo[element_index] += 1
            new_value = element + 2
            for i in range(element_index + 1, len(new_combo)):
                new_combo[i] = new_value
                new_value += 1
            accumulated_combos.append(new_combo)
            return combo_selectors(max_combo_length, accumulated_combos)






def pair(combos, max_length):

    def opposite_of(combo, possible_elements):
        """
        if [1] is combo, and possible_elements is [1, 2, 3],
        the opposite of combo is [2, 3]
        """
        opposite = []
        for element in possible_elements:
            if element not in combo:
                opposite.append(element)

        return opposite

    possible_elements = []
    for i in range(max_length):
        possible_elements.append(i)

    output = []
    for combo in combos:
        pair = []
        opposite = opposite_of(combo, possible_elements)
        pair.append(combo)
        pair.append(opposite)

        combos.remove(opposite)

        output.append(pair)
        output.append(reversed(pair))

    return output



def selector2value(selector_combo, tasks):
    grouped_tasks = []
    for selector_pair in selector_combo:
        sub_group = []

        for selector_group in selector_pair:
            values = []
            for selector in selector_group:
                values.append(tasks[selector])
            sub_group.append(values)
        
        grouped_tasks.append(sub_group)
    
    return grouped_tasks

def operating_time(pair, operators):
    # print(sum(pair[0]) / operators[0])
    # print(sum(pair[1]) / operators[1])
    return max(
        sum(pair[0]) / operators[0], sum(pair[1]) / operators[1]
    )
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs="+")
    parser.add_argument("--operators", nargs="+")
    value = parser.parse_args()
    tasks = value.tasks
    for i, item in enumerate(tasks):
        tasks[i] = int(item)


    operators = value.operators
    for i, item in enumerate(operators):
        operators[i] = int(item)

    if len(operators) != 2:
        print("Number of operators should be 2. ")
        sys.exit()



    tasks_length = len(tasks)

    pairs = pair(combo_selectors(tasks_length), tasks_length)

    values = selector2value(pairs, tasks)


    min_time = None
    most_efficient_pair = None

    for pair in values:

        if min_time == None or operating_time(pair, operators) < min_time:
            min_time = operating_time(pair, operators)
            most_efficient_pair = pair

    print(f"\nOperator {operators[0]} should be given tasks {most_efficient_pair[0]}. ")
    print(f"Operator {operators[1]} should be given tasks {most_efficient_pair[1]}. ")
    print(f"\nIn {round(min_time, ndigits=1)}s, both will have completed their tasks. \n")






