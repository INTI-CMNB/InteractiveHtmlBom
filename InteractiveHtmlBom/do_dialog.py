import os
import sys
# Look for the 'dialog' module from where the script is running
cur_dir = os.path.dirname(os.path.abspath(__file__))
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from dialog.settings_dialog import *


class MyApp(wx.App):
    def OnInit(self):
        frame = SettingsDialog(lambda: None, None, lambda x: None, "Hi", 'test')
        if frame.ShowModal() == wx.ID_OK:
            print("Should generate bom")
        frame.Destroy()
        return True


app = MyApp()
app.MainLoop()

print("Done")
