import logging
from typing import Type

import numpy

from web_application.errors import ColumnTypeOperationMismatch

__USER_ARRAY = numpy.recarray


def init_array(input_array: numpy.recarray) -> None:
    """
    Initializes a global array to the array read from the CSV, then sets it so
    that it is read-only. This is done for efficiency and to avoid passing large
    amounts of data to functions repeatedly. Not for use outside of this file
    :param input_array: numpy.ndarray representation of CSV input
    :return: None
    """
    global __USER_ARRAY
    __USER_ARRAY = input_array
    __USER_ARRAY.setflags(write=False, uic=False, align=False)


def sum_column(column_name) -> numpy.ndarray:
    """
    Returns the sum of the desired column
    :param column_name: Name of the column to sum
    :return: numpy.ndarray with the sum of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    return numpy.sum(float_arr) if float_arr is not None else float_arr


def average_column(column_name) -> numpy.ndarray:
    """
    Returns the average of the desired column
    :param column_name: Name of the column to average
    :return: numpy.ndarray with the average of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    return numpy.average(float_arr) if float_arr is not None else float_arr


def median_column(column_name) -> numpy.ndarray:
    """
    Returns the median of the desired column
    :param column_name: Name of the column to median
    :return: numpy.ndarray with the median of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    return numpy.median(float_arr) if float_arr else float_arr


def min_occurrences(column_name) -> tuple:
    """
    Finds the elements that occur the least amount of times and the value
    :param column_name: name of the column to parse
    :return: tuple where the first element is a numpy.ndarray of the column names
             and the second element is the number of occurrences
    """
    min_names = []
    unique_values = get_unique_elements(column_name)
    rows, min_value = unique_values[0], unique_values[2].min()

    for index in numpy.where(unique_values[2] == min_value):
        min_names = numpy.append(min_names, rows[index])

    return min_names, min_value


def max_occurrences(column_name) -> tuple:
    """
    Finds the elements that occur the most amount of times and the value
    :param column_name: name of the column to parse
    :return: tuple where the first element is a numpy.ndarray of the element names
             and the second element is the number of occurrences
    """
    max_names = []
    unique_values = get_unique_elements(column_name)
    rows, max_value = unique_values[0], unique_values[2].max()

    for index in numpy.where(unique_values[2] == max_value):
        max_names = numpy.append(max_names, rows[index])

    return max_names, max_value


def col_to_float(column_name: str) -> float | ColumnTypeOperationMismatch:
    """
    Attempts to convert column elements of global to float-type.
    If failed, -1 is returned. This is to prevent the application from crashing.
    :param column_name: name of column to convert
    :return: numpy.ndarray with elements converted to floats or -1 (conversion fail)
    """
    global __USER_ARRAY

    try:
        return __USER_ARRAY[column_name].astype(dtype=float, copy=True)
    except ValueError:
        return ColumnTypeOperationMismatch()


def get_unique_elements(column_name: str) -> numpy.ndarray:
    """
    Gets unique row names, indices, and counts
    :param column_name: name of column to parse
    :return: numpy.ndarray with row names, indices and counts
    """
    global __USER_ARRAY

    return numpy.unique(__USER_ARRAY[column_name],
                        return_index=True, return_counts=True)


def sort(column_name: str) -> numpy.ndarray:
    pass


operations = {'Sum': sum_column, 'Average': average_column,
              'Median': median_column,
              'Minimum Occurrences': min_occurrences,
              'Maximum Occurrences': max_occurrences,
              'Unique Elements': get_unique_elements}
