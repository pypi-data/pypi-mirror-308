import os
from pathlib import Path

def main():
    print("Welcome to Instigator CLI!")
    # Step-by-step prompts
    project_name = input("Project name (e.g., My Project): ") or "My Project"
    project_slug = input(f"Project slug ({project_name.lower().replace(' ', '_')}): ") or project_name.lower().replace(' ', '_')
    author_name = input("Author name: ") or "Your Name"
    version = input("Version (1.0): ") or "1.0"
    description = input("Description: ") or "An amazing project."
    # Add more questions as per requirement

    # Create project structure
    project_dir = Path(project_slug)
    project_dir.mkdir(exist_ok=True)
    with open(project_dir / "README.md", "w") as readme:
        readme.write(f"# {project_name}\n\n{description}\n")

    print(f"Project '{project_name}' created successfully in '{project_slug}'.")

if __name__ == "__main__":
    main()
