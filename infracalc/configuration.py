import configparser
import os

class Configuration():

    def __init__(self, config, ctx):
        self.__configParser = configparser.ConfigParser()
        self.__configParser._interpolation = configparser.ExtendedInterpolation()
        self.__config_file_path = config
        self.ctx = ctx
        ctx.vlog("Reading file configuration {}".format(self.__config_file_path))
        self.__configParser.read(self.__config_file_path,)

    def get(self, section, key):
        if not (self.__configParser.has_section(section) or self.__configParser.has_option(section, key)):
            self.ctx.elog("Section {} or property {} was not found".format(section, property))
            return None
        else:
            try:
                return self.__configParser.get(section, key)
            except configparser.NoOptionError:
                return None

    def set(self, section, key, value):
        if section in self.__configParser:
            self.__configParser.set(section, key, value)
        else:
            self.__configParser.add_section(section)
            self.__configParser.set(section, key, value)
