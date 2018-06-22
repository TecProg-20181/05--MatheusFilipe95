import os
import re
import unittest
from diskspace import bytes_to_readable, subprocess_check_output, print_tree, show_space_list

class TestBytes_to_readable(unittest.TestCase):

    def test_subprocess_check_output(self):
        cmd = 'du '
        subprocess = subprocess_check_output(cmd)
        self.assertIsInstance(cmd, str)

    def test_bytes_to_readable(self):
        bytes = bytes_to_readable(2)
        self.assertEqual(bytes, '1.00Kb')
        self.assertIsNotNone(bytes)

    def test_print_tree(self):
        depth = -1
        order = True
        abs_directory = os.path.abspath('.')

        cmd = 'du '
        if depth != -1:
            cmd += '-d {} '.format(depth)

        cmd += abs_directory
        raw_output = subprocess_check_output(cmd)

        total_size = -1
        line_regex = r'(\d+)\s+([^\s]*|\D*)'

        file_tree = {}
        for line in re.findall(line_regex, raw_output.strip(), re.MULTILINE):
            file_path = line[-1]
            dir_path = os.path.dirname(file_path)

            file_size = int(line[0])

            if file_path == abs_directory:
                total_size = file_size

                if file_path in file_tree:
                    file_tree[file_path]['size'] = file_size
                else:
                    file_tree[file_path] = {
                        'children': [],
                        'size': file_size,
                    }

                continue

            if file_path not in file_tree:
                file_tree[file_path] = {
                    'children': [],
                    'size': file_size,
                }

            if dir_path not in file_tree:
                file_tree[dir_path] = {
                    'children': [],
                    'size': 0,
                }

            file_tree[dir_path]['children'].append(file_path)
            file_tree[file_path]['size'] = file_size

        largest_size = 0
        for file_path in file_tree:
            file_tree_entry = file_tree[file_path]
            file_tree_entry['children'] = sorted(
                file_tree_entry['children'],
                key=lambda v: file_tree[v]['size'],
                reverse=order
            )

            file_tree_entry['print_size'] = bytes_to_readable(
                file_tree_entry['size']
            )
            largest_size = max(largest_size, len(file_tree_entry['print_size']))

        self.assertNotIsInstance(print_tree(file_tree, file_tree[abs_directory], abs_directory,
                   largest_size, total_size), str)

    def test_show_space_list(self):
        self.assertIsNone(show_space_list(directory='.', depth=-1, order=True))

if __name__ == '__main__':
    unittest.main()
