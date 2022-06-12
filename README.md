# Palette Extender

# Table of Contents

1.  [Rationale](#org2d0ad07)
2.  [Source](#org87946d5)
3.  [Usage](#org442a880)
    1.  [Note](#org4d9ec08)
4.  [Examples](#orga5a4ab1)
    1.  [Plotting](#org8f4bfa2)
        1.  [Original Palette Line](#org9560395)
        2.  [Extended Palette Line](#org03bfcc3)
        3.  [Comparison Palettes](#org1a714ef)
        4.  [Original Palette Joint](#org009a78f)
        5.  [Extended Palette Joint](#org6bc5492)
        6.  [Original Palette Scatter](#org82ac0da)
        7.  [Extended Palette Scatter](#org1a64b80)
    2.  [Console](#orgc310b14)
5.  [Requirements](#org446235b)



<a id="org2d0ad07"></a>

# Rationale

Have you ever had a great color palette, but it didn't contain enough values to use for your (plot / website / theme / etc)?

This tool takes a color palette, and returns a set of new candidate colors that fit well


<a id="org87946d5"></a>

# Source

This wonderful blog post:

    https://matthewstrom.com/writing/how-to-pick-the-least-wrong-colors/

This repository takes his [code](https://github.com/ilikescience/category-colors) (written in javascript) and implements it in python.


<a id="org442a880"></a>

# Usage

1.  Go to the directory
2.  Check that the [5](#org446235b) are installed
3.  Add your colors to the \`run.py\` file
4.  Run it!

    python run.py

This will also show some example plots


<a id="org4d9ec08"></a>

## Note

This is a probabilistic algorithm. If you don't get results you like, just run it again until you do!


<a id="orga5a4ab1"></a>

# Examples

You can run the \`plotting.py\` or \`console.py\` files to see different outputs:


<a id="org8f4bfa2"></a>

## Plotting


<a id="org9560395"></a>

### Original Palette Line

![img](./Examples/original_line.png)


<a id="org03bfcc3"></a>

### Extended Palette Line

![img](./Examples/extended_line.png)


<a id="org1a714ef"></a>

### Comparison Palettes

![img](./Examples/comparison_palette.png)


<a id="org009a78f"></a>

### Original Palette Joint

![img](./Examples/join_original.png)


<a id="org6bc5492"></a>

### Extended Palette Joint

![img](./Examples/join_extended.png)


<a id="org82ac0da"></a>

### Original Palette Scatter

![img](./Examples/scatter_original.png)


<a id="org1a64b80"></a>

### Extended Palette Scatter

![img](./Examples/scatter_extended.png)


<a id="orgc310b14"></a>

## Console

![img](Examples/2022-06-12_17-17-49_screenshot.png)


<a id="org446235b"></a>

# Requirements

Currently too lazy to add an environment here. May update later

**Main Functionality**

    numpy, matplotlib, colormath, cytoolz

**Running Examples**

    rich, seaborn
