from .services import get_sites_status, send_email_if_error_detected


def do():
    get_sites_status()


def every_hour_check():
    send_email_if_error_detected()
