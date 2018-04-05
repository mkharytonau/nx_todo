class MyWin (Gtk.Window):
    def __init__(self):
        super(MyWin, self).__init__()
        self.set_opacity(0.93)
        self.set_default_size(300, 100)
        s = Gdk.Screen.get_default()
        self.set_decorated(False)
        self.move(s.get_width() - 320, 50)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual != None and self.screen.is_composited():
            print("yay")
            self.set_visual(self.visual)


        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)
        self.show_all()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(float(130/255), float(113/255), float(78/255), 1)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

MyWin()
Gtk.main()


win = Gtk.Window()
win.set_position(Gtk.WindowPosition.MOUSE)
win.set_decorated(True)
win.set_default_size(300, 100)
win.set_opacity(0.5)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()