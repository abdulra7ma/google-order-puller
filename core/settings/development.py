from os.path import join
import os

from .common import *
from .environment import env

# ##### DEBUG CONFIGURATION ###############################
DEBUG = env("DEBUG", default=False)

# allow all hosts during development
ALLOWED_HOSTS = ["*"]


# ##### DATABASE CONFIGURATION ############################
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": join(PROJECT_ROOT, "run", "dev.sqlite3"),
#     }
# }

DATABASES = {
    "default": env.db(
        "CORE_DATABASE_URL",
        default="psql://postgres:orders_puller_db_password_1@database:5432/orders_puller_db",
    )
}

# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS = DEFAULT_APPS

DATE_INPUT_FORMATS = ["%d/%m/%Y"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

CRONTAB_LOCK_JOBS = True
CRONJOBS = [
    (
        "* * * * *",
        "stats.workers.pull_orders.puller_initiator",
        ">> " + os.path.join(PROJECT_ROOT, "logs/cron_debug.log" + " 2>&1 "),
    ),
]
