__version__ = '2.7.8'

import mke_sculib.scu 
from mke_sculib.scu import scu as scu_api
from mke_sculib.scu import plot_tt, print_color, colors, log, link_stellarium, activate_logging_mattermost
from mke_sculib.sim import scu_sim
from mke_sculib.stellarium_api import stellarium_api as stellar_api
from mke_sculib.sim import plot_motion_pyplot as plot_motion
from mke_sculib.helpers import get_utcnow, make_zulustr, parse_zulutime



def load(antenna_id='', post_put_delay=0.0, debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):

    if not "requests" in locals():
        import requests
    if not "json" in locals():
        import json

    if not isinstance(antenna_id, str):
        antenna_id = str(antenna_id)
    

    if antenna_id == 'test_antenna' or antenna_id == 'sim':
        return scu_sim(antenna_id, debug=debug, **kwargs)
    else:
        return scu_api.load(antenna_id, post_put_delay=post_put_delay, debug=debug, url_qry=url_qry, **kwargs)