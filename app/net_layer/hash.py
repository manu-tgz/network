class IPPacketSerializer:
    """
                                  TRAMA
    |  32 bits   |  32 bits  |  8 bits |  8 bits   |    8 bits    |         |
    |------------|-----------|---------|-----------|--------------|---------|
    | IP_receive | IP_source |   TTL   | Protocolo | Payload size | Payload |
    """