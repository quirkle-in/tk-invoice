import json
import os
from gui.main_window import MainWindow
from models import Base, engine

default_settings = {
                    "pdf_title": "Change this value in Settings",
                    "pdf_address": "Change this value in Settings",
                    "pdf_gst_no": "Change this value in Settings",
                    "cgst": "6",
                    "sgst": "1",
                    "igst": "6",
                    "state": "Change this value in Settings",
                    "default_save_folder": os.path.abspath(os.curdir)
                }

if __name__ == "__main__":

    if not engine.dialect.has_table(engine, 'Invoice'):
        # print('Creating tables')
        Base.metadata.create_all(bind=engine)
    else:
        # print('Table Exists')
        pass

    try:
        with open("settings.json", 'rw') as json_file:
            settings = json_file.read()
            for default in default_settings:
                if default not in settings:
                    settings[default] = default_settings[default]
            try:
                json.dump(settings, json_file)
            except Exception as e:
                print(e)
    except:
        with open("settings.json", 'w') as json_file:
                json.dump(default_settings, json_file)

    MainWindow()
