import xlsxwriter
from T_rastrigin import *
from T_Schwefel import *
from T_griewank import *
from T_bohachevsky import *
from T_schaffer_F6 import *
from T_schaffer_F7 import *
from T_rosenbrock import *

#   NOTE
#   three changes need to be made for test_function_table
#   1.) the single_function which is being called
#   2.) the optimum generation
#   3.) the tolerance value (5% of optimum offset)
#   (optional) - the console print logs

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

# test a single n-dimensional Rastrigin function
def single_rastrigin(n):
    RastriginSpace.n_dimensions = n
    RastriginSpace.up_bound = 5.12
    RastriginSpace.low_bound = -5.12
    RastriginSpace.eps = 0.001
    playground_obj = Playground(200, 6, RastriginSpace, 5000, 30, 0.00000001, 0.00000001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_rastrigin_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING RASTRIGIN FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_rastrigin(n)
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


# test a single n-dimensional Schwefel function
def single_schwefel(n):
    SchwefelSpace.n_dimensions = n
    SchwefelSpace.up_bound = 500
    SchwefelSpace.low_bound = -500
    SchwefelSpace.eps = 5
    playground_obj = Playground(200, 6, SchwefelSpace, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(5)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_schwefel_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING SCHWEFEL FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_schwefel(n)
            real_optimum = [420.9687 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 21.04844):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# test a single n-dimensional Griewangk function
def single_griewank(n):
    GriewankSpace.n_dimensions = n
    GriewankSpace.up_bound = 600
    GriewankSpace.low_bound = -600
    GriewankSpace.eps = 5
    playground_obj = Playground(1000, 5, GriewankSpace, 5000, 185, 0.0000001, 0.000000001, 350)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_griewank_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING GRIEWANK FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_griewank(n)
            real_optimum = [0 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.1):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# NOTE - only defined for two variables!!
def single_bohachevksy(n):
    BohachevskySpace.n_dimensions = n
    BohachevskySpace.up_bound = 600
    BohachevskySpace.low_bound = -600
    BohachevskySpace.eps = 0.1
    playground_obj = Playground(200, 6, BohachevskySpace, 5000, 30, 0.0000001, 0.000000001, 350)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_bohachevsky_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING BOHACHEVSKY FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_bohachevksy(n)
            real_optimum = [0 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.1):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# NOTE - only defined for two variables!!
def single_schafferF6(n):
    SchafferF6Space.n_dimensions = n
    SchafferF6Space.up_bound = 100
    SchafferF6Space.low_bound = -100
    SchafferF6Space.eps = 1
    playground_obj = Playground(1000, 16, SchafferF6Space, 5000, 61, 0.0000001, 0.000000001, 350)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_schafferF6_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING SCHAFFER F6 FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_schafferF6(n)
            real_optimum = [0 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.1):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

def single_schafferF7(n):
    SchafferF7Space.n_dimensions = n
    SchafferF7Space.up_bound = 100
    SchafferF7Space.low_bound = -100
    SchafferF7Space.eps = 0.001
    playground_obj = Playground(1000, 14, SchafferF7Space, 5000, 68, 0.1e-10, 0.1e-25, 500)
    start = time.time()
    playground_obj.matchday_search(12)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)
    optimum = copy.deepcopy(playground_obj.get_optimum())
    return [optimum.attribute.x, optimum.get_criteria()]

def test_schafferF7_table(p, q):
    dimensions = p
    n_searches = q
    search_results = []
    print('******************************* RUNNING SCHAFFER F7 FUNCTION TESTS *************************************')
    for n in dimensions:
        print('---->>>>---->>>>---->>>>---->>>>---- DIMENSIONS= ', n, ' ----<<<<----<<<<----<<<<----<<<<----')
        n_optimums_found = 0
        for i in range(1, n_searches+1):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            optimum = single_schafferF7(n)
            real_optimum = [0 for k in range(n)]
            if validate_optimum(optimum[0], real_optimum, 0.1):
                print('The real optimum has been found!')
                n_optimums_found += 1
            else:
                print('This is not the real optimum!')
            print('-------------------------------------------------------------------------------------------')
        print('***************************************************************************************************')
        search_results.append(n_optimums_found)
    return search_results

# test a single n-dimensional Rastrigin function
def single_rosenbrock(n):
    RosenbrockSpace.n_dimensions = n
    RosenbrockSpace.up_bound = 2.048
    RosenbrockSpace.low_bound = -2.048
    RosenbrockSpace.eps = 0.01
    playground_obj = Playground(300, 17, RosenbrockSpace, 5000, 17, 0.00000001, 0.00000001, 50)
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


def main():
    workbook = xlsxwriter.Workbook('rosenbrock_date15_05.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 2, 10)
    worksheet.set_column(3, 3, 13)
    curr_row = 0

    dimensions = [6]
    n_searches = 3

    # Rastrigin
    #results = test_rastrigin_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Rastrigin', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Schwefel
    #results = test_schwefel_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Schwefel', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Griewangk
    #results = test_griewank_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Griewank', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Bohachevsky - only valid dimension is 2!
    #results = test_bohachevsky_table([2], n_searches)
    #curr_row = add_header_to_table(worksheet, 'Bohachevsky', curr_row)
    #curr_row = add_results_to_table(worksheet, [2], results, n_searches, curr_row)

    # Schaffer F6 - only valid dimension is 2!
    #results = test_schafferF6_table([2], n_searches)
    #curr_row = add_header_to_table(worksheet, 'Schaffer F6', curr_row)
    #curr_row = add_results_to_table(worksheet, [2], results, n_searches, curr_row)

    # Schaffer F7
    #results = test_schafferF7_table(dimensions, n_searches)
    #curr_row = add_header_to_table(worksheet, 'Schaffer F7', curr_row)
    #curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    # Rosenbrock
    results = test_rosenbrock_table(dimensions, n_searches)
    curr_row = add_header_to_table(worksheet, 'Rosenbrock', curr_row)
    curr_row = add_results_to_table(worksheet, dimensions, results, n_searches, curr_row)

    workbook.close()


main()
