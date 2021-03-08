
from gui.main_window import MainWindow
from models import Base, engine


if not engine.dialect.has_table(engine, 'Invoice'):
    print('Creating tables')
    Base.metadata.create_all(bind=engine)
else:
    print('Table Exists')


if __name__ == "__main__":
    MainWindow()
