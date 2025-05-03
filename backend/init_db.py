"""
Initialize the database by running the schema creation and data generation scripts.
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and check its result"""
    print(f"{description}...")
    result = subprocess.run(["py", command], cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        print(f"Error: {description} failed with return code {result.returncode}")
        sys.exit(1)
    return result

print("Initializing database...")

# Run create_db.py to create the schema
run_command("create_db.py", "Creating database schema")

# Run generate_data.py to populate with all data
run_command("generate_data.py", "Populating database with data")

print("Database initialization complete!")
print("You can now start the API server with: uvicorn app:app --reload") 