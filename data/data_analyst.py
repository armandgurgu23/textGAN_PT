from configs.analyst_defaults import *
import argparse


class Data_Analyst(object):
    def __init__(self, analyst_cp):
        self.analyst_cp = analyst_cp
        # Initialize the settings of the data analyst.
        self.analyst_cfg = self.get_analyst_config(self.analyst_cp)
        print('\n\n Displaying the yaml configuration!\n\n')
        print(self.analyst_cfg)
        print('\n\n')

    def get_analyst_config(self, path):
        # Get the default configuration for the analyst YAML file.
        analyst_settings = get_analyst_defaults()
        # Overwrite changed settings and make frozen YAML file.
        analyst_settings.merge_from_file(path)
        analyst_settings.freeze()
        return analyst_settings


def analyst_arguments():
    parser = argparse.ArgumentParser(description='Computes analytics for a given corpus.')
    parser.add_argument('--yf', type=str, help='Path to the YACS config file.')
    args = parser.parse_args()
    return args


def run_analyst():
    run_settings = analyst_arguments()
    # Set up the analyst object.
    analyst = Data_Analyst(run_settings.yf)
    return


if __name__ == "__main__":
    run_analyst()
