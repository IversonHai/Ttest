{
     'name': 'Multiuser To-Do',
     'description': 'Extend the To-Do app to multiuser.',
     'author': 'Daniel Reis',
     'depends': ['todo_app'],
     'data':
          [
          'views/todo_task.xml',
          'security/todo_access_rules.xml',
     ],
     'demo': ['security/todo.task.csv',
              'security/todo_data.xml',],
}