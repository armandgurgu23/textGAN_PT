from configs.analyst_defaults import *
import argparse
import os
import numpy as np
import nltk
import re


class Processed_Dataset_Generator(object):
    def __init__(self, analyst_cp):
        self.generator_cp = analyst_cp
        # Initialize the settings of the data analyst.
        self.generator_cfg = self.get_analyst_config(self.generator_cp)
        print('\n\n Displaying the yaml configuration!\n\n')
        print(self.generator_cfg)
        print('\n\n')
        self.path_file = self.get_filename_to_analyze(self.generator_cfg)
        print('The file to open: \n')
        print(self.path_file)

    def __call__(self):
        lines_arr, counts_arr = self.read_filename_contents(self.path_file)
        print('Total number of lines in file = {} is: {}'.format(
            self.generator_cfg.dataset.dataset_name, len(lines_arr)))
        unique_values, counts_unique = self.compute_unique_char_counts(counts_arr)
        print('Unique values = {} and shape = {}'.format(unique_values, unique_values.shape))
        print('Distribution of counts = \n')
        print(counts_unique)
        if self.generator_cfg.dataset.compute_tokens:
            tokenized_lines_arr = self.count_tokens_all_lines(lines_arr)
            self.cache_tokenized_counts(tokenized_lines_arr, self.generator_cfg)
        else:
            # Read in the cached tokens in memory.
            tokenized_lines_arr = self.load_tokenized_counts_from_disk(self.generator_cfg)
            print('The in memory token counts = {}\n'.format(tokenized_lines_arr))
        if self.generator_cfg.dataset.processed_dataset.generate_processed_dataset:
            self.generate_compressed_textfiles(tokenized_lines_arr, lines_arr, self.generator_cfg)
        return

    def generate_compressed_textfiles(self, token_counts, lines_arr, cfg):
        compressed_out_file = self.generate_compressed_file_path(cfg)
        print('Caching compressed dataset at = {}'.format(compressed_out_file))
        with open(compressed_out_file, 'w') as comp_file:
            for index, curr_line in enumerate(lines_arr):
                curr_line_token_count = token_counts[index]
                if curr_line_token_count > cfg.dataset.processed_dataset.token_threshold:
                    comp_file.write(curr_line)
                    comp_file.write('\n')
        print('Finished generating compressed file {} to disk!'.format(compressed_out_file))
        return

    def generate_compressed_file_path(self, cfg):
        dir_path = cfg.dataset.cache_tokens
        prefix_name = cfg.dataset.dataset_name.split('.')[0] + '_compressed.txt'
        return os.path.join(dir_path, prefix_name)

    def load_tokenized_counts_from_disk(self, cfg):
        cache_path = self.get_tokens_cache_path(cfg)
        return np.load(cache_path)

    def cache_tokenized_counts(self, tokens_arr, cfg):
        tokens_arr = np.array(tokens_arr)
        cache_path = self.get_tokens_cache_path(cfg)
        print('The path where I will cache tokens = {}'.format(cache_path))
        np.save(file=cache_path, arr=tokens_arr)
        return

    def get_tokens_cache_path(self, cfg):
        prefix_filename = cfg.dataset.dataset_name.split('.')[0]
        cache_path = os.path.join(cfg.dataset.cache_tokens, prefix_filename + '_ctokens.npy')
        return cache_path

    def get_analyst_config(self, path):
        # Get the default configuration for the analyst YAML file.
        analyst_settings = get_analyst_defaults()
        # Overwrite changed settings and make frozen YAML file.
        analyst_settings.merge_from_file(path)
        analyst_settings.freeze()
        return analyst_settings

    def get_filename_to_analyze(self, cfg):
        filename = os.path.join(cfg.dataset.path, cfg.dataset.dataset_name)
        return filename

    def count_tokens_all_lines(self, lines_arr):
        tokenized_lines = []
        # Each tokenized line in the file is now an array.
        for curr_line in lines_arr:
            tokenized_lines.append(len(nltk.word_tokenize(curr_line)))
        return tokenized_lines

    def compute_unique_char_counts(self, counts_arr):
        return np.unique(counts_arr, return_counts=True)

    def read_filename_contents(self, file_path):
        line_array = []
        counts_array = []
        with open(file_path, 'r') as f_obj:
            for line in f_obj:
                line = line.strip('\n')
                line = self.apply_text_filter(line)
                line_array.append(line)
                counts_array.append(len(line))
        return line_array, counts_array

    def apply_text_filter(self, line):
        # Remove square/curly brackets since they are of no use.
        line = re.sub(r"[()]", "", line)
        return line


def analyst_arguments():
    parser = argparse.ArgumentParser(description='Computes analytics for a given corpus.')
    parser.add_argument('--yf', type=str, default='configs/analyst.yaml',
                        help='Path to the YACS config file.')
    args = parser.parse_args()
    return args


def run_analyst():
    run_settings = analyst_arguments()
    # Set up the analyst object.
    analyst = Processed_Dataset_Generator(run_settings.yf)
    analyst()
    return


if __name__ == "__main__":
    run_analyst()
