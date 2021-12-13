import logging
from typing import Union, TextIO

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

    """ 
    Drops all empty rows 
         axis=0 indicates that the rows should be dropped
         how='all' indicates that all empty rows should be dropped
         inplace=True alters the dataframe variable, eliminating the need for 
         another variable
    """
    dataframe.dropna(axis=0, how='all', inplace=True)

    return dataframe


def get_numpy_array(dataframe: pandas.DataFrame) -> numpy.recarray:
    """
    Takes in a pandas DataFrame and converts it into a numpy structured ndarray,
    which allows elements to be accessible via their column name.
    :param dataframe: DataFrame representation of the data.
    :return: Numpy structured array.
    """
    return dataframe.to_records(index=False)
