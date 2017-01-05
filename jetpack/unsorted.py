# -*- coding: utf-8 -*-
def fonts():
    import matplotlib.font_manager as fm
    return sorted(set([f.name for f in fm.fontManager.ttflist]))
