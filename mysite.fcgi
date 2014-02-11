#!/home7/cohetico/python27/bin/python27
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/home7/cohetico/python27")
sys.path.insert(13, "/home7/cohetico/Quiniela")

os.environ['DJANGO_SETTINGS_MODULE'] = 'Quiniela.settings'
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
