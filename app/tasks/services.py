

class TaskModelService:

    def json(self):
        '''
        This method returns the current task in JSON format
        '''
        #TODO: modify it so that it returns the children as well
        return{
            'task_id': self.task_id,
            'task_title': self.task_title,
            'task_description': self.task_description,
            'time_from': self.time_form,
            'time_to': self.time_to,
            'time_started': self.time_started,
            'is_completed': self.is_completed,
            'repeat': self.repeat,
            'reminder': self.reminder,
            'list_id': self.list_id,
            'color_id': self.color_id,
            'user_id': self.user_id,
            'parent_event_id': self.parent_event_id,
            'parent_task_id': self.parent_task_id
        }

    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current task to the database.
        If the task already exists it will update it.
        '''
        #TODO: implement this method
        pass

    def update_in_db(self):
        '''
        This method updates the current task in the DB.
        If the task does not exit in the DB it will save it.
        '''
        #TODO: implement this method
        pass

    def delete_from_db(self):
        '''
        This method deletes the currnet task from the database.
        If the task doesn't exist it will do nothing
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_by_task_id(self, task_id):
        '''
        This method searchs the DB for a task with the given task_id.
        If nothing could be found it will return None.
        '''
        #TODO: implement this method
        pass

    @classmethod
    def find_tasks_by_parent_task_id(self, parent_task_id):
        '''
        This methods searchs the DB for tasks that have the task with the given id as a parent and returns them in a list.
        If nothing could be found, it will return an empty list
        '''
        #TODO: implement this method
        pass

    @classmethod 
    def find_tasks_by_parent_event_id(self, parent_event_id):
        '''
        This method searchs the DB for the tasks that have the event with the given id as a parent and return them in the form of a list.
        If nothing could be found it will return an empty list.
        '''
        #TODO: implement this method
        pass

    #endregion


class TasksListModelService:

    def json(self):
        '''
        This method return the object in JSON format
        '''
        #TODO: a second thougt
        return {
            'list_id': self.list_id,
            'list_title': self.list_title
        }
    #region DB methods

    def save_to_db(self):
        '''
        This method saves the current TasksList to the database.
        If the Tasks List already exists it will just update it.
        '''
        if self.find_by_list_id(self.list_id):
            self.update_in_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        INSERT INTO TasksLists VALUES (NULL, ?);
                        """
                curser.execute(query, (
                    self.list_title,
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.add(self)
                db.session.commit()

    def update_in_db(self):
        '''
        This method will update the current TasksList in the database with its current values.
        If the TasksList does not exist in the database it will save it.
        '''
        if not self.find_by_list_id(self.list_id):
            self.save_to_db()
        else:
            if app.app.config['DEBUG']:
                connection = sqlite3.Connection(db_url)
                curser = connection.cursor()

                query = """
                        UPDATE TasksLists
                        SET list_title = ?
                        WHERE list_id = ?;
                        """
                curser.execute(query, (
                    self.list_title,
                    self.list_id
                    )
                )

                connection.commit()
                connection.close()
            else:
                db.session.commit()

    def delete_from_db(self):
        '''
        This method will delete the TasksList and its tasks from the database only if it exists.
        '''
        if find_by_list_id(self.color_id):
            if app.app.config['DEBUG']:
                #TODO: delete the tasks the belong to this tasks list
                connection = sqlite3.connect(db_url)
                curser = connection.cursor()

                query = 'DELETE FROM TasksLists WHERE list_id = ?;'
                curser.execute(query, (self.list_id,))

                connection.commit()
                connection.close()
            else:
                 #TODO: delete the tasks the belong to this tasks list
                db.session.delete(self)
                db.session.commit()

    @classmethod
    def find_by_list_id(cls, list_id):
        '''
        This method searchs the database for a list with the given list id.
        If the list does not exist it will return None.
        '''
        if app.app.config['DEBUG']:
            connection = sqlite3.Connection(db_url)
            curser = connection.cursor()

            query = 'SELECT * FROM TasksLIsts WHERE list_id = ?;'

            result = curser.execute(query, (list_id,))
            row = result.fetchone()
            if row:
                new_list = cls(*row)
            else:
                new_list = None

            connection.close()
            return new_list

        else:
            return cls.query.filter_by(list_id = list_id).first()

    #endregion