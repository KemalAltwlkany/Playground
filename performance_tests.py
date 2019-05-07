import xlsxwriter
from T_rastrigin import *
from T_Schwefel import *

def add_to_results(worksheet, results):
    col = 0
    for i in range(1, len(results[1])+1):
        worksheet.write(i+1, col, i)
        worksheet.write(i+1, col+1, results[0])
        worksheet.write(i+1, col+2, results[1][i-1])
        worksheet.write(i+1, col+3, results[1][i-1]/results[0])


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


# for loop defines which dimensional rastrigin functions are tested
def test_multiple_rastrigins():
    print('******************************* RUNNING RASTRIGIN FUNCTION TESTS *************************************')
    for i in range(1, 3):
        print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
        optimum = single_rastrigin(i)
        real_optimum = [0 for k in range(i)]
        if validate_optimum(optimum[0], real_optimum, 0.05):
            print('The real optimum has been found!')
        else:
            print('This is not the real optimum!')
        print('-------------------------------------------------------------------------------------------')
    print('*****************************************************************************************************')

def test_rastrigin_table():
    max_dimensions = 4
    n_searches = 2
    search_results = []
    print('******************************* RUNNING RASTRIGIN FUNCTION TESTS *************************************')
    for n in range(1, max_dimensions+1):
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
    return [n_searches, search_results]


# test a single n-dimensional Schwefel function
def single_schwefel(n):
    SchwefelSpace.n_dimensions = n
    SchwefelSpace.up_bound = 500
    SchwefelSpace.low_bound = -500
    SchwefelSpace.eps = 5
    playground_obj = Playground(200, 6, SchwefelSpace, 5000, 30, 0.0001, 0.0001, 200)
    start = time.time()
    playground_obj.matchday_search(3)
    end = time.time()
    print("The matchday algorithm ran for, t = ", end - start)

# for loop defines which dimensional schwefel functions are tested
def test_multiple_schwefels():
    print('******************************* RUNNING SCHWEFEL FUNCTION TESTS *************************************')
    for i in range(1, 21):
        print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
        single_schwefel(i)
        print('-------------------------------------------------------------------------------------------')
    print('*****************************************************************************************************')

def main():
    workbook = xlsxwriter.Workbook('performance_tests_08_05.xlsx')
    worksheet = workbook.add_worksheet()
    func_number = 1
    worksheet.write(0, 0, 'Rastrigin')
    worksheet.write(1, 0, 'Dimensions')
    worksheet.write(1, 1, 'N searches')
    worksheet.write(1, 2, 'N correct')
    worksheet.write(1, 3, 'Percentage')
    # Rastrigin
    results = test_rastrigin_table()
    add_to_results(worksheet, results)
    func_number += 1
    workbook.close()


main()
