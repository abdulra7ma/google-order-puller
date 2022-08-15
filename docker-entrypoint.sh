#!/bin/sh
# docker-entrypoint.sh

# If this is going to be a cron container, set up the cron service and create logs folder.
if [ "$1" = cron ]; then
    service cron start
    mkdir logs
fi

# Launch the main container command passed as arguments.
exec "$@"