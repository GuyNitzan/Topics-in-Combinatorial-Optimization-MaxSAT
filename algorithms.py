NUM_OF_DIFFERENT_CNFS = 25  # Number of iteration to run the algorithm. answer will be average on all
NUM_OF_CLAUSES = 540  # Number of clauses in each CNF
MIN_NUM_LITS_PER_CLAUSE = 3  # minimum number of literals per clause - minimum optional is 2
MAX_NUM_LITS_PER_CLAUSE = 3  # maximum number of literals per claus
NUM_OF_VARS = 100

from utils import *

'''
All algorithms return an assignment.

'''


def algorithm_1():  # Choose random assignment and
    # print ('Algorithm 1 results')
    # print_program_vars()
    return rand_assignment()


def algorithm_2(cnf):  # Choose by max
    # print ('Algorithm 2 results')
    # print_program_vars()
    return find_assignment_by_max_and_clean(cnf)


def algorithm_2_b():  # Choose by max - Do not update list of maximum occurrences
    # print ('Algorithm 2b results')
    # print_program_vars()
    return find_assignment_by_max()


def algorithm_3(cnf):  # Choose by max diff
    # print ('Algorithm 3 results')
    # print_program_vars()
    return find_assignment_by_max_diff_and_clean(cnf)


def algorithm_4(cnf):  # Choose by Expected value
    # print ('Algorithm 4 results')
    # print_program_vars()
    return find_assignment_by_expected_value(cnf)


def local_search(assignment, copy_of_cnf, num_of_iter):  # Use local search to try and improve the current given
    # assignment. pick number of tries of improvement
    return find_random_local_max(assignment, copy_of_cnf, num_of_iter)


def local_search_2(assignment, copy_of_cnf, num_of_iter):  # Use local search to try and improve the current given
    # assignment. pick number of tries of improvement
    return find_ordered_local_max(assignment, copy_of_cnf, num_of_iter)


def analyze_results(cnf, assignment):  # count number of satisfied clauses under an assignment in the specific cnf
    return count_satisified(cnf, assignment)


if __name__ == "__main__":
    total_count = 0
    max2 = 0
    max3 = 0
    total_count_after_local_search = 0
    for iteration in range(0, NUM_OF_DIFFERENT_CNFS):
        my_cnf = create_cnf()
        copy_cnf = copy.deepcopy(my_cnf)
        copy_cnf_2 = copy.deepcopy(my_cnf)
        assignment = algorithm_1() # Change used algorithm here. Denote algorithms 2,3,4 should receive 'my_cnf' as a var
        assignment_2 = copy.deepcopy(assignment)
        max2 = max(max2, analyze_results(copy_cnf, assignment))
        assignment_2 = local_search(assignment_2, copy_cnf_2, 500)
        max3 = max(max3, analyze_results(copy_cnf, assignment_2))
        total_count = total_count + analyze_results(copy_cnf, assignment)


    print ('Results:')
    print ('Maximum of satisfied clauses:' + str(max2))
    print ('Maximum Percentage of satisfied clauses: ' + str(
        float(max2) / NUM_OF_CLAUSES * 100))
    print ('Number of satisfied clauses in average: ' + str(total_count / NUM_OF_DIFFERENT_CNFS))
    print ('Percentage of satisfied clauses by average: ' + str(
        float(total_count / NUM_OF_DIFFERENT_CNFS) / NUM_OF_CLAUSES * 100))
    print ('Satisfied clauses with local search:' + str(max3))
    print ('Percentage of satisfied clauses with local search: ' + str(
        float(max3) / NUM_OF_CLAUSES * 100))
