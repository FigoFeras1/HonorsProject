class ColumnTypeOperationMismatch(ValueError):

    def __init__(self):
        self.column_name = ''
        self.operation_name = ''
        self.message = f"Analysis not available: data type mismatch."

    def get_message(self, column_name, operation_name):
        self.message = f"Analysis not available: " \
                       f"'{operation_name}' operation " \
                       f"not available on column '{column_name}' " \
                       f"due to a data type mismatch."

    def __str__(self):
        return self.message
