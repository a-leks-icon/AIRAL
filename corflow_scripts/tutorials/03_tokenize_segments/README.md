# Tokenize Segments

This tutorial shows how to tokenize (split) segments.

## Introduction

The [previous tutorial](../02_copy_tiers/README.md) showed and explained how to copy existing `Tiers` and add them as either independent *root* or dependent *child* tiers to a `Transcription`. These tiers were copied and added in order to preserve their original segmentation before being altered and further processed. <!--before being altered in the upcoming tokenization--> The following tutorial will show how to (1) identify certain `Segments` based on their annotation value and (2) tokenize them. We will work with the .eaf file `doreco_teop1238_Gol_01_copied_legacy_tiers.eaf` created in the previous tutorial. Alternatively, one can just as well work with the original .eaf [`doreco_teop1238_Gol_01.eaf`](../02_copy_tiers/doreco_teop1238_Gol_01.eaf) instead.

## Starting Point

The screenshot taken of the .eaf file `doreco_teop1238_Gol_01_copied_legacy_tiers.eaf` from *Teop* from the older DoReCo version 1.2 highlights one instance of `Segments` (in a blue rectangle), which have to be tokenized: The morph *a=naa* and its gloss *OBJM=1SG.PRON* corresponding to the word *anaa*:

<img src="starting_point_mod.png" width="600" alt="Screenshot of the file 'doreco_teop1238_Gol_01_copied_legacy_tiers.eaf' from Teop from DoReCo 1.2 showing one instance of problematic segments, which have to be tokenized.">

Both segments contain two separate units: *a=naa* contains the proclitic *a=* and the root *naa* with their respective glosses being *OBJM=* and *1SG.PRON*. Each segment has to be split into two separate segments (highlighted by green and red rectangles), such that each morph and gloss constitutes its own segment. But what does *splitting* a segment mean in particular? The next section [*Excursus: Concept behind Splitting a Segment*](#excursus-concept-behind-splitting-a-segment) answers this question. The section [*Splitting a Segment*](#splitting-a-segment) right after the next one instead explains how to use the `split_seg()` function located in the [`general_functions.py`](../../general_functions.py) script in order to split a segment.

## Excursus: Concept behind Splitting a Segment

Splitting a segment involves (1) adding a new segment next to the current segment and adjusting the (2) content (annotation value) as well as the (3) start and end time of the new and current segment. Furthermore, when adding a segment, the (4) child and parent segments of the new segment have to be established. Lastly, depending on the hierarchy of the tier, (5) additional new segments may have to be added, if the tier has child tiers. In what follows, I will go through each step involved when splitting a segment and explain it.

When we (1) add a new segment, we create a new `Segment` object and insert it into the list of elements of a `Tier`. In our particular example, we would add a new `Segment` on the morph tier and another one on the gloss tier right next to the segments *a=naa* and *OBJM=1SG.PRON*. Having added new segments, (2) we would have to define the content of the new segments and potentially also those of the old segments. In our particular example, we would split the content of each old segment after the equal sign. We would end up having two segments on the morph tier defined as *a=* and *naa* as well as two segments on the gloss tier defined as *OBJM=* and *1SG.PRON*.

Next, there are two approaches for how to (3) adjust the time of the old and new segments. One approach is to equally distribute the time of the old segment among the old and new segment by splitting the time of the old segment in half. This is what ELAN does when creating segments. While this approach makes sense in many cases, it is not useful in our particular example. Taking a look at the phone tier reveals why: The time of the segments on the phone tier, which represent phones (the smallest acoustic units), is *not* equally distributes among them: The time of the phone [a] corresponding to the morph *a=* is different compared to the unified time of the phones [n] and [aː] corresponding to the morph *naa*. In the case of DoReCo, the phones and their time dictate the duration of the other units (morphs, glosses and words). That is why, in our particular example, the time of the morph *a=* and gloss *OBJM=* should be set equal to the time of the phone [a], and the time of the morph *naa* and gloss *1SG.PRON* should be set equal to the unified time of the phones [n] and [aː].

<!--Take a look at the previous screenshot and consider the hierarchy of the tiers, whose segments we want to split there: The morph tier is a child tier of the word tier and the parent tier of the (1) gloss, (2) phone and (3) special *doreoco-mb-algn@* tier. When we add a new segment on the morph tier and one on the gloss tier, we want the new segment on the morph tier to be a child segment of the word segment *anaa* and at the same time be a parent segment of the new segment on the gloss tier. In other words, we have to consider-->

When splitting a segment and thereby adding a new segment, its (4) parent and child segments have to be defined. One way of doing this would be to simply use the old segment's parent and child segments as the new segment's parent and child segments. However, this would only work in part: In ELAN (and generally in linguistic structures), while a parent segment can have multiple child segments (on the same and/or different tiers), a child segment can only have one parent segment. Additionally, when a new segment is added, the time of the old and new segment is changed.

*to be continued*

<!--In theory, there may be scenarios, where definiens and definiendum are reversed: the time of a segment is defined based on its relation to its parent





 the parent and child segments of the new segment will be located based on the time of the new segment.

As it is, when splitting a segment, the times of the old and new segment will not go beyond the original time of the old segment (and the old segment's parent). That is why, (4) the parent segment of the old segment will also be the parent of the new segment. In our example, the word *anaa* will be the parent segment of the left segment *a=* and the new, right segment *naa*. However, ....: -->

## Splitting a Segment