# Color Palette Extender

# Table of Contents

1.  [Rationale](#org51511fd)
2.  [Source](#orgaafc768)
3.  [Usage](#org0d08d70)
    1.  [Note](#orgfc4b528)
4.  [Examples](#org7a6ca94)
    1.  [Plotting](#orgf02b6a8)
        1.  [Original Palette Line](#orgaf84ce4)
        2.  [Extended Palette Line](#org8cd3d43)
        3.  [Comparison Palettes](#orgd7594ab)
        4.  [Original Palette Joint](#org28941d8)
        5.  [Extended Palette Joint](#org9aa0ddf)
        6.  [Original Palette Scatter](#org8d2bf89)
        7.  [Extended Palette Scatter](#org16483b1)
    2.  [Console](#org70bd9fd)
5.  [Requirements](#orgbcd827e)



<a id="org51511fd"></a>

# Rationale

Have you ever had a great color palette, but it didn't contain enough values to use for your (plot / website / theme / etc)?

This tool takes a color palette, and returns a set of new candidate colors that fit well


<a id="orgaafc768"></a>

# Source

This wonderful blog post:

    https://matthewstrom.com/writing/how-to-pick-the-least-wrong-colors/

This repository takes his [code](https://github.com/ilikescience/category-colors) (written in javascript) and implements it in python.


<a id="org0d08d70"></a>

# Usage

1.  Go to the directory
2.  Check that the Requirements: [5](#orgbcd827e) are installed
3.  Add your colors to the \`run.py\` file
4.  Run it!

    python run.py

This will also show some example plots


<a id="orgfc4b528"></a>

## Note

This is a probabilistic algorithm. If you don't get results you like, just run it again until you do!


<a id="org7a6ca94"></a>

# Examples

You can run the \`plotting.py\` or \`console.py\` files to see different outputs:


<a id="orgf02b6a8"></a>

## Plotting


<a id="orgaf84ce4"></a>

### Original Palette Line

![img](./Examples/original_line.png)


<a id="org8cd3d43"></a>

### Extended Palette Line

![img](./Examples/extended_line.png)


<a id="orgd7594ab"></a>

### Comparison Palettes

![img](./Examples/comparison_palette.png)


<a id="org28941d8"></a>

### Original Palette Joint

![img](./Examples/join_original.png)


<a id="org9aa0ddf"></a>

### Extended Palette Joint

![img](./Examples/join_extended.png)


<a id="org8d2bf89"></a>

### Original Palette Scatter

![img](./Examples/scatter_original.png)


<a id="org16483b1"></a>

### Extended Palette Scatter

![img](./Examples/scatter_extended.png)


<a id="org70bd9fd"></a>

## Console

![img](Examples/2022-06-12_17-17-49_screenshot.png)


<a id="orgbcd827e"></a>

# Requirements

Currently too lazy to add an environment here. May update later

**Main Functionality**

    numpy, matplotlib, colormath, cytoolz

**Running Examples**

    rich, seaborn
