import os

import environ

env = environ.Env(DEBUG=(bool, False))

root_path = environ.Path(__file__) - 2

env_file = root_path(".env")

if os.path.exists(env_file):  # pragma: no cover
    environ.Env.read_env(env_file=env_file)
