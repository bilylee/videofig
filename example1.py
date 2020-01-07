#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import numpy as np
from videofig import videofig

SAVE_PLOTS = False

class Redraw(object):
    def __init__(self, amp=3000, f0=3):
        self.initialized = False
        self.amp = amp
        self.f0 = f0

    def draw(self, f, ax):
        amp = float(f) / self.amp
        f0 = self.f0
        t = np.arange(0.0, 1.0, 0.001)
        s = amp * np.sin(2 * np.pi * f0 * t)
        if not self.initialized:
            self.l, = ax.plot(t, s, lw=2, color='red')
            self.initialized = True
        else:
            self.l.set_ydata(s)

def redraw_fn(f, axes):
    redraw_fn.sub.draw(f, axes)
redraw_fn.sub = Redraw(3000, 1)

if not SAVE_PLOTS:
    videofig(100, redraw_fn)
else:
    videofig(100, redraw_fn, save_dir='example1_save')