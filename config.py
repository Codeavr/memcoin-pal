import os

class Config(object):
    def __getitem__(self, config_var):
        try:
            return os.environ[config_var]            
        except:
            raise Exception(f'No \'{config_var}\' variable in config')

        