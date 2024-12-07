import os
from InquirerPy import inquirer

def create_service_structure():
    try:
        # Prompt user for the service name
        service_name = inquirer.text(message="Enter the service name:").execute()
        if not service_name.strip():
            print("Error: Service name cannot be empty.")
            return

        # Prompt user for the programming language
        language_choice = inquirer.select(
            message="Select the programming language:",
            choices=["Python", "Node.js"]
        ).execute()

        # Determine file extension based on language choice
        file_extension = "py" if language_choice == "Python" else "js"

        # Define base directory for the service
        base_dir = f"services/{service_name.strip()}"
        
        # Define folder structure
        folders = [
            f"{base_dir}/.serverless",
            f"{base_dir}/entities",
            f"{base_dir}/handlers"
        ]

        # Define handler files
        handler_files = ["add", "list", "view", "update", "delete"]

        # Create directories
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder: {folder}")

        # Create handler files with boilerplate content
        for file_name in handler_files:
            file_path = os.path.join(base_dir, "handlers", f"{file_name}.{file_extension}")
            with open(file_path, 'w') as file:
                file.write(f"# {file_name.capitalize()} handler\n")
            print(f"Created file: {file_path}")

        # Additional files to be created
        additional_files = [
            f"{base_dir}/.env",
            f"{base_dir}/bank-management-swagger.json",
            f"{base_dir}/dredd.yml",
            f"{base_dir}/hooks.{file_extension}",
            f"{base_dir}/serverless.yml"
        ]

        # Create additional files with boilerplate content
        for file_path in additional_files:
            with open(file_path, 'w') as file:
                file.write(f"# {os.path.basename(file_path)} file\n")
            print(f"Created file: {file_path}")

        print("\nService structure generated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point for the script
if __name__ == "__main__":
    create_service_structure()
