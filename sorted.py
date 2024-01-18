import os
import shutil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

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
    result = []
    for number in numbers:
        result.append(factorize(number))
    return result

def sort_files(files):
    return sorted(files)

def main(source_folder, destination_folder, num_threads, num_processes):
    with ThreadPoolExecutor(max_workers=num_threads) as thread_executor:
        # Step 1: Process the source folder and get the list of files
        files = process_folder(source_folder)

        # Step 2: Move each file to the destination folder in parallel using threads
        futures_move = [thread_executor.submit(move_file, file_path, destination_folder) for file_path in files]

        # Wait for all the file-moving tasks to complete
        for future in futures_move:
            future.result()

    with ProcessPoolExecutor(max_workers=num_processes) as process_executor:
        # Step 3: Factorize numbers in parallel using processes
        numbers_to_factorize = [128, 256, 512, 1024, 2048]
        futures_factorize = [process_executor.submit(factorize, number) for number in numbers_to_factorize]

        # Wait for all the factorization tasks to complete
        result_factorize = [future.result() for future in futures_factorize]

        print("Factors:")
        for factors in result_factorize:
            print(factors)

    with ThreadPoolExecutor(max_workers=num_threads) as thread_executor:
        # Step 4: Sort files in parallel using threads
        futures_sort = [thread_executor.submit(sort_files, files)]

        # Wait for the file sorting task to complete
        sorted_files = futures_sort[0].result()

        print("Sorted Files:")
        for file_path in sorted_files:
            print(file_path)

if __name__ == "__main__":
    source_folder = "Хлам"  # Ваша вхідна папка
    destination_folder = "Сортовано"  # Папка, куди будуть переміщені файли
    num_threads = 4  # Кількість потоків для паралельного обробки
    num_processes = 2  # Кількість процесів для паралельного обробки

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    start_time_main = time.time()
    main(source_folder, destination_folder, num_threads, num_processes)
    end_time_main = time.time()

    print("Time taken for main program: {:.4f} seconds".format(end_time_main - start_time_main))

