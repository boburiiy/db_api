# psql.py (new version, replacing the original pure Python one)

"""
This module provides a Python interface to a PostgreSQL database,
backed by a C++ implementation for performance.
It aims to be a drop-in replacement for the original psql.py.
"""

# Try to import the C++ core extension.
# The actual name of the .so/.pyd file will depend on the build system.
# We assume the Pybind11 module was named 'psql_cpp'.
try:
    # Attempt to import the DB class and the custom Error exception
    # (which PsqlCppException was bound to) from the C++ extension.
    from .psql_cpp import DB, Error as PsqlCppError

except ImportError as e:
    original_msg = str(e)
    # Provide a more helpful error message if the C++ module is not found.
    if "psql_cpp" in original_msg or "No module named 'psql_cpp'" in original_msg or "No module named '.psql_cpp'" in original_msg :
        raise ImportError(
            f"Failed to import the C++ database extension module '.psql_cpp'. "
            f"Please ensure it has been compiled and is accessible in the same package. "
            f"Original error: {original_msg}"
        )
    else:
        # Re-raise if it's some other import error (e.g., an issue *within* the C++ module during its import).
        raise

# Define what gets imported with 'from psql import *'
__all__ = ['DB', 'PsqlCppError']

# Optional: A simple test block for when the script is run directly.
if __name__ == '__main__':
    print("psql.py (C++ backed wrapper) loaded.")
    print("Available exports: DB class and PsqlCppError exception.")
    print("To use: from psql import DB, PsqlCppError")
    print("\nExample usage (requires PostgreSQL server and compiled C++ module):")
    print("try:")
    print("    db = DB(dbname='your_db', user='your_user', passwd='your_password', host='localhost')")
    print("    # Further operations like db.create_table(...), db.insert(...), etc.")
    print("    print('Successfully initialized DB object if C++ module is functional and DB is accessible.')")
    print("except PsqlCppError as e:")
    print(f"    A PsqlCppError occurred: {e}")
    print("except ImportError as e:")
    print(f"    ImportError: {e}")
    print("except Exception as e:")
    print(f"    An unexpected error occurred: {e}")
