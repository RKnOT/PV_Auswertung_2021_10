
import pyto_ui as ui
#import sy_symbols as sf

image = ui.ImageView(symbol_name=sf.PERSON_CIRCLE)







'''
#-----------
from UIKit import *
from LinkPresentation import *
from Foundation import *
from rubicon.objc import *
from mainthread import mainthread
import pyto_ui as ui

# We subclass UIViewController
class MyViewController(UIViewController):

    @objc_method
    def close(self):
        self.dismissViewControllerAnimated(True, completion=None)

    @objc_method
    def dealloc(self):
        self.link_view.release()

    # Overriding viewDidLoad
    @objc_method
    def viewDidLoad(self):
        send_super(__class__, self, "viewDidLoad")

        self.title = "Link"

        self.view.backgroundColor = UIColor.systemBackgroundColor()

        # 0 is the value for a 'Done' button
        done_button = UIBarButtonItem.alloc().initWithBarButtonSystemItem(0, target=self, action=SEL("close"))
        self.navigationItem.rightBarButtonItems = [done_button]

        self.url = NSURL.alloc().initWithString("https://apple.com")
        self.link_view = LPLinkView.alloc().initWithURL(self.url)
        self.link_view.frame = CGRectMake(0, 0, 200, 000)
        self.view.addSubview(self.link_view)
        self.fetchMetadata()

    @objc_method
    def fetchMetadata(self):

        @mainthread
        def set_metadata(metadata):
            self.link_view.setMetadata(metadata)
            self.layout()

        def fetch_handler(metadata: ObjCInstance, error: ObjCInstance) -> None:
             set_metadata(metadata)

        provider = LPMetadataProvider.alloc().init().autorelease()
        provider.startFetchingMetadataForURL(self.url, completionHandler=fetch_handler)

    @objc_method
    def layout(self):
        self.link_view.sizeToFit()
        self.link_view.setCenter(self.view.center)

    @objc_method
    def viewDidLayoutSubviews(self):
        self.layout()

@mainthread
def show():
    # We initialize our view controller and a navigation controller
    # This must be called from the main thread
    vc = MyViewController.alloc().init().autorelease()
    nav_vc = UINavigationController.alloc().initWithRootViewController(vc).autorelease()
    ui.show_view_controller(nav_vc)

show()
'''
a=6
'''
#-------- date picker
import pyto_ui as ui
from UIKit import UIDatePicker
from Foundation import NSObject
from rubicon.objc import objc_method, SEL
from datetime import datetime

# We subclass ui.UIKitView to implement a date picker
class DatePicker(ui.UIKitView):

    did_change = None

    # Here we return an UIDatePicker object
    def make_view(self):
        picker = UIDatePicker.alloc().init()

         # We create an Objective-C instance that will respond to the date picker value changed event
        delegate = PickerDelegate.alloc().init()
        delegate.picker = self
        delegate.objc_picker = picker

        # 4096 is the value for UIControlEventValueChanged
        picker.addTarget(delegate, action=SEL("didChange"), forControlEvents=4096)
        return picker

# An Objective-C class for addTarget(_:action:forControlEvents:)
class PickerDelegate(NSObject):

    picker = None

    @objc_method
    def didChange(self):
        if self.picker.did_change is not None:
            date = self.objc_picker.date
            date = datetime.fromtimestamp(date.timeIntervalSince1970())
            self.picker.did_change(date)

# Then we can use our date picker as any other view

view = ui.View()
view.background_color = ui.COLOR_SYSTEM_BACKGROUND

def did_change(date):
    view.title = str(date)

date_picker = DatePicker()
date_picker.did_change = did_change

date_picker.flex = [
    ui.FLEXIBLE_BOTTOM_MARGIN,
    ui.FLEXIBLE_TOP_MARGIN,
    ui.FLEXIBLE_LEFT_MARGIN,
    ui.FLEXIBLE_RIGHT_MARGIN
]
date_picker.center = view.center
view.add_subview(date_picker)

ui.show_view(view, ui.PRESENTATION_MODE_SHEET)
'''
a =1

'''
#----------ui button------------
import pyto_ui as ui

def button_pressed(sender):
    sender.superview.close()

view = ui.View()
view.background_color = ui.COLOR_SYSTEM_BACKGROUND

button = ui.Button(title="Hello World!")
button.size = (100, 50)
button.center = (view.width/2, view.height/2)
button.flex = [
    ui.FLEXIBLE_TOP_MARGIN,
    ui.FLEXIBLE_BOTTOM_MARGIN,
    ui.FLEXIBLE_LEFT_MARGIN,
    ui.FLEXIBLE_RIGHT_MARGIN
]
button.action = button_pressed
view.add_subview(button)

ui.show_view(view, ui.PRESENTATION_MODE_SHEET)

print("Hello World!")

'''