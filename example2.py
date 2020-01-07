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
import time

import cv2 as cv
from matplotlib.pyplot import Rectangle

from videofig import videofig

NUM_IMAGES = 100
PLAY_FPS = 100  # set a large FPS (e.g. 100) to test the fastest speed our script can achieve
SAVE_PLOTS = False  # whether to save the plots in a directory

# Preload images and boxes
imgs, boxs = [], []
for idx in range(NUM_IMAGES):
    img = cv.imread('assets/squirrel-2/imgs/{:08d}.jpg'.format(idx + 1))
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    imgs.append(img)

with open('assets/squirrel-2/groundtruths.txt', 'r') as file_handle:
    for line in file_handle:
        boxs.append([float(v) for v in line.strip().split(',')])


def redraw_fn(f, ax):
    img = imgs[f]
    box = boxs[f]

    x, y, w, h = box
    if not redraw_fn.initialized:
        redraw_fn.img_handle = ax.imshow(img)
        box_artist = Rectangle((x, y), w, h,
                               fill=False,  # remove background
                               lw=2,
                               edgecolor="red")
        ax.add_patch(box_artist)
        redraw_fn.box_handle = box_artist
        redraw_fn.last_time = time.time()
        redraw_fn.text_handle = ax.text(0., 1 - 0.05,
                                        'Resolution {}x{}, FPS: {:.2f}'.format(img.shape[1], img.shape[0], 0),
                                        transform=ax.transAxes,
                                        color='yellow', size=12)
        redraw_fn.initialized = True
    else:
        redraw_fn.img_handle.set_array(img)
        redraw_fn.box_handle.set_xy((x, y))
        redraw_fn.box_handle.set_width(w)
        redraw_fn.box_handle.set_height(h)
        current_time = time.time()
        redraw_fn.text_handle.set_text('Resolution {}x{}, FPS: {:.2f}'.format(img.shape[1], img.shape[0],
                                                                              1 / (current_time - redraw_fn.last_time)))
        redraw_fn.last_time = current_time


redraw_fn.initialized = False

if not SAVE_PLOTS:
    videofig(NUM_IMAGES, redraw_fn, play_fps=PLAY_FPS)
else:
    videofig(NUM_IMAGES, redraw_fn, play_fps=PLAY_FPS, save_dir='example2_save')
