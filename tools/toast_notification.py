from plyer import notification


def send_toast(title="Bot", body="Hello World", app_name="Supino"):
    notification.notify(
    title=title,
    message=body,
    app_name=app_name,
    timeout=8
    )
    return 0
