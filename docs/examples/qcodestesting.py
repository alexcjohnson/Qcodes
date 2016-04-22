print('\n\n\n')

import logging
logger = logging.getLogger('qcodes')
logger.setLevel(logging.DEBUG)

logger.debug('start')

import time
import numpy as np

import qcodes as qc
from toymodel import AModel, MockGates, MockSource, MockMeter, AverageGetter, AverageAndRaw


if __name__ == '__main__':
    # freeze_support()

    qc.set_mp_method('spawn')  # force Windows behavior on mac


    model = AModel()
    gates = MockGates('gates', model=model)
    source = MockSource('source', model=model)
    meter = MockMeter('meter', model=model)

    station = qc.Station(gates, source, meter)

    station.set_measurement(meter.amplitude)
    c0, c1, c2, vsd = gates.chan0, gates.chan1, gates.chan2, source.amplitude

    logger.debug('blah yyy')

    # qc.active_children()


    # station.snapshot(update=True)
