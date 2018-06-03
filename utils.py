import random
import copy
import algorithms as program_vars

# A class defining a literal with appropriate fields
class literal:
    def __init__(self, literal_number, is_not):
        self.literal_number = literal_number
        self.is_not = is_not


VARS_DATA = {}

# Init function for a variables list
def create_new_vars_list():
    literals = []
    for i in range(0, program_vars.NUM_OF_VARS):
        k = literal(i, True)
        literals.append(k)
        k = literal(i, False)
        literals.append(k)
    return literals

# For debug purposes
def print_cnf(inp_cnf):
    cnf = []
    for clause in inp_cnf:
        cls = []
        for lit in clause:
            lit_list = [lit.literal_number, lit.is_not]
            cls.append(lit_list)
        cnf.append(cls)
    print(cnf)

# Create CNF
def create_cnf():
    current_expected_val = 0
    vars_list = create_new_vars_list()
    for i in range(0, program_vars.NUM_OF_VARS):
        # This is a dictionary that holds data for each variable (6 keys). This is data helpful for the different algorithms.
        VARS_DATA[i] = {'occ_as_not': 0, 'occ_as_norm': 0, 'diff': 0, 'max_occ': 0, 'max_value': 0,
                        'is_occ_balanced': 0}
    cnf = []
    for j in range(0, program_vars.NUM_OF_CLAUSES):
        iteration = 0
        a_clause = []
        # Create clause
        clause_size = random.randint(program_vars.MIN_NUM_LITS_PER_CLAUSE, program_vars.MAX_NUM_LITS_PER_CLAUSE)
        current_expected_val += 1 - (float(1) / pow(2, clause_size))
        for k in range(0, clause_size):
            rand = random.randint(0, 2 * program_vars.NUM_OF_VARS - iteration - 1)
            iteration += 1
            to_put = vars_list.pop(rand)
            a_clause.append(to_put)
            if not to_put.is_not:
                VARS_DATA[to_put.literal_number]['occ_as_not'] += 1
            else:
                VARS_DATA[to_put.literal_number]['occ_as_norm'] += 1
        cnf.append(a_clause)
        vars_list = create_new_vars_list()
    for i in range(0, program_vars.NUM_OF_VARS):
        VARS_DATA[i]['diff'] = abs(VARS_DATA[i]['occ_as_norm'] - VARS_DATA[i]['occ_as_not'])
        if max(VARS_DATA[i]['occ_as_norm'], VARS_DATA[i]['occ_as_not']) == VARS_DATA[i]['occ_as_not']:
            VARS_DATA[i]['max_occ'] = 'occ_as_not'
            VARS_DATA[i]['max_value'] = VARS_DATA[i]['occ_as_not']
        else:
            VARS_DATA[i]['max_occ'] = 'occ_as_norm'
            VARS_DATA[i]['max_value'] = VARS_DATA[i]['occ_as_norm']
        if VARS_DATA[i]['occ_as_not'] == VARS_DATA[i]['occ_as_norm']:
            VARS_DATA[i]['is_occ_balanced'] = 1
    return cnf

# Algorithm 1
def rand_assignment():
    assignment = {}
    for j in range(0, program_vars.NUM_OF_VARS):
        assignment[j] = (random.randint(0, 1))
    return assignment


def count_satisified(a_cnf, an_assignment):
    count = 0
    for clause in a_cnf:
        for lit in clause:
            if not (lit.is_not != an_assignment[lit.literal_number]):
                count += 1
                break
    return count

# Part of 2.c, 2.d in algorithms 2 and 3. Adress attached paper for more information
def clean_literal_from_cnf(the_cnf, the_lit, is_not):
    for clause in the_cnf:
        for lit in clause:
            if lit.literal_number == the_lit and lit.is_not == is_not:
                for clause_lit in clause:
                    update_lit_after_deletion(clause_lit)
                the_cnf.remove(clause)
                break

# Part of 2.c, 2.d in algorithms 2 and 3. Adress attached paper for more information
def update_lit_after_deletion(lit):
    if lit.is_not and VARS_DATA[lit.literal_number]['is_occ_balanced'] == 1 and VARS_DATA[lit.literal_number][
        'diff'] != -1:
        VARS_DATA[lit.literal_number]['occ_as_not'] -= 1
        VARS_DATA[lit.literal_number]['is_occ_balanced'] = 0
        VARS_DATA[lit.literal_number]['max_occ'] = 'occ_as_norm'
        VARS_DATA[lit.literal_number]['diff'] = 1
    elif (not lit.is_not) and VARS_DATA[lit.literal_number]['is_occ_balanced'] == 1 and VARS_DATA[lit.literal_number][
        'diff'] != -1:
        VARS_DATA[lit.literal_number]['occ_as_norm'] -= 1
        VARS_DATA[lit.literal_number]['is_occ_balanced'] = 0
        VARS_DATA[lit.literal_number]['max_occ'] = 'occ_as_not'
        VARS_DATA[lit.literal_number]['diff'] = 1
    elif lit.is_not and VARS_DATA[lit.literal_number]['occ_as_not'] > VARS_DATA[lit.literal_number]['occ_as_norm']:
        VARS_DATA[lit.literal_number]['occ_as_not'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] > -1:
            VARS_DATA[lit.literal_number]['diff'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] == 0:
            VARS_DATA[lit.literal_number]['is_occ_balanced'] = 1
    elif lit.is_not and VARS_DATA[lit.literal_number]['occ_as_not'] < VARS_DATA[lit.literal_number]['occ_as_norm']:
        VARS_DATA[lit.literal_number]['occ_as_not'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] > -1:
            VARS_DATA[lit.literal_number]['diff'] += 1
        if VARS_DATA[lit.literal_number]['diff'] == 0:
            VARS_DATA[lit.literal_number]['is_occ_balanced'] = 1
    elif (not lit.is_not) and VARS_DATA[lit.literal_number]['occ_as_not'] > VARS_DATA[lit.literal_number][
        'occ_as_norm']:
        VARS_DATA[lit.literal_number]['occ_as_norm'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] > -1:
            VARS_DATA[lit.literal_number]['diff'] += 1
        if VARS_DATA[lit.literal_number]['diff'] == 0:
            VARS_DATA[lit.literal_number]['is_occ_balanced'] = 1
    elif (not lit.is_not) and VARS_DATA[lit.literal_number]['occ_as_not'] < VARS_DATA[lit.literal_number][
        'occ_as_norm']:
        VARS_DATA[lit.literal_number]['occ_as_norm'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] > -1:
            VARS_DATA[lit.literal_number]['diff'] -= 1
        if VARS_DATA[lit.literal_number]['diff'] == 0:
            VARS_DATA[lit.literal_number]['is_occ_balanced'] = 1


def max_occ_get():
    max_occ_of_all = 0
    max_occ_of_all_ind = -1
    for k in range(0, program_vars.NUM_OF_VARS):
        max_occ_of_all = max(max_occ_of_all, VARS_DATA[k][VARS_DATA[k]['max_occ']])
        if max_occ_of_all == VARS_DATA[k][VARS_DATA[k]['max_occ']]:
            max_occ_of_all_ind = k
    return max_occ_of_all, max_occ_of_all_ind


def max_diff_get():
    max_diff_of_all = 0
    max_diff_of_all_ind = -1
    for k in range(0, program_vars.NUM_OF_VARS):
        max_diff_of_all = max(max_diff_of_all, VARS_DATA[k]['diff'])
        if max_diff_of_all == VARS_DATA[k]['diff']:
            max_diff_of_all_ind = k
    return max_diff_of_all, max_diff_of_all_ind

# Algorithm 2b
def find_assignment_by_max():
    assign = {}
    for var in range(0, program_vars.NUM_OF_VARS):
        max_occ_of_all, max_occ_of_all_ind = max_occ_get()
        if max_occ_of_all == 0:
            break
        if VARS_DATA[max_occ_of_all_ind]['occ_as_not'] == max_occ_of_all:
            assign[max_occ_of_all_ind] = 0
        else:
            assign[max_occ_of_all_ind] = 1
        VARS_DATA[max_occ_of_all_ind]['occ_as_not'] = 0
        VARS_DATA[max_occ_of_all_ind]['occ_as_norm'] = 0
    return assign

# Algorithm 2
def find_assignment_by_max_and_clean(a_cnf):
    assign = {}
    for var in range(0, program_vars.NUM_OF_VARS):
        max_occ_of_all, max_occ_of_all_ind = max_occ_get()
        if max_occ_of_all == 0:
            assign[max_occ_of_all_ind] = 1
        elif VARS_DATA[max_occ_of_all_ind]['occ_as_not'] == max_occ_of_all:
            assign[max_occ_of_all_ind] = 0
        else:
            assign[max_occ_of_all_ind] = 1
        VARS_DATA[max_occ_of_all_ind]['occ_as_not'] = -1
        VARS_DATA[max_occ_of_all_ind]['occ_as_norm'] = -1
        clean_literal_from_cnf(a_cnf, max_occ_of_all_ind, assign[max_occ_of_all_ind])
    return assign


def find_assignment_by_max_diff():
    assign = {}
    for var in range(0, program_vars.NUM_OF_VARS):
        max_diff_of_all, max_diff_of_all_ind = max_diff_get()
        if (VARS_DATA[max_diff_of_all_ind]['occ_as_not'] - VARS_DATA[max_diff_of_all_ind][
            'occ_as_norm']) == max_diff_of_all:
            assign[max_diff_of_all_ind] = 0
        else:
            assign[max_diff_of_all_ind] = 1
        VARS_DATA[max_diff_of_all_ind]['diff'] = -1
    return assign

# Algorithm 3
def find_assignment_by_max_diff_and_clean(a_cnf):
    assign = {}
    for var in range(0, program_vars.NUM_OF_VARS):
        max_diff_of_all, max_diff_of_all_ind = max_diff_get()
        if (VARS_DATA[max_diff_of_all_ind]['occ_as_not'] - VARS_DATA[max_diff_of_all_ind][
            'occ_as_norm']) == max_diff_of_all:
            assign[max_diff_of_all_ind] = 0
        else:
            assign[max_diff_of_all_ind] = 1
        VARS_DATA[max_diff_of_all_ind]['diff'] = -1
        clean_literal_from_cnf(a_cnf, max_diff_of_all_ind, assign[max_diff_of_all_ind])
    return assign

# Loacl search of type 1
def find_random_local_max(an_assignment, a_cnf, num_of_tries):
    new_assignment = {}
    for i in range(0, program_vars.NUM_OF_VARS):
        new_assignment[i] = an_assignment[i]
    for i in range(0, num_of_tries):
        rand_var = random.randint(0, program_vars.NUM_OF_VARS - 1)
        if new_assignment[rand_var] == 1:
            new_assignment[rand_var] = 0
        else:
            new_assignment[rand_var] = 1

        if count_satisified(a_cnf, new_assignment) < count_satisified(a_cnf, an_assignment):
            new_assignment[rand_var] = an_assignment[rand_var]
        else:
            an_assignment[rand_var] = new_assignment[rand_var]
    return new_assignment

# Loacl search of type 2
def find_ordered_local_max(an_assignment, a_cnf, num_of_tries):
    new_assignment = {}
    for i in range(0, program_vars.NUM_OF_VARS):
        new_assignment[i] = an_assignment[i]
    for i in range(0, num_of_tries):
        for j in range(0, program_vars.NUM_OF_VARS - 1):
            if new_assignment[j] == 1:
                new_assignment[j] = 0
            else:
                new_assignment[j] = 1

            if count_satisified(a_cnf, new_assignment) < count_satisified(a_cnf, an_assignment):
                new_assignment[j] = an_assignment[j]
            else:
                an_assignment[j] = new_assignment[j]
    return new_assignment

# Algorithm 4
def find_assignment_by_expected_value(my_cnf):
    assign = {}
    count = 0
    count2 = 0
    vars_num_list = list(range(0, program_vars.NUM_OF_VARS))
    random.shuffle(vars_num_list)

    for i in vars_num_list:
        copy_cnf = copy.deepcopy(my_cnf)
        copy_cnf_2 = copy.deepcopy(my_cnf)
        clauses_to_remove = []
        for clause in copy_cnf:
            found_with_not = False
            found_without_not = False
            index_to_remove = -1
            for lit in range(0, len(clause)):
                if clause[lit].literal_number == i and clause[lit].is_not:
                    found_with_not = True
                if clause[lit].literal_number == i and not clause[lit].is_not:
                    found_without_not = True
                    index_to_remove = lit
            if found_with_not:
                clauses_to_remove.append(clause)
                count += 1
            elif found_without_not:
                count = count + (float(1) / pow(2, len(clause))) - (float(1) / pow(2, len(clause) - 1))
                clause.remove(clause[index_to_remove])
        for k in clauses_to_remove:
            copy_cnf.remove(k)

        clauses_to_remove = []
        for clause in copy_cnf_2:
            found_with_not = False
            found_without_not = False
            index_to_remove = -1
            for lit in range(0, len(clause)):
                if clause[lit].literal_number == i and clause[lit].is_not:
                    found_with_not = True
                    index_to_remove = lit
                if clause[lit].literal_number == i and not clause[lit].is_not:
                    found_without_not = True
            if found_without_not:
                clauses_to_remove.append(clause)
                count2 += 1
            elif found_with_not:
                count2 = count2 + (float(1) / pow(2, len(clause))) - (float(1) / pow(2, len(clause) - 1))
                clause.remove(clause[index_to_remove])
        for k in clauses_to_remove:
            copy_cnf_2.remove(k)
        if count > count2:
            assign[i] = 1
            my_cnf = copy_cnf
            count2 = count
        else:
            assign[i] = 0
            my_cnf = copy_cnf_2
            count = count2
    return assign


def print_program_vars():
    print ('Number of iterations/CNFs: ' + str(program_vars.NUM_OF_DIFFERENT_CNFS))
    print ('Number of clauses: ' + str(program_vars.NUM_OF_CLAUSES))
    print ('Number of literals per clause is in the range: ' + str(program_vars.MIN_NUM_LITS_PER_CLAUSE) + ' to ' + str(program_vars.MAX_NUM_LITS_PER_CLAUSE))
    print ('Number of variables: ' + str(program_vars.NUM_OF_VARS))
