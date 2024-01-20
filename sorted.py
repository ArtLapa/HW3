import os
import shutil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import unittest

def process_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files

def move_file(file_path, destination_folder):
    _, extension = os.path.splitext(file_path)
    destination_path = os.path.join(destination_folder, extension[1:], os.path.basename(file_path))
    shutil.move(file_path, destination_path)

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_all(numbers):
    with ProcessPoolExecutor() as executor:
        return list(executor.map(factorize, numbers))

def sort_files(files):
    return sorted(files)

class TestParallelFunctions(unittest.TestCase):

    def setUp(self):
        self.source_folder = "TestFolder"
        self.destination_folder = "SortedFolder"
        self.num_threads = 2
        self.num_processes = 2

        if not os.path.exists(self.source_folder):
            os.makedirs(self.source_folder)

        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)

        # Create some test files in the source folder
        for i in range(10):
            open(os.path.join(self.source_folder, f"file{i}.txt"), 'w').close()

    def tearDown(self):
        shutil.rmtree(self.source_folder)
        shutil.rmtree(self.destination_folder)

    def test_file_sorting(self):
        files_to_sort = process_folder(self.source_folder)
        sorted_files = sort_files(files_to_sort)
        self.assertEqual(sorted_files, sorted(files_to_sort))

    def test_file_moving(self):
        files_to_move = process_folder(self.source_folder)
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(move_file, file_path, self.destination_folder) for file_path in files_to_move]

        # Wait for all the file-moving tasks to complete
        for future in futures:
            future.result()

        files_in_destination = process_folder(self.destination_folder)
        self.assertEqual(len(files_in_destination), len(files_to_move))

    def test_factorization(self):
        numbers_to_factorize = [128, 256, 512, 1024, 2048]
        result_factorize = factorize_all(numbers_to_factorize)

        expected_factors = [[1, 2, 4, 8, 16, 32, 64, 128],
                            [1, 2, 4, 8, 16, 32, 64, 128, 256],
                            [1, 2, 4, 8, 16, 32, 64, 128, 256, 512],
                            [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024],
                            [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]]

        for i in range(len(numbers_to_factorize)):
            self.assertEqual(result_factorize[i], expected_factors[i])

if __name__ == "__main__":
    unittest.main()


