def keyboard_to_regex(keyboard):
    res = ""
    for row in keyboard:
        for button in row:
            if button != "Custom":
                res += button + "|"
    return res[:-1]