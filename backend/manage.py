#!/usr/bin/env python

import os
import json
import signal
import subprocess
import time

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


cur_dir = os.path.abspath(os.path.dirname(__file__))


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


APPLICATION_CONFIG_PATH = os.path.join(cur_dir, "config")
DOCKER_PATH = os.path.join(
  cur_dir,
  os.path.dirname(__file__), "docker")


def app_config_file(config):
  return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(config):
  return os.path.join(DOCKER_PATH, f"{config}.yml")


def configure_app(config):
  # Read configuration from the relative JSON file
  with open(app_config_file(config)) as f:
    config_data = json.load(f)

  # Convert the config into a usable Python dictionary
  config_data = dict((item["name"], item["value"]) for item in config_data)

  for key, value in config_data.items():
    setenv(key, value)


@click.group()
def cli():
  pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
  configure_app(os.getenv("APPLICATION_CONFIG"))
  cmdline = ["flask"] + list(subcommand)

  try:
    p = subprocess.Popen(cmdline)
    p.wait()
  except KeyboardInterrupt:
    p.send_signal(signal.SIGINT)
    p.wait()


@cli.command(context_settings={"ignore_unknown_options": True})
def db_upgrade():
  config = os.getenv("APPLICATION_CONFIG")

  configure_app(os.getenv("APPLICATION_CONFIG"))
  # cmdline = "flask db init".split()
  # subprocess.call(cmdline)
  cmdline = "flask db migrate".split(' ')
  subprocess.call(cmdline)
  cmdline = "flask db upgrade".split()
  subprocess.call(cmdline)


@cli.command(context_settings={"ignore_unknown_options": True})
def run_server():
  config = os.getenv("APPLICATION_CONFIG")

  configure_app(os.getenv("APPLICATION_CONFIG"))
  # cmdline = "flask db init".split()
  # subprocess.call(cmdline)
  cmdline = "flask db migrate".split(' ')
  subprocess.call(cmdline)
  cmdline = "flask db upgrade".split()
  subprocess.call(cmdline)
  if config == 'development':
    cmdline = "flask run --host 0.0.0.0".split(' ')
  elif config == 'production':
    cmdline = "gunicorn -w 4 -b 0.0.0.0 wsgi:app".split(' ')
  else:
    raise ValueError(f'config not implemented for run command: {config}')
  try:
    p = subprocess.Popen(cmdline)
    p.wait()
  except KeyboardInterrupt:
    p.send_signal(signal.SIGINT)
    p.wait()


def docker_compose_cmdline(commands_string=None):
  config = os.getenv("APPLICATION_CONFIG")
  print(f'config: {config}')
  configure_app(config)
  
  compose_file = docker_compose_file(config)

  if not os.path.isfile(compose_file):
    raise ValueError(f"The file {compose_file} does not exist.")

  command_line = [
    "docker-compose",
    "-p",
    config,
    "-f",
    compose_file
  ]

  if commands_string:
    command_line.extend(commands_string.split(" "))
  return command_line


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = docker_compose_cmdline() + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


def run_sql(statements):
  conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOSTNAME"),
    port=os.getenv("POSTGRES_PORT")
  )

  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()
  for statement in statements:
      cursor.execute(statement)

  cursor.close()
  conn.close()


def wait_for_logs(cmdline, message):
  logs = subprocess.check_output(cmdline)
  while message not in logs.decode("utf-8"):
    time.sleep(1)
    logs = subprocess.check_output(cmdline)


@cli.command()
def create_initial_db():
  configure_app(os.getenv("APPLICATION_CONFIG"))

  try:
    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])
  except psycopg2.errors.DuplicateDatabase:
    print(
        f"The database {os.getenv('APPLICATION_DB')} already exists and will not be recreated"
    )


@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
  os.environ["APPLICATION_CONFIG"] = "testing"
  configure_app(os.getenv("APPLICATION_CONFIG"))

  cmdline = docker_compose_cmdline("up -d")
  subprocess.call(cmdline)

  cmdline = docker_compose_cmdline("logs db")
  wait_for_logs(cmdline, "ready to accept connections")

  run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

  # import sample data
  sample_filename = "application_data.psql"
  username = os.getenv('POSTGRES_USER')
  host = os.getenv('POSTGRES_HOSTNAME')
  db_name = os.getenv('APPLICATION_DB')
  port = os.getenv('POSTGRES_PORT')
  pw = os.getenv('POSTGRES_PASSWORD')
  psql_str = f'postgresql://{username}:{pw}@{host}:{port}/{db_name}'
  cmdline = [
    "psql",
    psql_str,
    "-f", sample_filename
  ]
  subprocess.call(cmdline)

  cmdline = ["coverage", "run", "--source", "application",
  "-m", "unittest", "discover"]
  cmdline.extend(filenames)
  subprocess.call(cmdline)
  cmdline = ["coverage", "report", "-m"]
  subprocess.call(cmdline)

  cmdline = docker_compose_cmdline("down --volume")
  subprocess.call(cmdline)


if __name__ == "__main__":
    cli()
