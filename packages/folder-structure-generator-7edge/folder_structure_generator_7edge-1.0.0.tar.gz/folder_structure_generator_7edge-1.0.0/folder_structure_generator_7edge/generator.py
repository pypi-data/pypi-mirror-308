import os
from InquirerPy import inquirer

def create_service_structure():
    service_name = inquirer.text(message="Enter the service name:").execute()
    language_choice = inquirer.select(
        message="Select the programming language:",
        choices=["Python", "Node.js"]
    ).execute()

    file_extension = "py" if language_choice == "Python" else "js"

    base_dir = f"services/{service_name}"
    folders = [
        f"{base_dir}/.serverless",
        f"{base_dir}/entities",
        f"{base_dir}/handlers"
    ]

    handler_files = ["add", "list", "view", "update", "delete"]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    for file_name in handler_files:
        file_path = os.path.join(base_dir, "handlers", f"{file_name}.{file_extension}")
        with open(file_path, 'w') as file:
            file.write(f"# {file_name} handler\n")
        print(f"Created file: {file_path}")

    additional_files = [
        f"{base_dir}/.env",
        f"{base_dir}/bank-management-swagger.json",
        f"{base_dir}/dredd.yml",
        f"{base_dir}/hooks.{file_extension}",
        f"{base_dir}/serverless.yml"
    ]

    for file_path in additional_files:
        with open(file_path, 'w') as file:
            file.write(f"# {os.path.basename(file_path)} file\n")
        print(f"Created file: {file_path}")
