import numpy
import pandas

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


def sum_column(column_name) -> (str, ColumnTypeOperationMismatch):
    """
    Returns the sum of the desired column
    :param column_name: Name of the column to sum
    :return: numpy.ndarray with the sum of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    if isinstance(float_arr, ColumnTypeOperationMismatch):
        return float_arr
    return f"The Sum of Column '{column_name}' is: {numpy.sum(float_arr)}"


def average_column(column_name) -> (str,  ColumnTypeOperationMismatch):
    """
    Returns the average of the desired column
    :param column_name: Name of the column to average
    :return: numpy.ndarray with the average of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    if isinstance(float_arr, ColumnTypeOperationMismatch):
        return float_arr
    return f"The Average of Column '{column_name}' is: {numpy.average(float_arr)}"


def median_column(column_name) -> (str, ColumnTypeOperationMismatch):
    """
    Returns the median of the desired column
    :param column_name: Name of the column to median
    :return: numpy.ndarray with the median of the column or 0 for operation failed
    """
    float_arr = col_to_float(column_name)
    if isinstance(float_arr, ColumnTypeOperationMismatch):
        return float_arr
    return f"The Median of Column '{column_name}' is: {numpy.median(float_arr)}"


def min_occurrences(column_name) -> str:
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

    return prettify((min_names, min_value), False)


def max_occurrences(column_name) -> str:
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
    return prettify((max_names, max_value), True)


def col_to_float(column_name: str) -> (float, ColumnTypeOperationMismatch):
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


def prettify(data: tuple, maximum: bool):
    message = f"Maximum " if maximum else f"Minimum "

    names, occurrences = data
    return message + f"Number of Occurrences: {occurrences}." \
                     f"<br>Data that occurs {occurrences} times: " \
                     f"{', '.join([str(name) for name in names])} "


def sort(column_name: str) -> numpy.ndarray:
    return numpy.sort(__USER_ARRAY[column_name])


def sort_table_ascending(column_name: str):
    dataframe = pandas.DataFrame(__USER_ARRAY)

    return dataframe.sort_values(by=f'{column_name}', ascending=True,
                                 kind='quicksort', na_position='last')


def sort_table_descending(column_name: str):
    dataframe = pandas.DataFrame(__USER_ARRAY)

    return dataframe.sort_values(by=f'{column_name}', ascending=False,
                                 kind='quicksort', na_position='last')


operations = {'Sum': sum_column, 
              'Average': average_column,
              'Median': median_column,
              'Minimum Occurrences': min_occurrences,
              'Maximum Occurrences': max_occurrences,
              'Unique Elements': get_unique_elements,
              'Sort': sort,
              'Sort Table Ascending': sort_table_ascending,
              'Sort Table Descending': sort_table_descending}
