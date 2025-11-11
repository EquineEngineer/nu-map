# USBClass.py
#
# Contains class definition for USBClass, intended as a base class (in the OO
# sense) for implementing device classes (in the USB sense), eg, HID devices,
# mass storage devices.
from numap.core.usb_base import USBBaseActor


class USBClass(USBBaseActor):
    name = "Class"

    Unspecified = 0x00
    Audio = 0x01
    CDC = 0x02
    HID = 0x03
    PID = 0x05
    Image = 0x06
    Printer = 0x07
    MassStorage = 0x08
    Hub = 0x09
    CDCData = 0x0A
    SmartCard = 0x0B
    ContentSecurity = 0x0D
    Video = 0x0E
    PHDC = 0x0F
    AudioVideo = 0x10
    Billboard = 0x11
    DiagnosticDevice = 0xDC
    WirelessController = 0xE0
    Miscellaneous = 0xED
    ApplicationSpecific = 0xFE
    VendorSpecific = 0xFF

    def __init__(self, app, phy):
        """
        :param app: nümap application
        :param phy: Physical connection
        """
        super(USBClass, self).__init__(app, phy)
        self.setup_request_handlers()
        self.device = None
        self.interface = None
        self.endpoint = None

    def setup_request_handlers(self):
        self.setup_local_handlers()
        self.request_handlers = {x: self._global_handler for x in self.local_handlers}

    def setup_local_handlers(self):
        self.local_handlers = {}

    def _global_handler(self, req):
        handler = self.local_handlers[req.request]
        response = handler(req)
        if response is not None:
            self.phy.send_on_endpoint(0, response)
        self.usb_function_supported("class specific setup request received")

    def default_handler(self, req):
        self._global_handler(req)
