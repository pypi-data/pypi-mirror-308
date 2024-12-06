from template_log_parser.log_type_classes import BuiltInLogFileType

from template_log_parser.log_functions import process_log
from template_log_parser.column_functions import (
    calc_data_usage,
    isolate_ip_from_parentheses,
)

from template_log_parser.synology_templates import synology_template_dict, backup_dict, general_system_dict, user_activity_dict
from template_log_parser.sample import synology_sample_log


synology_column_process_dict = {
    "data_uploaded": [calc_data_usage, "data_uploaded_MB"],
    "data_downloaded": [calc_data_usage, "data_download_MB"],
    "client_ip": [isolate_ip_from_parentheses, "client_ip_address"],
}

# Merging events for consolidation
synology_merge_events_dict = {
    'backups': [value[2] for value in backup_dict.values()],
    'general_system': [value[2] for value in general_system_dict.values()],
    'user_activity': [value[2] for value in user_activity_dict.values()]
}

synology = BuiltInLogFileType(
    name="synology",
    sample_log_file=synology_sample_log,
    templates=synology_template_dict,
    column_functions=synology_column_process_dict,
    merge_events=synology_merge_events_dict,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)


def synology_process_log(file, dict_format=True):
    """
    Return a single Pandas Dataframe or dictionary of dfs whose keys are the log file event types,
        utilizes predefined templates and functions.  This function is tailored to Synology log files.

        Args:
            file (text log file):
                most commonly in the format of some_log_process.log

            dict_format (bool) (True by default):
                If False, function returns a concatenated df of all event types with numerous NaN values.
                Use with caution as this will consume more memory.

        Returns:
              dict or Pandas DataFrame:
                dict formatted as {'event_type_1': df_1, 'event_type_2': df_2, ...}
                Pandas Dataframe will include all event types and all columns

        Notes:
            This function is built on process_log()
    """
    final = process_log(
        file=file,
        template_dictionary=synology.templates,
        additional_column_functions=synology.column_functions,
        merge_dictionary=synology.merge_events,
        datetime_columns=synology.datetime_columns,
        localize_timezone_columns=synology.localize_datetime_columns,
        drop_columns=True,
        dict_format=dict_format,
    )

    return final
