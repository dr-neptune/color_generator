
# Table of Contents

1.  [Rationale](#org96cbdd2)
2.  [Source](#orgaa3544f)
3.  [Usage](#org4aa67dd)
    1.  [Note](#orga9adba5)
4.  [Examples](#orge9c5a0e)
    1.  [Plotting](#orgedaed3b)
        1.  [Original Palette Line Plot](#org5a36749)
        2.  [Extended Palette Line Plot](#orgd85fc2f)
    2.  [Console](#orge58120f)
5.  [Requirements](#orgaa46b57)



<a id="org96cbdd2"></a>

# Rationale

Have you ever had a great color palette, but it didn't contain enough values to use for your (plot / website / theme / etc)?

This tool takes a color palette, and returns a set of new candidate colors that fit well


<a id="orgaa3544f"></a>

# Source

This wonderful blog post:

    https://matthewstrom.com/writing/how-to-pick-the-least-wrong-colors/

This repository takes his [code](https://github.com/ilikescience/category-colors) (written in javascript) and implements it in python.


<a id="org4aa67dd"></a>

# Usage

1.  Go to the directory
2.  Check that the [5](#orgaa46b57) are installed
3.  Add your colors to the \`run.py\` file
4.  Run it!

    python run.py

This will also show some example plots


<a id="orga9adba5"></a>

## Note

This is a probabilistic algorithm. If you don't get results you like, just run it again until you do!


<a id="orge9c5a0e"></a>

# Examples

You can run the \`plotting.py\` or \`console.py\` files to see different outputs:


<a id="orgedaed3b"></a>

## Plotting


<a id="org5a36749"></a>

### Original Palette Line Plot

![img](./Examples/original_line.png)


<a id="orgd85fc2f"></a>

### Extended Palette Line Plot

![img](./Examples/extended_line.png)

![img](./Examples/comparison_palette.png)

![img](./Examples/join_original.png)

![img](./Examples/join_extended.png)

![img](./Examples/scatter_original.png)

![img](./Examples/scatter_extended.png)


<a id="orge58120f"></a>

## Console

![img](Examples/2022-06-12_17-17-49_screenshot.png)


<a id="orgaa46b57"></a>

# Requirements

Currently too lazy to add an environment here. May update later

**Main Functionality**

    numpy, matplotlib, colormath, cytoolz

**Running Examples**

    rich, seaborn
