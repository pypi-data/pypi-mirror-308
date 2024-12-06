from template_log_parser.log_functions import process_log

from template_log_parser.pihole_templates import pihole_template_dict, pihole_dnsmasq, pihole_ftl
from template_log_parser.log_type_classes import BuiltInLogFileType
from template_log_parser.sample import pihole_debian_sample_log

# Merging events for consolidation
pihole_merge_events_dict = {
    'dnsmasq': [value[2] for value in pihole_dnsmasq.values()],
    'ftl': [value[2] for value in pihole_ftl.values()],
}

pihole = BuiltInLogFileType(
    name="pihole",
    sample_log_file=pihole_debian_sample_log,
    templates=pihole_template_dict,
    column_functions=None,
    merge_events=pihole_merge_events_dict,
    datetime_columns=["time"],
    localize_datetime_columns=None,
)


def pihole_process_log(file, dict_format=True):
    """
    Return a single Pandas Dataframe or dictionary of dfs whose keys are the log file event types,
        utilizes predefined templates and functions.  This function is tailored to PiHole log files.

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
    output = process_log(
        file=file,
        template_dictionary=pihole.templates,
        additional_column_functions=pihole.column_functions,
        merge_dictionary=pihole.merge_events,
        datetime_columns=pihole.datetime_columns,
        localize_timezone_columns=pihole.localize_datetime_columns,
        dict_format=dict_format,
    )

    return output
