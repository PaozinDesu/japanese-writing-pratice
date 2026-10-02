from common import *

def mheader(title, right=None):
    return ('<header style="position:relative;width:390px;height:72px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;padding:12px 20px 4px;">'
            '<h1 class="disp" style="margin:0;font-size:28px;font-weight:700;">' + title + '</h1>' + (right if right is not None else macct()) + '</header>')

def tabbar_m(active):
    return tabbar(active)
