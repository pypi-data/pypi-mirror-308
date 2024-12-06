from pyTRADE.core.wrapper import TRADEWrapper
from ai.thinkingrobots.trade import TRADE
from jpype import JImplements, JOverride, JClass
from edu.tufts.hrilab.interfaces import DockingInterface, MoveBaseInterface, ArmInterface


@JImplements(DockingInterface)
class dummyWrapper:
    @JOverride
    def dock(self, dockId):
        mo = wrapper.call_trade("getEntityForReference", dockId,
                                JClass("edu.tufts.hrilab.vision.stm.MemoryObject"))
        pass

    @JOverride
    def undock(self):
        pass

if __name__ == '__main__':
    wrapper = TRADEWrapper()
    dummyObject = dummyWrapper()
    TRADE.registerAllServices(dummyObject, "")
    dummyObject.dock("")
