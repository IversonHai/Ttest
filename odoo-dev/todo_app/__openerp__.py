{
     'name': 'TO-DO Application',
     'description': 'Manage your personal Tasks with this module.',
     'author': 'Daniel Reis',
     'depends': ['mail'],
     'data':[
          'views/todo_view.xml',
          'security/ir.model.access.csv',
          'security/todo_access_rules.xml',
     ],
     'application': True,
}