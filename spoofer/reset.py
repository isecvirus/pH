from controller.reroute import reset
from spoofer.spoof import spoofed
from utils.debug import dbg, WARNING, SUCCESS, INFO


def spoofer_reset():
    if len(spoofed) > 0:
        dbg("Resetting routing..", WARNING)

        for item in spoofed:
            src = spoofed[item]['info'][0]
            dest = spoofed[item]['info'][1]
            reset(src, dest)
            dbg("Rerouted 'Target: %s > Destination: %s'" % (src, dest), INFO)
            reset(dest, src)
            dbg("Rerouted 'Destination: %s > Target: %s'" % (dest, src), INFO)
        dbg("All done.", SUCCESS)