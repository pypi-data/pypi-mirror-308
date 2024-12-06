from pyTRADE.core.wrapper import TRADEWrapper
from ai.thinkingrobots.trade import TRADE


if __name__ == '__main__':
    wrapper = TRADEWrapper()
    print(TRADE.getAvailableServices())
    # wrapper.call_trade("moveto", 1, 3, 4)
