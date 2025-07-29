import os
from faker import Faker

fake = Faker()


def create_files_and_directories(base_dir, depth, num_dirs, num_files_per_dir):
    if depth == 0:
        return

    for i in range(num_dirs):
        dir_name = fake.word()
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

        create_files_and_directories(dir_path, depth - 1, num_dirs, num_files_per_dir)

        for j in range(num_files_per_dir):
            file_name = f"{fake.word()}.{fake.file_extension()}"
            file_path = os.path.join(dir_path, file_name)

            with open(file_path, "w") as f:
                f.write(fake.text())


base_directory = "src_dir"
depth_of_recursion = 3
number_of_directories = 3
number_of_files_per_directory = 5

create_files_and_directories(
    base_directory,
    depth_of_recursion,
    number_of_directories,
    number_of_files_per_directory,
)
