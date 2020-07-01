import moderngl
import numpy as np


class Surface:
    def __init__(self, vts, ids, ns, cs=(0, 0, 1)):
        self.vts, self.ids, self.ns, self.cs = vts, ids, ns, cs
        self.box = np.vstack((vts.min(axis=0), vts.max(axis=0)))
        self.mode, self.blend, self.visible = 'mesh', 1.0, True
        self.color = cs if isinstance(cs, tuple) else (0, 0, 0)
        self.width = 1

    def on_ctx(self, ctx, prog):
        self.ctx = ctx
        vts, ids, ns, cs = self.vts, self.ids, self.ns, self.cs;
        buf = self.buf = np.zeros((len(vts), 9), dtype=np.float32)
        buf[:, 0:3], buf[:, 3:6], buf[:, 6:9] = vts, ns, cs
        self.vbo = ctx.buffer(buf.tobytes())
        ibo = ctx.buffer(ids.tobytes())

        content = [(self.vbo, '3f 3f 3f', 'v_vert', 'v_norm', 'v_color')]
        self.vao = ctx.vertex_array(prog, content, ibo)
        self.prog = prog

    def set_style(self, mode=None, blend=None, color=None, visible=None):
        if not mode is None: self.mode = mode
        if not blend is None: self.blend = blend
        if not visible is None: self.visible = visible
        if not color is None:
            self.buf[:, 6:9] = color
            self.vbo.write(self.buf.tobytes())
            self.color = color if isinstance(color, tuple) else (0, 0, 0)

    def draw(self, mvp, light, bright, scatter):
        if not self.visible: return
        self.ctx.line_width = self.width
        mvp = np.dot(*mvp)
        self.prog['Mvp'].write(mvp.astype(np.float32).tobytes())
        self.prog['blend'].value = self.blend
        self.prog['scatter'].value = scatter
        self.prog['light'].value = tuple(light)
        self.prog['bright'].value = bright
        self.vao.render({'mesh': moderngl.TRIANGLES, 'grid': moderngl.LINES}[self.mode])


class Loader:
    def __init__(self):
        self.h, self.v, self.r = 1.5, 0, 300
        self.ratio, self.dial = 1.0, 1.0
        self.pers, self.center = True, (0, 0, 0)
        self.background = 0.4, 0.4, 0.4
        self.light = (1, 0, 0)
        self.bright, self.scatter = 0.66, 0.66
        self.objs = {}
        self.ctx = None

    def on_ctx(self):
        self.ctx = moderngl.create_context()
        self.prog_suf = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 Mvp;
                in vec3 v_vert;
                in vec3 v_norm;
                in vec3 v_color;
                out vec3 f_norm;
                out vec3 f_color;
                void main() {
                    gl_Position = Mvp * vec4(v_vert, 1);
                    f_norm = v_norm;
                    f_color = v_color;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform vec3 light;
                uniform float blend;
                uniform float scatter;
                uniform float bright;
                in vec3 f_norm;
                in vec3 f_color;
                out vec4 color;
                void main() {
                    float d = clamp(dot(light, f_norm)*bright+scatter, 0, 1);
           			color = vec4(f_color*d, blend);
                }
			'''
        )

        self.prog_txt = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 mv;
                uniform mat4 proj;
                uniform float h;
                in vec3 v_vert;
                in vec3 v_pos;
                void main() {
                    vec4 o = mv * vec4(v_pos, 1);
                    gl_Position = proj *(o + vec4(v_vert.x*h, v_vert.y*h, v_vert.z, 0));
                }
            ''',
            fragment_shader='''
                #version 330
                uniform vec3 f_color;
                out vec4 color;
                void main() {
           			color = vec4(f_color, 1);
                }
			''')

        for i in self.objs.values():
            if isinstance(i, Surface): i.on_ctx(self.ctx, self.prog_suf)

    def add_surf(self, name, vts, ids, ns=None, cs=(0, 0, 1), real=True):
        surf = Surface(vts, ids, ns, cs)
        if not real: surf.box = None
        if not self.ctx is None:
            surf.on_ctx(self.ctx, self.prog_suf)
        self.objs[name] = surf
        self.count_box()
        return surf


    def get_obj(self, key):
        if not key in self.objs: return None
        return self.objs[key]

    def draw(self):
        self.ctx.clear(*self.background)
        self.ctx.enable(moderngl.DEPTH_TEST)
        # self.ctx.enable(ModernGL.CULL_FACE)
        self.ctx.enable(moderngl.BLEND)
        for i in self.objs.values(): i.draw(self.mvp, self.light, self.bright, self.scatter)

    def count_box(self):
        minb = np.array([i.box[0] for i in self.objs.values() if not i.box is None]).min(axis=0)
        maxb = np.array([i.box[1] for i in self.objs.values() if not i.box is None]).max(axis=0)
        self.box = np.vstack((minb, maxb))
        # print(self.box)
        self.center = self.box.mean(axis=0)
        self.dial = np.linalg.norm(self.box[1] - self.box[0])
