# videofig
Lightweight image sequence visualization utility based on matplotlib

## Introduction
Python is an elegant programming language with rich add-on libraries to meet various needs. For scientific computation, it has `numpy`; for plotting, it has `matplotlib`. Personally, I use Python for video analysis and it works like a charm except for one thing: *visualize image sequences for detailed inspection*. 
 
When visualizing image sequences for detailed inspection, it is desirable to have `play`, `pause`, `forward by one frame`, `backward by one frame`, etc utilities. Moreover, we may add some custom plots(bounding box, for example) and graphics on top. In Matlab, we have `VideoPlayer` in `Computer Vision System Toolbox`, but to the best of my knowledge, there isn't any tools in Python that provides similar functionality. Let me know, if there are any : )
 
Accidentally, I came across [the excellent script of João Filipe Henriques](https://www.mathworks.com/matlabcentral/fileexchange/29544-figure-to-play-and-analyze-videos-with-custom-plots-on-top?focused=5172704&tab=function
), which provides utilities for detailed image sequence inspection before `VideoPlayer` is available in Matlab. Inspired by this, I decided to write a similar function in Python before more sophisticated tools come out.

## Dependency
This tool is specifically designed to be minimal, lightweight and readable such that anyone can easily modify it to suit different needs. The only dependency is `Matplotlib`. I have tested it in Python 2.7, but it should also work in Python 3.5.

- matplotlib >= 2.0.0
 
## Basic Usage
```python
videofig(NUM_FRAMES, REDRAW_FUNC)
```

Creates a figure with a horizontal scrollbar and shortcuts to scroll automatically.
The scroll range is 0 to NUM_FRAMES - 1. The function REDRAW_FUN(F, AXES) is called to
redraw at scroll position F (for example, REDRAW_FUNC can show the frame F of a video)
using AXES for drawing. F is an integer, AXES is a instance of [Axes class](https://matplotlib.org/api/axes_api.html)

This can be used not only to play and analyze standard videos, but it also lets you place
any custom Matplotlib plots and graphics on top.

The keyboard shortcuts are:
+ Enter(Return) -- play/pause video (25 frames-per-second default).
+ Backspace -- play/pause video 5 times slower.
+ Right/left arrow keys -- advance/go back one frame.
+ Page down/page up -- advance/go back 30 frames.
+ Home/end -- go to first/last frame of video.

## Advanced Usage
```python
videofig(NUM_FRAMES, REDRAW_FUNC, FPS, BIG_SCROLL)
```
Also specifies the speed of the play function (frames-per-second) and
the frame step of page up/page down (or empty for defaults).

```python
videofig(NUM_FRAMES, REDRAW_FUNC, FPS, BIG_SCROLL, KEY_FUNC)
```
Also calls KEY_FUNC(KEY) with any keys that weren't processed, so you
can add more shortcut keys (or empty for none).

## Examples
### Example 1: Plot a dynamic sine wave
```python
  import numpy as np

  def redraw_fn(f, axes):
    amp = float(f) / 3000
    f0 = 3
    t = np.arange(0.0, 1.0, 0.001)
    s = amp * np.sin(2 * np.pi * f0 * t)
    if not redraw_fn.initialized:
      redraw_fn.l, = axes.plot(t, s, lw=2, color='red')
      redraw_fn.initialized = True
    else:
      redraw_fn.l.set_ydata(s)

  redraw_fn.initialized = False

  videofig(100, redraw_fn)
```

### Example 2: Show images in a custom directory
```python
  import os
  import glob
  from scipy.misc import imread

  img_dir = 'YOUR-IMAGE-DIRECTORY'
  img_files = glob.glob(os.path.join(video_dir, '*.jpg'))

  def redraw_fn(f, axes):
    img_file = img_files[f]
    img = imread(img_file)
    if not redraw_fn.initialized:
      redraw_fn.im = axes.imshow(img, animated=True)
      redraw_fn.initialized = True
    else:
      redraw_fn.im.set_array(img)
  redraw_fn.initialized = False

  videofig(len(img_files), redraw_fn, play_fps=30)
```

### Example 3: Show images together with object bounding boxes
```python
  import os
  import glob
  from scipy.misc import imread
  from matplotlib.pyplot import Rectangle
  
  video_dir = 'YOUR-VIDEO-DIRECTORY'

  img_files = glob.glob(os.path.join(video_dir, '*.jpg'))
  box_files = glob.glob(os.path.join(video_dir, '*.txt'))

  def redraw_fn(f, axes):
    img = imread(img_files[f])
    box = bbread(box_files[f])  # Define your own bounding box reading utility
    x, y, w, h = box
    if not redraw_fn.initialized:
      im = axes.imshow(img, animated=True)
      bb = Rectangle((x, y), w, h,
                     fill=False,  # remove background
                     edgecolor="red")
      axes.add_patch(bb)
      redraw_fn.im = im
      redraw_fn.bb = bb
      redraw_fn.initialized = True
    else:
      redraw_fn.im.set_array(img)
      redraw_fn.bb.set_xy((x, y))
      redraw_fn.bb.set_width(w)
      redraw_fn.bb.set_height(h)
  redraw_fn.initialized = False

  videofig(len(img_files), redraw_fn, play_fps=30)
```
