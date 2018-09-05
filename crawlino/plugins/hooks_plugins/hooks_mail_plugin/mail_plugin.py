import logging
import smtplib

from crawlino import hook_plugin, PluginReturnedData, CrawlinoValueError

log = logging.getLogger("crawlino-plugin")


@hook_plugin
def hook_mail(prev_step: PluginReturnedData, **kwargs):
    log.debug("Hooks Module :: mail plugin")

    data = prev_step.to_dict
    # -------------------------------------------------------------------------
    # Check the source of data. If data comes from step: expressions, check if
    # there're results. If not have results -> don't display nothing
    #
    # Data from STEP_EXTRACTORS have property: 'extractor_results'
    # -------------------------------------------------------------------------
    if "extractor_results" in data:
        if not data["extractor_results"]:
            # No data to display
            return
        else:
            data = data["extractor_results"]
    else:
        data = [data]

    config = kwargs["config"]

    # -------------------------------------------------------------------------
    # Get mandatory data
    # -------------------------------------------------------------------------
    mail_from: str = config["from"]
    mail_to: str = config["to"]
    mail_body_field: str = config["bodyField"]
    mail_subject_field: str = config.get("subject", mail_body_field[:100])

    # -------------------------------------------------------------------------
    # Server settings
    # -------------------------------------------------------------------------
    server_config: dict = config["server"]

    if mail_from.endswith("@gmail.com"):
        server_smtp = "smtp.gmail.com"
        server_port = 587
        server_tls = True
    else:
        server_smtp = server_config["smtp"]
        server_port = int(server_config.get("port", 587))
        server_tls = bool(server_config.get("tls", True))

    server_user = server_config["user"]
    server_password = server_config["password"]

    server = smtplib.SMTP(server_smtp, server_port, timeout=2)
    if server_tls:
        server.starttls()

    log.info("Start sending mail")
    try:
        server.login(server_user, server_password)

        for d in data:
            _data = d.to_dict

            try:
                message_body = f"Subject:{mail_subject_field}\n\n" \
                               f"{_data[mail_body_field]}"
            except KeyError as e:
                log.error(f"Error while try to sending mail. bodyField "
                          f"'{mail_body_field}' not found in response of "
                          f"previous step")
                continue

            server.sendmail(mail_from, mail_to, message_body)
            server.quit()

            log.info("Mail sent")
    except Exception as e:
        log.error(f"Error while try to sending mail: '{e}'")


