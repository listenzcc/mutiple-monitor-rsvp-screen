# %%
import time
import threading

from . import setPortAddress, setData

# %%


class Parallel(object):
    def __init__(self, address):
        self.reset(str(address))

    def reset(self, address):
        self.address = address
        address_hex = int(address, 16)
        setPortAddress(address_hex)
        setData(0)
        self.latest = 0

    def send(self, value, verbose=False):
        if self.address is None:
            print('Send failed since the Parallel is not set')
            return

        t = threading.Thread(target=self._send, args=(value, verbose))
        t.setDaemon(True)
        t.start()

        return time.time()

    def _send(self, value, verbose):
        setData(int(value))
        time.sleep(0.001)
        setData(0)

        if verbose:
            print(f'Sent: {value} to {self.address}')
