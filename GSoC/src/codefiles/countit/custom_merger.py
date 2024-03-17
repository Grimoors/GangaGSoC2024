

import sys

def merge(file_list_txt, output_file):
    #read the content of the file
    file_list = []
    print(type(file_list_txt[0]))
    print(file_list_txt[0])
    with open(file_list_txt[0], 'r') as f_in:
        # read the file paths from the file
        file_paths = f_in.read().strip().split('\n')
        # append the file path to the list
        file_list.extend(file_paths)

    # import pickle
    # file_list = pickle.load(open(file_list_pickle, 'rb'))
    total_count = 0
    for file_path in file_list:
        with open(file_path, 'r') as f_in:
            count = int(f_in.read().strip())
            total_count += count
    with open(output_file, 'w') as f_out:
        f_out.write(str(total_count))

if __name__ == "__main__":
    file_list    = sys.argv[1:-1]
    print(type(file_list))
    output_file = sys.argv[-1]
    merge(file_list, output_file)


