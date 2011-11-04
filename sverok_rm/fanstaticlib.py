""" Fanstatic lib"""
from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_common_js
from voteit.core.fanstaticlib import voteit_main_css


sverok_rm_lib = Library('sverok_rm', 'static')

sverok_rm_js = Resource(sverok_rm_lib, 'sverok_rm.js', depends=(voteit_common_js,))
sverok_rm_css = Resource(sverok_rm_lib, 'sverok_rm.css', depends=(voteit_main_css,))

sverok_rm = Group((sverok_rm_js, sverok_rm_css))
