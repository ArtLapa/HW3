import os
import shutil
from concurrent.futures import ThreadPoolExecutor
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

def main(source_folder, destination_folder, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Step 1: Process the source folder and get the list of files
        files = process_folder(source_folder)

        # Step 2: Move each file to the destination folder in parallel
        futures = [executor.submit(move_file, file_path, destination_folder) for file_path in files]

        # Wait for all the tasks to complete
        for future in futures:
            future.result()

    # Step 3: Factorize numbers in a synchronous manner
    numbers_to_factorize = [128, 256, 512, 1024, 2048]
    start_time_factorize = time.time()
    result_factorize = factorize_all(numbers_to_factorize)
    end_time_factorize = time.time()

    print("Factors:")
    for factors in result_factorize:
        print(factors)

    print("Time taken for factorization: {:.4f} seconds".format(end_time_factorize - start_time_factorize))

if __name__ == "__main__":
    source_folder = "Хлам"  # Ваша вхідна папка
    destination_folder = "Сортовано"  # Папка, куди будуть переміщені файли
    num_threads = 4  # Кількість потоків для паралельного обробки

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    start_time_main = time.time()
    main(source_folder, destination_folder, num_threads)
    end_time_main = time.time()

    print("Time taken for main program: {:.4f} seconds".format(end_time_main - start_time_main))
