import socket
import logging
import urllib.parse

from crawlino import input_plugin, PluginReturnedData, \
    dict_to_object, CrawlinoValueError

log = logging.getLogger("crawlino-plugins")


@input_plugin
def input_raw_socket(prev_step: PluginReturnedData, **kwargs) \
        -> PluginReturnedData:

    log.debug("Starting plugin - input::raw-socket")
    allowed_inputs = ("ip", "web", "domain", "url")
    allowed_proto = ("tcp", "udp")

    # Load data
    prev_config = dict_to_object(prev_step.to_dict)

    if prev_config.source_type not in allowed_inputs:
        raise CrawlinoValueError(f"This plugin only works with: "
                                 f"{'|'.join(allowed_inputs)}")

    # -------------------------------------------------------------------------
    # Extract config
    # -------------------------------------------------------------------------
    config = kwargs.get("config", {})
    port_to_test = config.get("port", None)
    data_to_send = config.get("data", None)
    connection_timeout = config.get("timeout", "0.5")
    port_proto = "tcp"

    #
    # Check proto
    #
    if config.get("proto", None):
        if config.get("proto", None) not in allowed_proto:
            raise CrawlinoValueError(f"This plugin only works with: "
                                     f"{'|'.join(allowed_proto)}")

        port_proto = config.get("proto")

    if port_proto == "tcp":
        proto = socket.SOCK_STREAM
    else:
        proto = socket.SOCK_DGRAM

    #
    # Checking timeout
    #
    try:
        timeout = float(connection_timeout)
    except ValueError:
        raise CrawlinoValueError(
            "Invalid timeout value. It must be a float falue")

    #
    # Extract target
    #
    if prev_config.source_type == "ip":
        ip = prev_config.target
    else:
        ip, *_ = urllib.parse.urlparse(prev_config.target).netloc.split(":")

    #
    # Do connection
    #
    if not data_to_send:
        data_to_send = b"\r\n\r\n"
    else:
        data_to_send = data_to_send.encode()

    log.debug(f"Connecting to {ip}:{port_to_test}...")
    with socket.socket(socket.AF_INET, proto) as s:
            s.settimeout(timeout)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            code = s.connect_ex((ip, int(port_to_test)))

            if code == 0:  # 0 = Open
                try:
                    s.sendall(data_to_send)
                    d, _, _, _ = s.recvmsg(100000)
                    received_data = d.decode(errors="ignore")
                    status = "open"
                except socket.timeout:
                    log.error(f"Port {port_to_test} is open but it got a "
                              f"timeout when try to get data from socket")
            else:
                received_data = None
                status = "closed/filtered"

    d = PluginReturnedData(**dict(
        host=ip,
        status=status,
        data=received_data,
        port=port_to_test
    ))

    return d
