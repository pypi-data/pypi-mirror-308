# Base templates for Synology log analysis

# Backup tasks
backup_task = "{time} {server_name} {package_name} {system_user}:#011[{type}][{task_name}] Backup task {state}."
credentials_changed = "{time} {server_name} {package_name} {system_user}:#011[{type}] Credentials changed on the destination."
multi_backup_task = "{time} {server_name} {package_name} {system_user}:#011[{type}][{task_name}] Backup task {state}. [{files_scanned} files scanned] [{new_files} new files] [{files_modified} files modified] [{files_unchanged} files unchanged]"
multi_backup_task_no_modified = '{time} {package_name} {backup_name} {system_user}:#011[{type}][{task_name}] Backup task {state}. [{files_scanned} files scanned] [{files_unchanged} files unchanged]'
version_rotation = "{time} {server_name} {package_name} {system_user}:#011[{task_name}] Trigger version rotation."
integrity_check = "{time} {server_name} {package_name} {system_user}:#011[{type}][{task_name}] Backup integrity {result}"


# General System
back_online = '{time} {server_name} System {system_user}:#011Server back online.'
countdown_reboot = '{time} {server_name} System {system_user}:#011System started counting down to reboot.'
download_task = '{time} {server_name} System {system_user}:#011Download task for [{task}] {result}.'
process_start_or_stop = "{time} {server_name} System: System successfully {result} [{process}]."
scrubbing = "{time} {server_name} System {system_user}:#011System {state} {type} scrubbing on [{location}]."
on_battery = "{time} {server_name} System {system_user}:#011Server is on battery."
package_change = "{time} {server_name} System {system_user}:#011Package [{package}] has been successfully {state}."
service_started_or_stopped = '{time} {server_name} System {system_user}:#011[{service}] service was {state}.'
restarted_service = '{time} {server_name} System {system_user}:#011System successfully restarted {service} service.'
update = "{time} {server_name} System {system_user}:#011Update was {result}."

# User Activity
login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged in successfully via [{method}]."
failed_login = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to log in via [{method}] due to authorization failure."
logout = "{time} {server_name} Connection: User [{user}] from [{client_ip}] logged out the server via [{method}] with totally [{data_uploaded}] uploaded and [{data_downloaded}] downloaded."
sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] signed in to [{service}] successfully via [{auth_method}]."
failed_sign_in = "{time} {server_name} Connection: User [{user}] from [{client_ip}] failed to sign in to [{service}] via [{auth_method}] due to authorization failure."
folder_access = "{time} {server_name} Connection: User [{user}] from [{client_ip}] via [{method}] accessed shared folder [{folder}]."
cleared_notifications = "{time} {server_name} System {system_user}:#011Cleared [{user}] all notifications successfully."
new_user = '{time} {server_name} System {system_user}:#011User [{created_user}] was created.'
user_app_privilege = '{time} {server_name} System {system_user}:#011The app privilege on app [{app}] for user [{user}] was set to [{privilege}] from [{client_ip}].'
user_group = '{time} {server_name} System {system_user}:#011User [{user}] was {action} the group [{group}].'
win_file_service_event = '{time} {server_name} WinFileService Event: {event}, Path: {path}, File/Folder: {file_or_folder}, Size: {size}, User: {user}, IP: {client_ip}'

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string greatly increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

backup_dict = {
    "Backup": [backup_task, 7, "backup_task"],
    "Credentials changed": [credentials_changed, 5, 'credentials_changed'],
    "integrity check": [integrity_check, 7, "integrity_check"],
    "Backup ": [multi_backup_task, 11, "multi_backup_task"],
    " Backup": [multi_backup_task_no_modified, 9, 'multi_backup_task_no_changes'],
    "version rotation": [version_rotation, 5, "version_rotation"],
}

general_system_dict = {
    'back online': [back_online, 3, 'back_online'],
    'counting down': [countdown_reboot, 3, 'countdown_reboot'],
    'Download task': [download_task, 5, 'download_task'],
    "Package": [package_change, 5, 'package_change'],
    "scrubbing": [scrubbing, 6, "scrubbing"],
    "System successfully": [process_start_or_stop, 4, "process_start_or_stop"],
    'service was': [service_started_or_stopped, 5, 'service_start_or_stop'],
    'successfully restarted': [restarted_service, 4, 'restarted_service'],
    'on battery': [on_battery, 3, 'on_battery'],
    'Update': [update, 4, 'update'],

}

user_activity_dict = {
    "Cleared": [cleared_notifications, 4, "cleared_notifications"],
    "failed to log in": [failed_login, 5, "failed_login"],
    "failed to sign in": [failed_sign_in, 6, "failed_sign_in"],
    "accessed shared folder": [folder_access, 6, "folder_access"],
    "logged in successfully via": [login, 5, "login"],
    "logged out the server": [logout, 7, "logout"],
    "signed in to": [sign_in, 6, "sign_in"],
    'was created': [new_user, 4, 'new_user'],
    'app privilege': [user_app_privilege, 7, 'user_app_privilege'],
    'group': [user_group, 6, 'user_group'],
    'WinFileService Event': [win_file_service_event, 8, 'win_file_service_event'],
}

synology_template_dict = {**backup_dict, **general_system_dict, **user_activity_dict}
