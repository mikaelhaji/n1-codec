import numpy as np

def apply_delta_encoding(signal):
    return np.diff(signal, prepend=signal[0])

def apply_delta_decoding(deltas, first_sample):
    reconstructed_signal = np.cumsum(np.insert(deltas, 0, first_sample))
    return reconstructed_signal[1:]  # Exclude the artificially added first sample for correct result