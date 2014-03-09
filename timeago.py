def timeago(seconds):
    sec = seconds / 60
    if sec >= 1:
        hour = sec / 60
        if hour >= 1:
            day = hour/24
            if day >= 1:
                return {"type":"days", "value":day}
            else:
                return {"type":"hours", "value":hour}
        else:
            return {"type":"minutes", "value":sec}

    else:
        return {"type":"seconds", "value":seconds}

