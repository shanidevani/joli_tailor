{
    'name': "Automatic Database Backup",
    'version': '16.0.1.0.0',
    'summary': """Generate automatic backup of databases and store to local, and google drive""",
    'description': """This module has been developed for creating database backups automatically 
                    and store it to the different locations.""",
    'author': "shani",
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/db_backup_configure_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
