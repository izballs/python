from gi.repository import Gio, Gdk
import time
gsettings_path = 'org.gnome.desktop.background'
gsettings = Gio.Settings.new(gsettings_path)
while True:
    gsettings.set_string('picture-uri', 'file://{}'.format("./fullImage.jpg"))
    gsettings.set_string('picture-options', 'Span')
    time.sleep(0.2)
