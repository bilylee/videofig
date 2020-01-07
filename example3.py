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
    def __init__(self, amp=3000, f0=3, ax_color=None):
        self.initialized = False
        self.amp = amp
        self.f0 = f0
        self.ax_color = ax_color

    def draw(self, f, ax):
        amp = float(f) / self.amp
        f0 = self.f0
        t = np.arange(0.0, 1.0, 0.001)
        s = amp * np.sin(2 * np.pi * f0 * t)
        if not self.initialized:
            ax.set_xticks([], [])
            ax.set_yticks([], [])
            ax.set_facecolor(self.ax_color)
            self.l, = ax.plot(t, s, lw=2, color='yellow')
            self.initialized = True
        else:
            # ax.set_facecolor(self.ax_color)
            self.l.set_ydata(s)

def redraw_fn(f, axes):
    redraw_fn.sub1.draw(f, axes[0])
    redraw_fn.sub2.draw(f, axes[1])
    redraw_fn.sub3.draw(f, axes[2])
redraw_fn.sub1 = Redraw(5000, 2, 'xkcd:salmon')
redraw_fn.sub2 = Redraw(7000, 10, 'xkcd:sea green')
redraw_fn.sub3 = Redraw(3000, 1, 'xkcd:sky blue')

if not SAVE_PLOTS:
    videofig(100, redraw_fn, 
            grid_specs={'nrows': 2, 'ncols': 2}, 
            layout_specs = ['[0, 0]', '[0, 1]', '[1, :]'])
else:
    videofig(100, redraw_fn, 
            grid_specs={'nrows': 2, 'ncols': 2}, 
            layout_specs = ['[0, 0]', '[0, 1]', '[1, :]'],
            save_dir='example3_save')