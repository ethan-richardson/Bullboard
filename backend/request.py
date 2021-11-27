class Request:
    def __init__(self,header_data, code, path):
        self.headers = parse_headers(header_data)
        self.code = code
        self.path = path


def parse_headers(header_data):
    headers = {}
    for hdr in str(header_data).split('\n'):
        split = hdr.split(':')
        if len(split) >= 2:
            headers[split[0].strip()] = split[1].strip()
    return headers
    
    