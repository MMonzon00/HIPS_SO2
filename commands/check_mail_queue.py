import os
from logging_notification import log_event, notify_admin

def check_mail_queue():
    command = "mailq"
    command_output = os.popen(command).read()
    final_message = ''
    
    if "" in command_output:
        final_message += "The mail queue is empty\n"
        log_event(final_message)
    else:
        output = command_output.splitlines()
        return output
    
    mail_queue = command_output.splitlines()
    if len(mail_queue) > 5:  # Choose an appropriate threshold
        final_message += f"Many emails ({len(mail_queue)}) were found in the queue, the administrator has been notified\n"
        log_event(final_message)
        notify_admin("High Email Queue Alert", final_message)
    else:
        final_message += "Not many emails were found in the queue\n"
        log_event(final_message)
    return final_message
