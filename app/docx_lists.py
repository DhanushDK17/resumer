def _xpath_options(level):
    return {
        True: {"single": "count(w:lvl)=1 and ", "level": 0},
        False: {"single": "", "level": level},
    }


def _style_xpath(style_id, level, prefer_single=True):
    options = _xpath_options(level)[prefer_single]
    return (
        'w:abstractNum['
        '{single}w:lvl[@w:ilvl="{level}"]/w:pStyle[@w:val="{style}"]'
        ']/@w:abstractNumId'
    ).format(style=style_id, **options)


def _type_xpath(list_type, level, prefer_single=True):
    options = _xpath_options(level)[prefer_single]
    return (
        'w:abstractNum['
        '{single}w:lvl[@w:ilvl="{level}"]/w:numFmt[@w:val="{type}"]'
        ']/@w:abstractNumId'
    ).format(type=list_type, **options)


def _get_abstract_id(numbering, style_id, level, list_type):
    for fn in (_style_xpath, _type_xpath):
        for prefer_single in (True, False):
            if fn is _style_xpath:
                xpath = fn(style_id, level, prefer_single)
            else:
                xpath = fn(list_type, level, prefer_single)
            ids = numbering.xpath(xpath)
            if ids:
                return min(int(x) for x in ids)
    return 0


def list_number(doc, par, prev=None, level=None, num=True):
    """
    Makes a paragraph into a list item with a specific level and optional restart.
    """

    if (
        prev is None
        or prev._p.pPr is None
        or prev._p.pPr.numPr is None
        or prev._p.pPr.numPr.numId is None
    ):
        if level is None:
            level = 0
        numbering = doc.part.numbering_part.numbering_definitions._numbering
        style_id = par.style.style_id
        list_type = "decimal" if num else "bullet"
        anum = _get_abstract_id(numbering, style_id, level, list_type)
        num = numbering.add_num(anum)
        num.add_lvlOverride(ilvl=level).add_startOverride(1)
        num = num.numId
    else:
        if level is None:
            level = prev._p.pPr.numPr.ilvl.val
        num = prev._p.pPr.numPr.numId.val
    par._p.get_or_add_pPr().get_or_add_numPr().get_or_add_numId().val = num
    par._p.get_or_add_pPr().get_or_add_numPr().get_or_add_ilvl().val = level
