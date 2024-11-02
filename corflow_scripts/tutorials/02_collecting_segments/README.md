# Collecting Segments

This tutorial shows how to collect `Segment` objects based on various features. Each code snipped presented in this tutorial can be used in its own .py file.

## What, Why and How?

`Segment` objects lie at the heart of a `Transcription`: They represent (linguistic or other) information with time points. As such, they can be collected (and manipulated) based on a variety of features, the most important of which are the following:

* **Time**: Represented by the `.start` and `.end` attributes.
* **Content**: Represented by the `.content` attribute.
* **Hierarchical Relations**: Represented by the `.parent()`, `.children()` and similar methods.

There are two ways to write scripts collecting (and manipulating) segments: (1) Using Corflow itself or (2) using the `get_segs()` function from [`general_functions.py`](../../general_functions.py) created on top of Corflow. In what follows, I will show how to collect segments based on various features using both methods and explain the pros and cons in using either of them. But first, I start with explaining the Syntax of using `get_segs()`.

## How to use `get_segs()`

In order to use `get_segs()`, it has to be imported from `general_functions.py` within a Python script in addition to Corflow (visit the [first tutorial](../00_getting_started/README.md#general-functions) to get more information about importing `general_functions.py`):

```python
from general_functions import get_segs
```

`get_segs()` consists of four parameters:

* **trans**: The `Transcription` object.
* **tier_re**: The regular expression used to identify tiers, whose segments will be collected.
* **\*conditions**: Conditions used to restrict, which segments will be collected.
* **\*\*options**: Additional settings using specific names as keys and strings as values.

The first two parameters are straightforward. The third parameter consists of a number of lists or tuples, depending on the number of conditions you have. Each condition is itself made up of up to four different elements:

1. A regular expression used to identify tiers, whose segments are used to create restrictions.
2. Optional: A string containing keywords to identify the *name of a condition type* segments to be collected have to fulfill.
3. Optional: A regular expression used to restrict, which segments will be collected. A segment's `.content` attribute has to match that regular expression.
4. Optional: Using `False` to negate the condition type.

## Collecting Segments based on various Features

### Time