import django, os, sys
from django.core import management

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_vote.settings")
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))
django.setup()

# Migrate
management.call_command("migrate", no_input=True)
# Seed
