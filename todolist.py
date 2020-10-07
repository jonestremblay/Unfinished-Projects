from _datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "%s|%s|%s\n" % (self.id, self.task, self.deadline)


# metadata = MetaData()
# # Define table
# task = Table('task', metadata,
#              Column('id', Integer, primary_key=True),
#              Column('task', String),
#              Column('deadline', Date, default=datetime.today()))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()


def concatenate_to_do_list(todo_list):
    """
    :param todo_list: Database's list
    :return: A formatted to-do list, and return the number of tasks
    """
    temp_list = ""
    p = 0
    for i in to_do_list:
        p += 1
        temp_list += (str(p) + ") " + str(i).split('|')[1] + "\n")   # i.e   p) Make breakfast
    return temp_list, p + 1


def get_new_task_id() -> int:
    """
    Find the id number of the last task, increment and return it.
    :return: Next ID number for task
    """
    return 0


choice = int
while choice != 0:
    task_list = session.query(Table).all()
    to_do_list = []
    for i in task_list:
        to_do_list.append(i)
    choice = int(input("1) Today\'s tasks\n2) Add task\n0) Exit\n"))
    if choice == 1:     # Today's task
        print("\nToday:")
        if not to_do_list:  # Checks if the list is empty.
            print("Nothing to do!\n")
        else:
            print(concatenate_to_do_list(to_do_list))
        print(concatenate_to_do_list(to_do_list)[0])
        continue
    elif choice == 2:   # Add task
        task = input("\nEnter task\n")
        n = concatenate_to_do_list(to_do_list)[1]
        new_task_to_add = Table(id=n, task=task)
        session.add(new_task_to_add)
        session.commit()
        print("The task has been added!\n")
        continue
    elif choice == 0:   # Exit
        print("Bye!")
        exit()
