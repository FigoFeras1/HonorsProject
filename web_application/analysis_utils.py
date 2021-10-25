import logging
from typing import Union, TextIO

import pandas
import numpy

from web_application import ALLOWED_EXTENSIONS
from web_application.statistic_controller import *

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s '
                           f': %(message)s')


def verify_file(filename: str) -> bool:
    """
    This method checks that the inputted file type is csv by checking the suffix
    :param filename: The filename to verify, including suffix
    :return: Whether The file type is a csv
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_csv(csv_file: Union[str, TextIO]) -> pandas.DataFrame:
    """
    Reads the csv file into a pandas DataFrame object and removes any empty rows
    :param csv_file: path or TextIO object of desired file to parse
    :return: DataFrame representation of the csv
    """

    "Reading the csv file into a DataFrame object"
    dataframe = pandas.DataFrame(pandas.read_csv(csv_file))
    # print(f"COLUMNS IN PARSE_CSV: {dataframe.columns.values}")

    """ 
    Drops all empty rows 
         axis=0 indicates that the rows should be dropped
         how='all' indicates that all empty rows should be dropped
         inplace=True alters the dataframe variable, eliminating the need for 
         another variable
    """
    dataframe.dropna(axis=0, how='all', inplace=True)

    return dataframe


def get_numpy_array(dataframe: pandas.DataFrame) -> numpy.ndarray:
    """
    Takes in a pandas DataFrame and converts it into a numpy structured ndarray,
    which allows elements to be accessible via their column name.
    :param dataframe: DataFrame representation of the data.
    :return: Numpy structured array.
    """
    columns = []
    for column_name in dataframe.columns:
        columns.append((column_name, 'U32'))
    columns = numpy.dtype(columns)
    array = numpy.array(dataframe.to_records(index=False), dtype=columns)
    return array


# TODO: Figure out if you should try and figure out if there are lists in the csv
def find_list(list_contents: str):
    pass


def main():
    file_path = '.\\uploads\\upload_CSV_CarData.csv'
    data_array = parse_csv(file_path)
    arr = get_numpy_array(data_array)
    # print(arr['VIN'][3])
    init_array(arr)
    # arr_sum = sum_column('Value')
    # print(arr_sum)
    # arr_sum = average_column('Value')
    # print(arr_sum)
    # print(get_unique_elements('Make'))
    print(max_occurrences('Make'))


if __name__ == '__main__':
    main()
