# Defines classes for built-in log file types
# This simplifies referencing built-ins for functions and testing


class BuiltInLogFileType:
    def __init__(
        self,
        name,
        sample_log_file,
        templates,
        column_functions,
        merge_events,
        datetime_columns,
        localize_datetime_columns,
    ):
        self.name = name
        self.sample_log_file = sample_log_file
        self.templates = templates
        self.column_functions = column_functions
        self.merge_events = merge_events
        self.datetime_columns = datetime_columns
        self.localize_datetime_columns = localize_datetime_columns
