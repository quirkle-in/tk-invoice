import json
import os
from gui.main_window import MainWindow
from models import Base, engine


if __name__ == "__main__":

    if not engine.dialect.has_table(engine, 'Invoice'):
        # print('Creating tables')
        Base.metadata.create_all(bind=engine)
    else:
        # print('Table Exists')
        pass

    try:
        with open("settings.json", 'r') as json_file:
            settings = json_file.read()
            json_file.close()
    except:
        with open("settings.json", 'w') as json_file:
                json.dump({
                    "cgst": "",
                    "sgst": "1",
                    "igst": "",
                    "state": "",
                    "default_save_folder": os.path.abspath(os.curdir)
                }, json_file)

    MainWindow()
