#TODO .obj must have a object name in header

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile

from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout

class ModelRenderer(Widget):
    model = StringProperty('')
    slider = NumericProperty()
    rotate_model = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            size=self.size,
            with_depthbuffer=True,
            compute_normal_mat=True,
            clear_color=(.5, .5, .5,))
        self.canvas.shader.source = resource_find('simple_lines.glsl')
        
        super(ModelRenderer, self).__init__(**kwargs)
        
    def setup_canvas(self, *args):
        if not (self.scene):
            return
        
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        
#         self.rotate = False
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, delta):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
#         self.canvas['height_plan'] = self.slider.value
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (1., 1., 1.)
#         self.slider.range = self.yrange
        if self.rotate_model:
            self.rot.angle += delta * 100

    def on_model(self, instance, value):
        print("loading scene %s" % value)
        self.canvas.clear()
        self.scene = ObjFile(resource_find(value))
        yrange = [i[1] for i in self.scene.vertices]
        self.yrange = (min(yrange), max(yrange))
        self.slider = self.yrange[0]
#         print "[{}:{}]".format(self.yrange[0], self.yrange[1])

        self.setup_canvas()

    def setup_scene(self):
        PushMatrix()
        Translate(0, 1.25, -3)
        Scale(0.0025)
        self.rot = Rotate(1, 0, 1, 0)
        m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
        PopMatrix()
   
    def reset_rotation(self):
        self.rot.angle = 0
   
    def _rotate_obj(self, dt):
        self.rot.angle += 2
    
    def on_touch_move(self, touch):
        if super(ModelRenderer, self).on_touch_down(touch):
            return True
        if not self.collide_point(touch.x, touch.y):
            return False
#         print "x({},{}) y({},{}) ".format(touch.pos[0], touch.ppos[0], touch.pos[1], touch.ppos[1])
        if touch.pos[0] > touch.ppos[0]:
            self.rot.angle += 4
        elif touch.pos[0] < touch.ppos[0]:
            self.rot.angle -= 4
        return True
    
    
#     def on_touch_up(self, touch):
#         print "touch: ({}, {})".format(touch.pos[0], touch.pos[1])
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self,  keyboard, keycode, text, modifiers):
#         print "plan: {}".format(self.plan)
        if keycode[1] == 'up':
            if self.slider.value < self.yrange[1]:
                self.slider.value += 10
        elif keycode[1] == 'down':
            if self.slider.value > self.yrange[0]:
                self.slider.value -= 10
        elif keycode[1] == 'right':
            self.rot.angle += 1/60. * 100
        elif keycode[1] == 'left':
            self.rot.angle -= 1/60. * 100

class MainScreen(FloatLayout):
    def on_state(self, togglebutton):
        if togglebutton.state == 'down':
            togglebutton.text = 'Parar'
            self.ids.renderer.rotate_model = True
        else:
            togglebutton.text = 'Girar'
            self.ids.renderer.rotate_model = False
#         print(togglebutton, togglebutton.state, togglebutton.text)

    def on_reset(self):
        self.ids.renderer.reset_rotation()

if __name__ == "__main__":
    class RendererApp(App):
        def build(self):
            return MainScreen()
    
    RendererApp().run()
