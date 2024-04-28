from funcs import LENGTH, find_data_for_karnaugh_map, find_j_k_triggers_exits, make_postproc, print_map


if __name__ == "__main__":
    nums = list(map(lambda x: bin(int(x))[2:].rjust(LENGTH, '0'), input('Введите числа через пробел').split()))
    map_data_j, map_data_k = find_data_for_karnaugh_map(nums)
    exit_j, exit_k = find_j_k_triggers_exits(nums, map_data_j, map_data_k)

    for trigger_name in ('j', 'k'):
        exit_var = locals()[f'exit_{trigger_name}']
        map_data = locals()[f'map_data_{trigger_name}']

        for i in range(LENGTH):
            print(f'{trigger_name}_{i}:'.upper())
            print_map(nums, map_data[LENGTH - i - 1])
            print(f'ДНФ для {trigger_name}_{i}: {make_postproc(exit_var[LENGTH - i - 1])}')
        print()
