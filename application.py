import paste.deploy

application = paste.deploy.loadapp('config:development.ini', relative_to='.')
