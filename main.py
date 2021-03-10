from gui.main_window import MainWindow
from models import Base, engine



if __name__ == "__main__":
    
    if not engine.dialect.has_table(engine, 'Invoice'):
        #print('Creating tables')
        Base.metadata.create_all(bind=engine)
    else:
        #print('Table Exists')
        pass

    try:
        with open("settings.json", 'r') as json_file:
            x = json_file.read()
            json_file.close()
    except:
        with open("settings.json", 'w') as json_file:
            json_file.write({})
            json_file.close()   
 
    MainWindow()

