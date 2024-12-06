import shutil
import os
import sys
from pathlib import Path
from .create_db import create_db

def get_config_dir():
    return Path('C:/ProgramData/Cytomat')

def setupt_config_dir():
    config_dir = get_config_dir()
    db_file = config_dir / 'slots.db'

    try: 
        if not config_dir.exists():
            os.mkdir(config_dir)
            print(f"Created: {config_dir}")
        else:
            print(f" allready exits: {config_dir}")

    except Exception as e:
        print(f"""  Path directory could not be created: {e}
                    -
                    Please Create manualy: {config_dir}""")
    try:
        if not db_file.exists():
            create_db(db_file)
            print(f"copied sample DataBase to: {db_file}")
        else:
            print(f"DataBase file allready exits: {db_file}")

    except Exception as e:
        print(f"""  Error: {e}
                    -
                    Please run funktion create_db(Path) in the program cytomat/scripts/create_db.py
                    -
                    choose the Path: 'C:/ProgrammData/Cytomat/slots.db'""")
        
def post_install():
    setupt_config_dir()

if __name__ == '__main__':
    post_install()