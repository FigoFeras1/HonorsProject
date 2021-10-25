
import numpy
import pandas
from operation_tests import test_get_min

csv_file = '\\MOCK_DATA1.csv'


def parse_csv(csv):
    dataframe = pandas.DataFrame(pandas.read_csv(csv))
    dataframe.dropna(axis=0, how='all', inplace=True)
    dataframe.assign()
    arr = dataframe.to_numpy()
    return arr




def main():
    arr = parse_csv(csv_file)
    test_get_min(arr, col=5)


if __name__ == '__main__':
    main()
