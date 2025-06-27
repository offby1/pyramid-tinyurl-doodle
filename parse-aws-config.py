import configparser
import pathlib
import sys

config = configparser.ConfigParser()
config.read(pathlib.Path("~/.aws/credentials").expanduser())

print(config["default"][sys.argv[1]])
