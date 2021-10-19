class ColumnTypeOperationMismatch(ValueError):

    def __init__(self, column_name, operation_name, message="Analysis not available"):
        self.column_name = column_name
        self.operation_name = operation_name
        self.message = f"Analysis not available: " \
                       f"Operation {operation_name} " \
                       f"not available on column {column_name} " \
                       f"due to a data type mismatch."

    def __str__(self):
        return self.message
