import mdl
import os
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """

basename = ''
num_frames = 0

def first_pass( commands ):
    bb = False
    fb = False
    animated = False
    global basename
    global num_frames
    for com in commands:
        x = com['op']
        if x == 'basename':
            basename = com['args'][0]
            bb = True
        elif x == 'frames':
            if not bb:
                basename = 'my_animation'
                num_frames = com['args'][0]
                fb = True
        elif x == 'vary':
            animated = True
            if not fb:
                raise Exception('Please insert a valid frame rate value')
    return animated
"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a separate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropriate value.
  ===================="""
def second_pass( commands ):
    frames = []
    for s in range(int(num_frames+1)):
        frames.append({})
    for com in commands:
        if com['op'] == 'vary':
            args = com['args']
            knob_frames = args[1]-args[0]+1
            step = (args[3]-args[2])/knob_frames
            for i in range(int(args[0]),int(args[1]+2)):
                frames[i][com['knob']] = args[2] + step*(i-args[0])
    return frames

def run(filename):
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    consts = ''
    coords = []
    coords1 = []
    frame = 0

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    
    animated = first_pass(commands)
    if animated:
        symbols = second_pass(commands)
    while frame < num_frames:
        for command in commands:
            
            c = command['op']
            args = command['args']
            if 'knob' in command:
                knob = command['knob']
                
            if c == 'box':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[-1], str):
                    coords = args[-1]
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'sphere':
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                    
            elif c == 'torus':
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'line':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[3], str):
                    coords = args[3]
                    args = args[:3] + args[4:]
                if isinstance(args[-1], str):
                    coords1 = args[-1]
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4],args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
            elif c == 'move':
                value = 1
                if animated and knob != None:
                    value = symbols[frame][knob]
                tmp = make_translate(args[0]*value, args[1]*value, args[2]*value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                value = 1
                if animated and knob != None:
                    value = symbols[frame][knob]
                tmp = make_scale(args[0]*value, args[1]*value, args[2]*value)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                value = 1
                if animated and knob != None:
                    value = symbols[frame][knob]
                theta = args[1] * value * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
            elif animated:
                if not os.path.exists('anim'):
                    os.mkdir('anim')
        save_extension(screen, 'anim/' + basename+'%03d'%frame+'.png')
        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20
        #print frame
        frame += 1
    make_animation(basename)                        
