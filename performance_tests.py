import xlsxwriter
from T_rastrigin import *
from T_Schwefel import *
from T_griewank import *
from T_bohachevsky import *
from T_schaffer_F6 import *
from T_schaffer_F7 import *
from T_rosenbrock import *
from T_ackley1 import *
from T_alpine2 import *
from T_bohachevsky3 import *
from T_schwefel4 import *
from T_shekel5 import *
from T_paviani import *

#   NOTE
#   three changes need to be made for test_function_table
#   1.) the single_function which is being called
#   2.) the optimum generation
#   3.) the tolerance value (5% of optimum offset)
#   (optional) - the console print logs

def table_header(workbook, worksheet, func_name, curr_row):
    worksheet.write(curr_row, 0, func_name, workbook.add_format({'bold': True}))
    return curr_row + 2

def add_search_to_table(workbook, worksheet, dimension, curr_row, results, optimum, search_space, tolerance=1):
    opt_crit = optimum.get_value()
    bold = workbook.add_format({'bold': True})
    worksheet.write(curr_row, 0, 'N dimensions == ' + str(dimension), bold)
    curr_row += 1
    worksheet.write(curr_row, 0, 'Criteria of optimum == ' + str(opt_crit), bold)
    worksheet.write(curr_row + 1, 0, 'Search number:', bold)
    worksheet.write(curr_row + 1, 1, 'Distance from optimum', bold)
    worksheet.write(curr_row + 1, 2, 'Distance in % of search space', bold)
    worksheet.write(curr_row + 1, 3, 'Criteria', bold)
    worksheet.write(curr_row + 1, 4, 'Criteria in % of optimum criteria', bold)
    worksheet.write(curr_row + 1, 5, 'Runtime [s]', bold)
    curr_row += 2
    n_corr = 0  # number of correct optimums considering both criteria and optimum distance (%)
    n_sp = 0    # number of correct searches relative to optimum distance (%)
    n_crit = 0  # number of correct searches relative to criteria (%)
    for i in range(len(results)):
        distance = results[i][0].attribute.measure_difference(optimum)
        criteria = results[i][0].get_criteria()
        dist_perc = distance*100/(search_space*1)  # distance in % of problem space
        # CAREFUL FOR DIVISION BY ZERO IN CASE OF OPTIMAL CRITERIA = 0
        crit_perc = 100 * math.fabs(criteria)  # % of criteria
        worksheet.write(curr_row, 0, i+1, bold)
        worksheet.write(curr_row, 1, distance)
        worksheet.write(curr_row, 2, dist_perc)
        worksheet.write(curr_row, 3, criteria)
        worksheet.write(curr_row, 4, crit_perc)
        worksheet.write(curr_row, 5, results[i][1])
        curr_row += 1
        if dist_perc - tolerance < 0:
            n_sp += 1
        if crit_perc - tolerance < 0:
            n_crit += 1
        if (crit_perc - tolerance < 0) or (dist_perc - tolerance < 0):
            n_corr += 1
    worksheet.write(curr_row + 0, 0, 'Total optimums found == ' + str(n_corr), bold)
    worksheet.write(curr_row + 1, 0, 'In (%) == ' + str(n_corr*100/len(results)), bold)
    worksheet.write(curr_row + 2, 0, 'Total optimums (space) == ' + str(n_sp), bold)
    worksheet.write(curr_row + 3, 0, 'In (%) == ' + str(n_sp*100/len(results)), bold)
    worksheet.write(curr_row + 4, 0, 'Total optimums (criteria) == ' + str(n_crit), bold)
    worksheet.write(curr_row + 5, 0, 'In (%) == ' + str(n_crit * 100 / len(results)), bold)
    return curr_row + 8

def add_results_to_table(worksheet, dimensions, results, n_searches, curr_row):
    col = 0
    for i in range(0, len(results)):
        worksheet.write(curr_row + i, col, dimensions[i])
        worksheet.write(curr_row + i, col + 1, n_searches)
        worksheet.write(curr_row + i, col + 2, results[i])
        worksheet.write(curr_row + i, col + 3, results[i] * 100 / n_searches)
    return curr_row + len(results) + 1

def add_header_to_table(worksheet, func_name, curr_row):
    curr_row += 4
    worksheet.write(curr_row,     0, func_name)
    worksheet.write(curr_row + 1, 0, 'Dimensions')
    worksheet.write(curr_row + 1, 1, 'N searches')
    worksheet.write(curr_row + 1, 2, 'N correct')
    worksheet.write(curr_row + 1, 3, 'Percentage(%)')
    return curr_row + 2


def validate_optimum(x, y, tolerance):
    if type(x) is float:
        if math.fabs(x - y) < tolerance:
            return True
        else:
            return False
    else:
        for i in range(len(x)):
            if math.fabs(x[i] - y[i]) > tolerance:
                return False
        return True

# test a single n-dimensional Rastrigin function, REWORKED
def single_rastrigin(n):
    RastriginSpace.n_dimensions = n
    playground_obj = Playground(400, 9, RastriginSpace, 5000, 35, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end - start]

# REWORKED
def test_rastrigin_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING RASTRIGIN FUNCTION TESTS *************************************')
    RastriginSpace.up_bound = 5.12
    RastriginSpace.low_bound = -5.12
    RastriginSpace.eps = 0.001
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches + 1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_rastrigin(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.05):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = RastriginSpace()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 10.24)
    return curr_row


# test a single n-dimensional Schwefel function, REWORKED
def single_schwefel(n):
    SchwefelSpace.n_dimensions = n
    playground_obj = Playground(200, 6, SchwefelSpace, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_schwefel_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING SCHWEFEL FUNCTION TESTS *************************************')
    SchwefelSpace.up_bound = 500
    SchwefelSpace.low_bound = -500
    SchwefelSpace.eps = 5
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [420.9687 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_schwefel(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 21.04844):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = SchwefelSpace()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 1000)
    return curr_row

# test a single n-dimensional Griewank function, REWORKED
def single_griewank(n):
    GriewankSpace.n_dimensions = n
    playground_obj = Playground(700, 12, GriewankSpace, 5000, 50, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_griewank_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING GRIEWANK FUNCTION TESTS *************************************')
    GriewankSpace.up_bound = 600
    GriewankSpace.low_bound = -600
    GriewankSpace.eps = 0.05
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_griewank(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.02):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = GriewankSpace()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 1200)
    return curr_row

# test a single 2-D Bohachevsky F1 function, REWORKED
def single_bohachevksy(n):
    BohachevskySpace.n_dimensions = n
    playground_obj = Playground(200, 6, BohachevskySpace, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_bohachevksy_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING BOHACHEVSKY F1 FUNCTION TESTS *************************************')
    BohachevskySpace.up_bound = 100
    BohachevskySpace.low_bound = -100
    BohachevskySpace.eps = 0.1
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_bohachevksy(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.02):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = BohachevskySpace()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 200)
    return curr_row

# test a single 2D Schaffer F6 function, REWORKED
def single_schafferF6(n):
    SchafferF6Space.n_dimensions = n
    playground_obj = Playground(700, 12, SchafferF6Space, 5000, 50, 0.00001, 0.00001, 300)
    start = time.time()
    playground_obj.matchday_search(5)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_schafferF6_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING SCHAFFER F6 FUNCTION TESTS *************************************')
    SchafferF6Space.up_bound = 100
    SchafferF6Space.low_bound = -100
    SchafferF6Space.eps = 1
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_schafferF6(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.05):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = SchafferF6Space()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 200)
    return curr_row


# test a single n dimensional Schaffer F7 function, REWORKED
def single_schafferF7(n):
    SchafferF7Space.n_dimensions = n
    playground_obj = Playground(700, 12, SchafferF7Space, 5000, 50, 0.00001, 0.00001, 300)
    start = time.time()
    playground_obj.matchday_search(5)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_schafferF7_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING SCHAFFER F7 FUNCTION TESTS *************************************')
    SchafferF7Space.up_bound = 100
    SchafferF7Space.low_bound = -100
    SchafferF7Space.eps = 1
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_schafferF7(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.05):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = SchafferF7Space()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 200)
    return curr_row

# test a single n-dimensional Rosenbrock function
def single_rosenbrock(n):
    RosenbrockSpace.n_dimensions = n
    RosenbrockSpace.up_bound = 2.048
    RosenbrockSpace.low_bound = -2.048
    RosenbrockSpace.eps = 0.2
    playground_obj = Playground(500, 10, RosenbrockSpace, 5000, 49, 0.00000001, 0.00000001, 150)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_rosenbrock_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING ROSENBROCK FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_rosenbrock(n)
            real_optimum = [1 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.05):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# test a single n-dimensional Ackley function
def single_ackley1(n):
    Ackley1Space.n_dimensions = n
    Ackley1Space.up_bound = 35
    Ackley1Space.low_bound = -35
    Ackley1Space.eps = 0.005
    playground_obj = Playground(200, 6, Ackley1Space, 5000, 30, 0.00000001, 0.00000001, 150)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_ackley1_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING ACKLEY1 FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_ackley1(n)
            real_optimum = [0 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.05):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results


# test a single n-dimensional Ackley function
def single_alpine2(n):
    Alpine2Space.n_dimensions = n
    Alpine2Space.up_bound = 10
    Alpine2Space.low_bound = 0
    Alpine2Space.eps = 0.001
    playground_obj = Playground(200, 6, Alpine2Space, 5000, 30, 0.00000001, 0.00000001, 350)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_alpine2_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING ALPINE2 FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_alpine2(n)
            real_optimum = [7.9170526982 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.396):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# test a single 2-D Bohachevsky F3 function, REWORKED
def single_bohachevksy3(n):
    BohachevskySpace3.n_dimensions = n
    playground_obj = Playground(200, 6, BohachevskySpace3, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_bohachevksy3_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING BOHACHEVSKY F3 FUNCTION TESTS *************************************')
    BohachevskySpace3.up_bound = 100
    BohachevskySpace3.low_bound = -100
    BohachevskySpace3.eps = 0.1
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [0 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_bohachevksy3(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.02):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = BohachevskySpace3()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 200)
    return curr_row

# test a single n-dimensional Schwefel4 function, REWORKED
def single_schwefel4(n):
    Schwefel4Space.n_dimensions = n
    playground_obj = Playground(200, 6, Schwefel4Space, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_schwefel4_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING SCHWEFEL 4 FUNCTION TESTS *************************************')
    Schwefel4Space.up_bound = 10
    Schwefel4Space.low_bound = 0
    Schwefel4Space.eps = 0.01
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [1 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_schwefel4(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.02):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = Schwefel4Space()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 10)
    return curr_row

# test a single 4D Shekel5 function, REWORKED
def single_shekel5(n):
    Shekel5Space.n_dimensions = n
    playground_obj = Playground(700, 12, Shekel5Space, 5000, 50, 0.00001, 0.00001, 300)
    start = time.time()
    playground_obj.matchday_search(2)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum, end-start]

#   REWORKED
def test_shekel5_table(p, q, workbook, worksheet, curr_row):
    dimensions = p
    n_searches = q
    print('******************************* RUNNING SHEKEL 5 FUNCTION TESTS *************************************')
    Shekel5Space.up_bound = 10
    Shekel5Space.low_bound = 0
    Shekel5Space.eps = 0.01
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        iteration_results = []
        raw_optimum = [4 for k in range(n)]
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            result = single_shekel5(n)
            iteration_results.append(result)
            if validate_optimum(result[0].attribute.x, raw_optimum, 0.1):
                print('The real optimum has been found!')
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        optimum = Shekel5Space()
        optimum.set_solution(raw_optimum)
        curr_row = add_search_to_table(workbook, worksheet, n, curr_row, iteration_results, optimum, 200)
    return curr_row

# test a single n-dimensional Shekel 5 function
def single_paviani(n):
    PavianiSpace.n_dimensions = n
    PavianiSpace.up_bound = 9.999
    PavianiSpace.low_bound = 2.001
    PavianiSpace.eps = 0.01
    playground_obj = Playground(200, 6, PavianiSpace, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(5)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_paviani_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING PAVIANI FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_paviani(n)
            real_optimum = [9.350266 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.4675):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results


def main():

    workbook = xlsxwriter.Workbook('new_schwefel4_11_15.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 6, 25)
    curr_row = 0

    dimensions = [16]
    n_searches = 50

    # Schwefel, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Schwefel', curr_row)
    #curr_row = test_schwefel_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Rastrigin, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Rastrigin', curr_row)
    #curr_row = test_rastrigin_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Schaffer F6, only defined for 2D, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Schaffer F6', curr_row)
    #curr_row = test_schafferF6_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # X
    # Schaffer F7, needs at least 2D, reworked
    #curr_row = table_header(workbook, worksheet, 'Schaffer F7', curr_row)
    #curr_row = test_schafferF7_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Shekel 5, only valid dimension is 4, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Shekel 5', curr_row)
    #curr_row = test_shekel5_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # X
    # Griewank, reworked
    #curr_row = table_header(workbook, worksheet, 'Griewank', curr_row)
    #curr_row = test_griewank_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Bohachevsky F1, only defined for 2D, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Bohachevsky F1', curr_row)
    #curr_row = test_bohachevksy_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Bohachevsky F3, only defined for 2D, reworked, done testing
    #curr_row = table_header(workbook, worksheet, 'Bohachevsky F3', curr_row)
    #curr_row = test_bohachevksy3_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # Schwefel 4, reworked
    curr_row = table_header(workbook, worksheet, 'Schwefel 4', curr_row)
    curr_row = test_schwefel4_table(dimensions, n_searches, workbook, worksheet, curr_row)

    # ----------

    # Schaffer F7
    #results = test_schafferF7_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Schaffer F7', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Rosenbrock
    #results = test_rosenbrock_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Rosenbrock', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Ackley1
    #results = test_ackley1_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Ackley1', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Alpine2
    #results = test_alpine2_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Alpine2', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Paviani - 10 dimensional problem
    #results = test_paviani_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Paviani', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    workbook.close()


main()
