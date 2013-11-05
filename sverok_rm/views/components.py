from betahaus.viewcomponent import view_action


@view_action('head', 'talandewebb')
def talandewebb(context, request, va, **kw):
    return u"""<script type="text/javascript" src="http://www.talandewebb.se/ba.se.js"></script>"""
