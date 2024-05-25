import numpy as np

def iwt53(c):
    c = np.asarray(c, dtype=np.int64)
    if len(c) % 2 != 0:
        last_element = c[-1]
        c = c[:-1]
    else:
        last_element = None
    s = c[0::2]
    d = c[1::2]
    l = len(s)
    a = d[:l-1] - np.floor(0.5 * (s[:l-1] + s[1:l]))
    b = d[l-1] - s[l-1]
    d = np.concatenate((a, [b]), axis=None)
    a = s[0] + np.floor(0.5 * d[0] + 0.5)
    b = s[1:l] + np.floor(0.25 * (d[1:l] + d[:l-1]) + 0.5)
    s = np.concatenate(([a], b), axis=None)
    if last_element is not None:
        c = np.append(np.column_stack((s, d)).ravel(), last_element)
    else:
        c = np.column_stack((s, d)).ravel()
    return c

def iiwt53(c):
    c = np.asarray(c, dtype=np.int64)
    if len(c) % 2 != 0:
        last_element = c[-1]
        c = c[:-1]
    else:
        last_element = None
    s = c[0::2]
    d = c[1::2]
    l = len(s)
    a = s[0] - np.floor(0.5 * d[0] + 0.5)
    b = s[1:l] - np.floor(0.25 * (d[1:l] + d[:l-1]) + 0.5)
    s = np.concatenate(([a], b), axis=None)
    a = d[:l-1] + np.floor(0.5 * (s[:l-1] + s[1:l]))
    b = d[l-1] + s[l-1]
    d = np.concatenate((a, [b]), axis=None)
    if last_element is not None:
        c = np.append(np.column_stack((s, d)).ravel(), last_element)
    else:
        c = np.column_stack((s, d)).ravel()
    return c