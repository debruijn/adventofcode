example_run = False
debug = False

file = 'aoc_7_exampledata' if example_run else 'aoc_7_data'
with open(file) as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]

list_of_files = {}
curr_folder = []
for row in adj_data:
    if debug:
        print('      ' + row)
    if row.startswith('$ cd'):
        folder_change = row.split('$ cd ')[1]
        if folder_change == '/':
            curr_folder = []
        elif folder_change == '..':
            curr_folder.pop()
        else:
            curr_folder.append(folder_change)
        if debug:
            print(curr_folder)
    elif not (row.startswith('$') or row.startswith('dir')):
        contents = row.split(' ')
        list_of_files.update({'/'.join(curr_folder) + '/' + contents[1]: int(contents[0])})
        if debug:
            print('/'.join(curr_folder) + '/' + contents[1])

if debug:
    print(list_of_files)

# WRONG: does not construct folders that don't have a file directly in them
# list_of_folders = ['/'.join(x.split('/')[:-1]) for x in list_of_files.keys()]
# list_of_folders_bu = list(set(list_of_folders))

# CORRECT: create all subfolders for every file (and take set of folders to remove duplicates)
list_of_folders = []
for file in list_of_files.keys():
    split = file.split('/')
    curr = ''
    for element in split[:-1]:
        curr += element + '/'
        list_of_folders.append(curr)
list_of_folders = list(set(list_of_folders) - set('/'))
list_of_folders.append('')

sum_of_sizes = 0
folder_sizes = {}
for folder in list_of_folders:
    size = 0
    for filename in list_of_files.keys():
        if filename.startswith(folder):
            size += list_of_files[filename]
    if debug:
        print(f'{folder}: {size}')
    folder_sizes.update({folder: size})
    if size <= 100000:
        sum_of_sizes += size

print(sum_of_sizes)

total_file_size = sum([list_of_files[x] for x in list_of_files])
minimum_remove = 30000000 - (70000000 - total_file_size)

print(min(v for k, v in folder_sizes.items() if v > minimum_remove))
