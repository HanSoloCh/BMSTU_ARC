from Kmap import make_karnaugh

EXIT_SYMB = 'q'

LENGTH = 4
TRIGGERS_COUNT = 4

REPLACE_PATTERNS = {0: 'q3', 1: 'q2', 2: 'q1', 3: 'q0'}


def print_map(enter_num, results):
    bin_karnaugh_data = ('00', '01', '11', '10')
    print('    | 00 | 01 | 11 | 10 |')
    for bin_num_i in bin_karnaugh_data:
        print(f' {bin_num_i} |', end='')
        for bin_num_j in bin_karnaugh_data:
            if f'{bin_num_j}{bin_num_i}' in enter_num:
                index = enter_num.index(f'{bin_num_j}{bin_num_i}')
                print(f'  {results[index]} |', end='')
            else:
                print(f' -- |', end='')
        print()


def preproc_data(bin_nums: list[str], bool_data: list[str]) -> dict[str, list[str]]:
    res_dict = {'terms': [], 'dont_cares': list()}
    zero_data = list()
    for i in range(len(bin_nums)):
        if bool_data[i] == '1':
            res_dict['terms'].append(bin_nums[i])
        elif bool_data[i] == '0':
            zero_data.append(bin_nums[i])

    for i in range(2 ** LENGTH):
        bin_x = bin(i)[2:].rjust(LENGTH, '0')
        if bin_x not in res_dict['terms'] and bin_x not in zero_data:
            res_dict['dont_cares'].append(bin_x)

    return res_dict


def replace_symbols(str_data):
    res = []
    for i, symbol in enumerate(list(str(str_data))):
        if symbol == '0':
            res.append('-' + REPLACE_PATTERNS[i])
        elif symbol == '1':
            res.append(REPLACE_PATTERNS[i])

    res = '*'.join(res)
    return res if len(res) else '1'


def make_postproc(dnf_lst):
    res: str
    if dnf_lst is None:
        res = '0'
    else:
        res = '+'.join([replace_symbols(dnf) for dnf in dnf_lst])
    return res


def find_data_for_karnaugh_map(nums):
    nums_extra = nums[1:] + [nums[0]]

    exit_j = list()
    exit_k = list()

    for i in range(len(nums)):
        exit_j.append([])
        exit_k.append([])
        for j in range(LENGTH):
            if nums[i][j] == '0':
                res_j = '0' if nums_extra[i][j] == '0' else '1'
                res_k = 'a'
            else:
                res_j = 'a'
                res_k = '1' if nums_extra[i][j] == '0' else '0'

            exit_j[i].append(res_j)
            exit_k[i].append(res_k)

    return list(zip(*exit_j)), list(zip(*exit_k))


def find_j_k_triggers_exits(nums, karnaugh_data_j, karnaugh_data_k):
    karnaugh_data_for_exit_j = [preproc_data(nums, j_i) for j_i in karnaugh_data_j]
    karnaugh_data_for_exit_k = [preproc_data(nums, k_i) for k_i in karnaugh_data_k]

    dnf_func_for_exit_j = [
        make_karnaugh(karnaugh_data_for_exit_j[i]['terms'], karnaugh_data_for_exit_j[i]['dont_cares'])
        for i in range(LENGTH)]

    dnf_func_for_exit_k = [
        make_karnaugh(karnaugh_data_for_exit_k[i]['terms'], karnaugh_data_for_exit_k[i]['dont_cares'])
        for i in range(LENGTH)]

    return dnf_func_for_exit_j, dnf_func_for_exit_k