from ..shared.db_man.service import db
from .interfaces import TaskModelInterface, TasksListModelInterface


class TaskModel(db.Model):
    __tablename__ = "Tasks"

    # region SQLAlchemy table columns

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    task_title = db.Column(db.String(50), nullable=False)

    task_description = db.Column(db.String(250), nullable=True, default=None)

    time_form = db.Column(db.String(100), nullable=False)

    time_to = db.Column(db.String(100), nullable=False)

    time_started = db.Column(db.String(100), nullable=False)

    time_finished = db.Column(db.String(100), nullable=False)

    is_completed = db.Column(db.Boolean, nullable=True, default=0)

    repeat = db.Column(db.String(100), nullable=True, default=None)

    reminder = db.Column(db.String(100), nullable=True, default=None)

    list_id = db.Column(db.Integer, db.ForeignKey("TasksLists.list_id"), nullable=False)

    color_id = db.Column(db.Integer, db.ForeignKey("Colors.color_id"), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)

    parent_event_id = db.Column(
        db.Integer, db.ForeignKey("Events.event_id"), nullable=True, default=None
    )

    parent_task_id = db.Column(
        db.Integer, db.ForeignKey("Events.event_id"), nullable=True, default=None
    )

    # endregion

    def update(self, task_attrs: TaskModelInterface):

        for key, value in task_attrs.items():
            setattr(self, key, value)
        return self


class TasksListModel(db.Model):

    __tablename__ = "TasksLists"

    # region SQLAlchemy table columns

    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    list_title = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)

    # endregion

    def update(self, list_attrs: TasksListModelInterface):

        for key, value in list_attrs.items():
            setattr(self, key, value)
        return self