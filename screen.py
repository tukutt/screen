import usys as sys
import lvgl as lv
import time
import fs_driver
from lv_utils import event_loop

sys.path.append('') # See: https://github.com/micropython/micropython/issues/6419

# Use to load font
try:
    script_path = __file__[:__file__.rfind('/')] if __file__.find('/') >= 0 else '.'
except NameError:
    script_path = ''


# FS driver init.
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, 'S')

# Load font
font_numberfont60 = lv.font_load("S:%s/assets/ui_font_numberfont80.bin" % script_path)

value = 0 # Time bar

# See: https://pymotw.com/2/sys/tracing.html

def mp_trace(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    print('[%s] [%s] %s:%s' % (event, func_name, func_filename, func_line_no))
    return mp_trace

def event_handler(evt):
    code = evt.get_code()

    if code == lv.EVENT.CLICKED:
            print("Clicked event seen")
    elif code == lv.EVENT.VALUE_CHANGED:
        print("Value changed seen")

# sys.settrace(mp_trace)



# lvgl must be initialized before any lvgl function is called or object/struct is constructed!

lv.init()


def SetFlag( obj, flag, value):
    if (value):
        obj.add_flag(flag)
    else:
        obj.clear_flag(flag)
    return

def ModifyFlag( obj, flag, value):
    if (value=="TOGGLE"):
        if ( obj.has_flag(flag) ):
            obj.clear_flag(flag)
        else:
            obj.add_flag(flag)
        return

    if (value=="ADD"):
        obj.add_flag(flag)
    else:
        obj.clear_flag(flag)
    return

def ModifyState( obj, state, value):
    if (value=="TOGGLE"):
        if ( obj.has_state(state) ):
            obj.clear_state(state)
        else:
            obj.add_state(state)
        return

    if (value=="ADD"):
        obj.add_state(state)
    else:
        obj.clear_state(state)
    return

def set_opacity(obj, v):
    obj.set_style_opa(v, lv.STATE.DEFAULT|lv.PART.MAIN)
    return

def SetPanelProperty(target, id, val):
   if id == 'Position_X': target.set_x(val)
   if id == 'Position_Y': target.set_y(val)
   if id == 'Width': target.set_width(val)
   if id == 'Height': target.set_height(val)
   return

def popup_display_Animation(TargetObject, delay):
  PropertyAnimation_0 = lv.anim_t()
  PropertyAnimation_0.init()
  PropertyAnimation_0.set_path_cb(lv.anim_t.path_ease_in_out)
  PropertyAnimation_0.set_time(300)
  PropertyAnimation_0.set_var(TargetObject)
  PropertyAnimation_0.set_custom_exec_cb(lambda a, v: TargetObject.set_y(v))
  PropertyAnimation_0.set_delay(delay + 0)
  PropertyAnimation_0.set_repeat_count(0)
  PropertyAnimation_0.set_repeat_delay(0) #+ 500
  PropertyAnimation_0.set_playback_delay(0)
  PropertyAnimation_0.set_playback_time(0)
  PropertyAnimation_0.set_early_apply(False)
  PropertyAnimation_0.set_values(-500, -20)
  lv.anim_t.start(PropertyAnimation_0)

  print ("popup_display_Animation called")
  return

def popup_hidden_Animation(TargetObject, delay):
  PropertyAnimation_0 = lv.anim_t()
  PropertyAnimation_0.init()
  PropertyAnimation_0.set_path_cb(lv.anim_t.path_ease_in_out)
  PropertyAnimation_0.set_time(500)
  PropertyAnimation_0.set_var(TargetObject)
  PropertyAnimation_0.set_custom_exec_cb(lambda a, v: TargetObject.set_style_opa(v,0))
  PropertyAnimation_0.set_delay(delay + 0)
  PropertyAnimation_0.set_repeat_count(0)
  PropertyAnimation_0.set_repeat_delay(0) #+ 1000
  PropertyAnimation_0.set_playback_delay(0)
  PropertyAnimation_0.set_playback_time(0)
  PropertyAnimation_0.set_early_apply(False)
  PropertyAnimation_0.set_values(255, 0)
  lv.anim_t.start(PropertyAnimation_0)
  PropertyAnimation_1 = lv.anim_t()
  PropertyAnimation_1.init()
  PropertyAnimation_1.set_path_cb(lv.anim_t.path_linear)
  PropertyAnimation_1.set_time(500)
  PropertyAnimation_1.set_var(TargetObject)
  PropertyAnimation_1.set_custom_exec_cb(lambda a, v: TargetObject.set_y(v))
  PropertyAnimation_1.set_delay(delay + 500)
  PropertyAnimation_1.set_repeat_count(0)
  PropertyAnimation_1.set_repeat_delay(0) #+ 1000
  PropertyAnimation_1.set_playback_delay(0)
  PropertyAnimation_1.set_playback_time(0)
  PropertyAnimation_1.set_early_apply(False)
  PropertyAnimation_1.set_values(0, -500)
  lv.anim_t.start(PropertyAnimation_1)

  print ("popup_hidden_Animation called")
  return


member_name_cache = {}

def get_member_name(obj, value):
    try:
        return member_name_cache[id(obj)][id(value)]
    except KeyError:
        pass

    for member in dir(obj):
        if getattr(obj, member) == value:
            try:
                member_name_cache[id(obj)][id(value)] = member
            except KeyError:
                member_name_cache[id(obj)] = {id(value): member}
            return member


class SymbolButton(lv.btn):
    def __init__(self, parent, symbol, text):
        super().__init__(parent)
        self.symbol = lv.label(self)
        self.symbol.set_text(symbol)
        self.label = lv.label(self)
        self.label.set_text(text)
        self.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)


class Page_Buttons:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.btn_event_count = {'Play': 0, 'Pause': 0}

        self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.START)

        self.btn1 = SymbolButton(page, lv.SYMBOL.PLAY, "Play")
        self.btn1.set_size(80, 80)

        self.btn2 = SymbolButton(page, lv.SYMBOL.PAUSE, "Pause")
        self.btn2.set_size(80, 80)

        self.label = lv.label(page)
        self.label.add_flag(lv.obj.FLAG.IGNORE_LAYOUT)
        self.label.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)

        def button_cb(event, name):
            self.btn_event_count[name] += 1
            event_name = get_member_name(lv.EVENT, event.code)
            if all((not event_name.startswith(s)) for s in ['DRAW', 'GET', 'STYLE', 'REFR']):
                self.label.set_text('[%d] %s %s' % (self.btn_event_count[name], name, event_name))

        for btn, name in [(self.btn1, 'Play'), (self.btn2, 'Pause')]:
            btn.add_event_cb(lambda event, btn_name=name: button_cb(event, btn_name), lv.EVENT.ALL, None)


class Page_Receipe_old:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.test_events = []

        self.page.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)

        # slider
        self.slider = lv.slider(page)
        self.slider.set_width(lv.pct(80))
        self.slider_label = lv.label(page)
        self.slider.add_event_cb(self.on_slider_changed, lv.EVENT.VALUE_CHANGED, None)
        self.on_slider_changed(None)

       
    
        self.style_selector = lv.dropdown(page)
        self.style_selector.align(lv.ALIGN.OUT_BOTTOM_LEFT, 0, 40)
        self.style_selector.set_options('\n'.join(x[0] for x in self.styles))
        self.style_selector.add_event_cb(self.on_style_selector_changed, lv.EVENT.VALUE_CHANGED, None)

        # counter button
        self.counter_btn = lv.btn(page)
        self.counter_btn.set_size(80,80)
        self.counter_label = lv.label(self.counter_btn)
        self.counter_label.set_text("Count")
        self.counter_label.align(lv.ALIGN.CENTER, 0, 0)
        self.counter_btn.add_event_cb(self.on_counter_btn, lv.EVENT.CLICKED, None)
        self.counter = 0

    def on_slider_changed(self, event):
        self.slider_label.set_text(str(self.slider.get_value()))

    def on_style_selector_changed(self, event):
        selected = self.style_selector.get_selected()
        tabview = self.app.screen_main.tabview
        if hasattr(self, 'selected_style'): tabview.remove_style(self.selected_style, lv.PART.MAIN)
        self.selected_style = self.styles[selected][1]
        tabview.add_style(self.selected_style, lv.PART.MAIN)

    def on_counter_btn(self, event):
        self.counter += 1
        self.counter_label.set_text(str(self.counter))

class Anim(lv.anim_t):
    def __init__(self, obj, val, size, exec_cb, path_cb, time=500, playback=False, ready_cb=None):
        super().__init__()
        self.init()
        self.set_time(time)
        self.set_values(val, val + size)
        if callable(exec_cb):
            self.set_custom_exec_cb(exec_cb)
        else:
            self.set_exec_cb(obj, exec_cb)
        self.set_path_cb(path_cb)
        if playback:
            self.set_playback(0)
        if ready_cb:
            self.set_ready_cb(ready_cb)
        self.start()
        

class AnimatedChart(lv.chart):
    def __init__(self, parent, val, size):
        super().__init__(parent)
        self.val = val
        self.size = size
        self.max = 2000
        self.min = 500
        self.factor = 100
        self.anim_phase1()

    def anim_phase1(self):
        self.phase1 = Anim(
            self,
            self.val,
            self.size,
            lambda a, val: self.set_range(self.AXIS.PRIMARY_Y, 0, val),
            lv.anim_t.path_ease_in,
            ready_cb=lambda a:self.anim_phase2(),
            time=(self.max * self.factor) // 100,
        )

    def anim_phase2(self):
        self.phase2 = Anim(
            self,
            self.val + self.size,
            -self.size,
            lambda a, val: self.set_range(self.AXIS.PRIMARY_Y, 0, val),
            lv.anim_t.path_ease_out,
            ready_cb=lambda a:self.anim_phase1(),
            time=(self.min * self.factor) // 100,
        )
class Page_Text:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.ta = lv.textarea(self.page)
        self.ta.set_height(lv.pct(100))
        self.ta.set_width(lv.pct(100))

class Page_Receipe:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.page.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.page.set_flex_align(lv.FLEX_ALIGN.SPACE_EVENLY, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.page.set_style_pad_all(10, lv.PART.MAIN)
        self.page.set_style_pad_gap(10, lv.PART.MAIN)
        self.chart = AnimatedChart(page, 100, 1000)
        self.chart.set_flex_grow(1)
        self.chart.set_height(lv.pct(100))
        self.series1 = self.chart.add_series(lv.color_hex(0xFF0000), self.chart.AXIS.PRIMARY_Y)
        self.chart.set_type(self.chart.TYPE.LINE)
        self.chart.set_style_line_width(3, lv.PART.ITEMS)
        # self.chart.add_style(ColorStyle(0x055), lv.PART.ITEMS)
        self.chart.set_range(self.chart.AXIS.PRIMARY_Y, 0, 100)
        self.chart.set_point_count(10)
        self.chart.set_ext_y_array(self.series1, [10, 20, 30, 20, 10, 40, 50, 90, 95, 90])
        # self.chart.set_x_tick_texts("a\nb\nc\nd\ne", 2, lv.chart.AXIS.DRAW_LAST_TICK)
        # self.chart.set_x_tick_length(10, 5)
        # self.chart.set_y_tick_texts("1\n2\n3\n4\n5", 2, lv.chart.AXIS.DRAW_LAST_TICK)
        # self.chart.set_y_tick_length(10, 5)
        self.chart.set_div_line_count(5, 5)

        # Create a slider that controls the chart animation speed

        def on_slider_changed(event):
            self.chart.factor = self.slider.get_value()

        self.slider = lv.slider(page)
        self.slider.set_size(10, lv.pct(100))
        self.slider.set_range(10, 200)
        self.slider.set_value(self.chart.factor, 0)
        self.slider.add_event_cb(on_slider_changed, lv.EVENT.VALUE_CHANGED, None)


class Page_Pellet:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        print("Page_Pellet")


class Page_Dashboard:
    def __init__(self, app, page):
        self.app = app
        self.page = page

        # Page style
        SetFlag(self.page, lv.obj.FLAG.SCROLLABLE, False)
        self.page.set_style_bg_color( lv.color_hex(0x464B55), lv.PART.MAIN | lv.STATE.DEFAULT )
        self.page.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        self.page.set_style_bg_grad_color( lv.color_hex(0x2D323C), lv.PART.MAIN | lv.STATE.DEFAULT )

        ## Grill Temp widget
        ui_Arc_Group = lv.obj(self.page)
        ui_Arc_Group.set_width(400)
        ui_Arc_Group.set_height( 400)
        ui_Arc_Group.set_align( lv.ALIGN.CENTER )
        SetFlag(ui_Arc_Group, lv.obj.FLAG.SCROLLABLE, False)
        ui_Arc_Group.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Arc_Group.set_style_bg_opa(0, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc_Group.set_style_border_width(0, lv.PART.MAIN| lv.STATE.DEFAULT)


        ui_Arc1 = lv.arc(ui_Arc_Group)
        ui_Arc1.set_width(  350)
        ui_Arc1.set_height( 350)
        ui_Arc1.set_align(  lv.ALIGN.CENTER )
        ui_Arc1.set_range( 15,35)
        ui_Arc1.set_value( 23)
        ui_Arc1.set_style_radius( 350, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_bg_color( lv.color_hex(0x1E232D), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Arc1.set_style_bg_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_pad_left( 10, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_pad_right( 10, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_pad_top( 10, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_pad_bottom( 10, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_arc_color( lv.color_hex(0x0F1215), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Arc1.set_style_arc_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_arc_width( 15, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Arc1.set_style_arc_color( lv.color_hex(0x36B9F6), lv.PART.INDICATOR | lv.STATE.DEFAULT )
        ui_Arc1.set_style_arc_opa( 255, lv.PART.INDICATOR| lv.STATE.DEFAULT)
        ui_Arc1.set_style_arc_width( 15, lv.PART.INDICATOR| lv.STATE.DEFAULT)
        ui_Arc1.set_style_bg_color( lv.color_hex(0xFFFFFF), lv.PART.KNOB | lv.STATE.DEFAULT )
        ui_Arc1.set_style_bg_opa( 0, lv.PART.KNOB| lv.STATE.DEFAULT)

        ui_Temp_Bg = lv.obj(ui_Arc_Group);
        ui_Temp_Bg.set_width(  280);
        ui_Temp_Bg.set_height(  280);
        ui_Temp_Bg.set_align(  lv.ALIGN.CENTER );
        SetFlag(ui_Temp_Bg, lv.obj.FLAG.SCROLLABLE, False)

        ui_Temp_Bg.set_style_radius( 280, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_bg_color( lv.color_hex(0x646464), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Bg.set_style_bg_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_bg_grad_color( lv.color_hex(0x3C414B), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Bg.set_style_bg_grad_dir( lv.GRAD_DIR.VER, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_border_color( lv.color_hex(0x2D323C), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Bg.set_style_border_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_border_width( 2, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_shadow_color( lv.color_hex(0x050A0F), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Bg.set_style_shadow_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_shadow_width( 80, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_shadow_spread( 0, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_shadow_ofs_x( 0, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Bg.set_style_shadow_ofs_y( 30, lv.PART.MAIN| lv.STATE.DEFAULT);

        ui_Temp_Num_Bg = lv.obj(ui_Temp_Bg);
        ui_Temp_Num_Bg.set_width(  200);
        ui_Temp_Num_Bg.set_height(  200);
        ui_Temp_Num_Bg.set_align(  lv.ALIGN.CENTER )
        SetFlag(ui_Temp_Num_Bg, lv.obj.FLAG.SCROLLABLE, False)

        ui_Temp_Num_Bg.set_style_radius( 200, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Num_Bg.set_style_bg_color( lv.color_hex(0x0C191E), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Num_Bg.set_style_bg_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Num_Bg.set_style_bg_grad_color( lv.color_hex(0x191C26), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Num_Bg.set_style_bg_grad_dir( lv.GRAD_DIR.VER, lv.PART.MAIN| lv.STATE.DEFAULT);
        ui_Temp_Num_Bg.set_style_border_color( lv.color_hex(0x5A646E), lv.PART.MAIN | lv.STATE.DEFAULT );
        ui_Temp_Num_Bg.set_style_border_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT);

        ui_Label_Celsius = lv.label(ui_Temp_Num_Bg)
        ui_Label_Celsius.set_width(  lv.SIZE_CONTENT)
        ui_Label_Celsius.set_height(  lv.SIZE_CONTENT)
        ui_Label_Celsius.set_x( 10 )
        ui_Label_Celsius.set_y( 0 )
        ui_Label_Celsius.set_align(  lv.ALIGN.CENTER )
        ui_Label_Celsius.set_style_text_color( lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Label_Celsius.set_style_text_opa( 255, lv.PART.MAIN| lv.STATE.DEFAULT)
        ui_Label_Celsius.set_style_text_font(font_numberfont60, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Label_Celsius.set_text("23°")

        # Widget Change Grill Temp

        ui_Arc_Group_Click = lv.obj(self.page)
        ui_Arc_Group_Click.set_width(400)
        ui_Arc_Group_Click.set_height(400)
        ui_Arc_Group_Click.set_x(-1)
        ui_Arc_Group_Click.set_y(0)
        ui_Arc_Group_Click.set_align( lv.ALIGN.CENTER)
        SetFlag(ui_Arc_Group_Click, lv.obj.FLAG.SCROLLABLE, False)
        ui_Arc_Group_Click.set_style_bg_color( lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_Arc_Group_Click.set_style_bg_opa(0, lv.PART.MAIN| lv.STATE.DEFAULT )
        ui_Arc_Group_Click.set_style_border_width( 0, lv.PART.MAIN | lv.STATE.DEFAULT )

        ui_GrillSet = lv.obj(self.page)
        ui_GrillSet.set_width(500)
        ui_GrillSet.set_height(300)
        ui_GrillSet.set_x(0)
        ui_GrillSet.set_y(50)
        ui_GrillSet.set_align( lv.ALIGN.TOP_MID)
        SetFlag(ui_GrillSet, lv.obj.FLAG.HIDDEN, True)
        SetFlag(ui_GrillSet, lv.obj.FLAG.SCROLLABLE, False)
        ui_GrillSet.set_style_radius( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_bg_color( lv.color_hex(0x464B55), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        ui_GrillSet.set_style_border_color( lv.color_hex(0x2D323C), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_border_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_color( lv.color_hex(0x050A0F), lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_width( 80, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_spread( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_ofs_x( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
        ui_GrillSet.set_style_shadow_ofs_y( 30, lv.PART.MAIN | lv.STATE.DEFAULT )

        def Button2_eventhandler(event_struct):
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                popup_hidden_Animation(ui_GrillSet, 0)
            return

        def GrillSetPopup_eventhandler(event_struct):
            event = event_struct.code
            if event == lv.EVENT.CLICKED and True:
                popup_display_Animation(ui_GrillSet, 0)
                set_opacity( ui_GrillSet, 255)
                ModifyFlag( ui_GrillSet, lv.obj.FLAG.HIDDEN, "REMOVE")
                SetPanelProperty(ui_GrillSet, 'Position_Y', -500)
            return

        ui_Button2 = lv.btn(ui_GrillSet)
        ui_Button2.set_width(100)
        ui_Button2.set_height(50)
        ui_Button2.set_align( lv.ALIGN.CENTER)
        SetFlag(ui_Button2, lv.obj.FLAG.SCROLLABLE, False)
        SetFlag(ui_Button2, lv.obj.FLAG.SCROLL_ON_FOCUS, True)
        ui_Button2.add_event_cb(Button2_eventhandler, lv.EVENT.ALL, None)
        

        # Event
        ui_Arc_Group_Click.add_event_cb(GrillSetPopup_eventhandler, lv.EVENT.ALL, None)

        # End Widget Change Grill Temp




        ## End Grill temp widget


        # pellet_Panel = lv.obj(self.page)
        # pellet_Panel.set_size(150, 110)
        # pellet_Panel.set_align( lv.ALIGN.TOP_LEFT)

        # probe0_Panel = lv.obj(self.page)
        # probe0_Panel.set_size(150, 110)
        # probe0_Panel.set_align( lv.ALIGN.TOP_RIGHT)

        # probe1_Panel = lv.obj(self.page)
        # probe1_Panel.set_size(150, 110)
        # probe1_Panel.set_align( lv.ALIGN.RIGHT_MID)

        # probe2_Panel = lv.obj(self.page)
        # probe2_Panel.set_size(150, 110)
        # probe2_Panel.set_align( lv.ALIGN.BOTTOM_RIGHT)


class Page_History:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        print("Page_History")


class Page_Events:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        print("Page_Events")

class Page_Settings:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        print("Page_Settings")


class Screen_Main(lv.obj):
    def __init__(self, app, *args, **kwds):
        self.app = app
        super().__init__(*args, **kwds)


        dispp = lv.disp_get_default()
        theme = lv.theme_default_init(dispp, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.RED), True, lv.font_default())
        dispp.set_theme(theme)

        tvMenu = lv.tabview(self, lv.DIR.TOP, 50)
        tvMenu.set_align(lv.ALIGN.TOP_MID)

        tab_btns = tvMenu.get_tab_btns()
        tab_btns.set_style_pad_left(300, 0)

        tab_btns.set_style_text_color(lv.palette_lighten(lv.PALETTE.RED, 5), 0)

        # Add page to tabview component
        self.page_receipe   = Page_Receipe(self.app, tvMenu.add_tab("Receipe"))
        self.page_pellet    = Page_Pellet(self.app, tvMenu.add_tab("Pellet"))
        self.page_dashboard = Page_Dashboard(self.app, tvMenu.add_tab("Dashboard"))
        self.page_history   = Page_History(self.app, tvMenu.add_tab("History"))
        self.page_events    = Page_Events(self.app, tvMenu.add_tab("Events"))
        self.page_settings  = Page_Settings(self.app, tvMenu.add_tab("Settings"))

        tvMenu.set_act(2, True)


        # Component Time
        lblTime = lv.label(self)
        lblTime.align(lv.ALIGN.TOP_LEFT, 10, 17)
        lblTime.set_text("")

        # Function update Time
        def displayTime(timer1):
            year, month, day, dhour, dmins, dsecs, dweekday, dyearday, isdst = time.localtime()
            timeValue = "{:02d}:{:02d}".format(dhour, dmins)
            lblTime.set_text(timeValue)

        lv.timer_create(displayTime, 1000, None)


class PifireScreen:
    def init_gui_SDL(self):

        import SDL

        WIDTH = 800
        HEIGHT = 480
        ZOOM = 1
        FULLSCREEN = False

        SDL.init(w=WIDTH, h=HEIGHT, zoom=ZOOM, fullscreen=FULLSCREEN, auto_refresh=False)
        self.event_loop = event_loop()

        # Register SDL display driver.

        disp_buf1 = lv.disp_draw_buf_t()
        buf1_1 = bytes(WIDTH * 10)
        disp_buf1.init(buf1_1, None, len(buf1_1)//4)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf1
        disp_drv.flush_cb = SDL.monitor_flush
        disp_drv.hor_res = WIDTH
        disp_drv.ver_res = HEIGHT
        disp_drv.register()

        # Register SDL mouse driver

        indev_drv = lv.indev_drv_t()
        indev_drv.init() 
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = SDL.mouse_read
        self.mouse = indev_drv.register()

        # Register keyboard driver

        keyboard_drv = lv.indev_drv_t()
        keyboard_drv.init()
        keyboard_drv.type = lv.INDEV_TYPE.KEYPAD
        keyboard_drv.read_cb = SDL.keyboard_read
        self.keyboard = keyboard_drv.register()
        self.keyboard.set_group(self.group)

    def init_gui(self):

        self.group = lv.group_create()
        self.group.set_default()

        # Identify platform and initialize it

        if not event_loop.is_running():

            try:
                self.init_gui_SDL()
            except ImportError:
                pass

        # Create the main screen and load it.
        self.screen_main = Screen_Main(self)
        lv.scr_load(self.screen_main)


app = PifireScreen()
app.init_gui()

if __name__ == '__main__':
    while True:
        pass
    