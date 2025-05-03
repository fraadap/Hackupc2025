
"""
Fix for the SQL query issue in app.py for the cities/evaluation endpoint.

The issue is with the query:
cursor.execute("SELECT name FROM City WHERE name NOT IN ({})".format(
    ','.join('?' for _ in voted_cities) if voted_cities else "''"),
voted_cities if voted_cities else [])

When voted_cities is empty, it generates: SELECT name FROM City WHERE name NOT IN ('')
which is invalid SQL syntax.

This script creates a backup of app.py and fixes the issue.
"""

import os
import re
import datetime
import shutil

def fix_cities_evaluation_endpoint():
    app_py_path = "app.py"
    
    # Check if the file exists
    if not os.path.exists(app_py_path):
        print(f"Error: {app_py_path} not found in the current directory.")
        return False
    
    # Create a backup
    backup_path = f"app.py.backup.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    try:
        shutil.copy2(app_py_path, backup_path)
        print(f"Created backup at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return False
    
    # Read the file contents
    with open(app_py_path, 'r') as f:
        content = f.read()
    
    # The pattern to look for
    pattern = re.compile(r'cursor\.execute\("SELECT name FROM City WHERE name NOT IN \(\{\}\)"\.format\((.*?)\),\s*(.*?)\)')
    
    # The replacement - a better approach handling empty voted_cities
    replacement = """if voted_cities:
        # If the user has voted on cities, exclude them
        placeholders = ','.join('?' for _ in voted_cities)
        cursor.execute(f"SELECT name FROM City WHERE name NOT IN ({placeholders})", voted_cities)
    else:
        # If the user hasn't voted on any cities, get all cities
        cursor.execute("SELECT name FROM City")"""
    
    # Find the pattern and replace
    new_content = pattern.sub(replacement, content)
    
    # Check if any replacement was made
    if new_content == content:
        print("Warning: Could not find the pattern to replace. The file might already be fixed or has a different structure.")
        return False
    
    # Write the updated content back to the file
    try:
        with open(app_py_path, 'w') as f:
            f.write(new_content)
        print(f"Successfully updated {app_py_path} with the fix.")
        print(f"The cities/evaluation endpoint should now handle empty voted_cities correctly.")
        return True
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        print(f"You can still use the backup at {backup_path}")
        return False

def main():
    print("="*80)
    print("Fixing SQL query issue in app.py for the cities/evaluation endpoint")
    print("="*80)
    
    success = fix_cities_evaluation_endpoint()
    
    if success:
        print("\n✅ Fix applied successfully!")
        print("You should restart your FastAPI server for the changes to take effect:")
        print("   uvicorn app:app --reload")
    else:
        print("\n❌ Fix could not be applied.")
        print("You might need to manually update the SQL query in app.py.")
        print("The correct implementation should be:")
        print("""
    # Get cities not yet voted
    if voted_cities:
        # If the user has voted on cities, exclude them
        placeholders = ','.join('?' for _ in voted_cities)
        cursor.execute(f"SELECT name FROM City WHERE name NOT IN ({placeholders})", voted_cities)
    else:
        # If the user hasn't voted on any cities, get all cities
        cursor.execute("SELECT name FROM City")
        """)
    
    print("="*80)

if __name__ == "__main__":
    main() 