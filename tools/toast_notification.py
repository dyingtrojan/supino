from plyer import notification


def send_toast(title="Bot", body="Hello World", app_name="Supino"):
    """
    Send a toast notification for the user. Use ONLY when it has finished processes.
    """
    notification.notify(
    title=title,
    message=body,
    app_name=app_name,
    timeout=8
    )
    return 0
