# Status Alert Before query SQL
STATUS_SUCCESS = "Success"
STATUS_ERROR = "Error"
STATUS_EMPTY = "Empty"


def set_result(status='', result=None):
    result = {
        'status': status,
        'result': result
    }
    return result
