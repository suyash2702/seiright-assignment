workers = 4
bind = "0.0.0.0:8000"

#Logs
errorlog = "/path/to/your/logs/gunicorn-error.log"
accesslog = "/path/to/your/logs/gunicorn-access.log"
loglevel = "info"

reload = True
timeout = 120
check_config = True

# Run in daemon mode
daemon = True