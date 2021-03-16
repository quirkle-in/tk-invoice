import json
import os
from gui.main_window import MainWindow
from models import Base, engine

default_settings = {
                    "pdf_title": "Rajeshree Marketing",
                    "pdf_address": "1/16, Vijay Nagar, Bandrekarwadi, Jogeshwari (East), Mumbai 400060.",
                    "pdf_gst_no": "27AKEPB0058K1ZE",
                    "sgst": "12",
                    "cgst": "6",
                    "igst": "6",
                    "state": "Maharashtra",
                    "default_save_folder": os.path.join(os.environ["HOMEPATH"], "Desktop"),
                    "theme": "breeze"
                }

if __name__ == "__main__":

    if not engine.dialect.has_table(engine, 'Invoice'):
        # print('Creating tables')
        Base.metadata.create_all(bind=engine)
    else:
        # print('Table Exists')
        pass

    settings = None
    try:
        with open("settings.json", 'r') as json_file:
            try:
                settings = json.load(json_file)
                for default in default_settings:
                    if default not in settings:
                        settings[default] = default_settings[default]
            except:
                pass
        with open("settings.json", "w") as json_file:
            try:
                json.dump(settings, json_file)
            except Exception as e:
                print(e)
    except Exception as e:
        with open("settings.json", 'w') as json_file:
                json.dump(default_settings, json_file)

    MainWindow()
