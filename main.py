import json
import os
from gui.main_window import MainWindow
from models import Base, engine

default_settings = {
                    "pdf_title": "Rajeshree Marketing",
                    "pdf_address": "1/16, Vijay Nagar, Bandrekarwadi, Jogeshwari (East), Mumbai 400060.",
                    "pdf_gst_no": "27AKEPB0058K1ZE",
                    "sgst": "6",
                    "cgst": "7",
                    "igst": "8",
                    "state": "Maharashtra",
                    "default_save_folder": os.path.join(os.environ["HOMEPATH"], "Desktop")
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
