# Collecting Segments

This tutorial shows how to collect `Segment` objects based on different features. Each code snipped presented in this tutorial can be used in its own .py file.

## What, Why and How?

`Segment` objects lie at the heart of a `Transcription`: They represent (linguistic or other) information with time points. As such, they can be collected (and manipulated) based on a variety of features, the most important of which are the following:

* **Time**: Represented by the `.start` and `.end` attributes.
* **Content**: Represented by the `.content` attribute.
* **Hierarchical Relations**: Represented by the `.parent()`, `.children()` and similar methods.

There are two ways to write scripts collecting (and manipulating) segments: (1) Using Corflow itself or (2) using the `get_segs()` function from [`general_functions.py`](../../general_functions.py) created on top of Corflow. In what follows, I will show how to collect segments based on various features using both methods and explain the pros and cons in using either of them.

## General Functions: `get_segs()`

