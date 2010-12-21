# PyVernier - Draw a vernier scale with python
#
# Copyright (c) 2010 Johan Van den Brande <johan@vandenbrande.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
PyVernier is Python program to generate a vernier scale as a PDF document.
A vernier scale allows a measurement to be read more precisely. The most common use
for a vernier scale is found on a caliper.
"""

import os
import tempfile
import cairo

class Vernier:
    one_point_in_mm = 0.352777778

    def __init__(self, config):
        self.filename = config['filename']
        self.vernier_size = config['vernier_size']
        self.vernier_resolution = config['vernier_resolution']
        self.vernier_size_points = self.points( config['vernier_size'] )
        self.main_scale_size = config['main_scale_size']
        self.main_scale_size_points = self.points( config['main_scale_size'] )
        self.major_tick_size = self.points( config['major_tick_size'] )
        self.minor_tick_size = self.points( config['minor_tick_size'] )
        self.vernier_major_tick_size = self.points( config['vernier_major_tick_size'] )
        self.vernier_minor_tick_size = self.points( config['vernier_minor_tick_size'] )
        self.line_width = self.points( config['line_width'] )
        self.text_margin = self.points( config['text_margin'] )
        self.text_size = self.points( config['text_size'] )
        self.gap = self.points( config['gap'] )
        self.fontname = config['font_name']
        self.color = eval( config.get( 'color', '(0, 0, 0)' ) )
        self.background_color = eval( config.get( 'background_color', '( 0.99, 1.0, 0.94 )' ) )
        self.say = False

    def _say(self, msg):
        if self.say: print msg

    def points(self, size):
        return size / self.one_point_in_mm

    def text_height(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        s = cairo.PDFSurface(path, 100, 100 )  
        c = cairo.Context( s )
        c.select_font_face(self.fontname, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(self.text_size)
        x_bearing, y_bearing, width, height = c.text_extents('0')[:4]
        os.remove(path)
        return height * 1.1

    def text_centered(self, c, x, y, string):
        x_bearing, y_bearing, width, height = c.text_extents(string)[:4]
        xc = x - width / 2
        yc = y + height + self.text_margin
        c.move_to(xc, yc)
        c.show_text( string )

    def draw(self):
        text_height = self.text_height()
        document_width = self.main_scale_size_points * 1.25
        document_height = self.major_tick_size + self.minor_tick_size + text_height * 4 + self.text_margin * 2 + self.gap

        (name,ext) = os.path.splitext(self.filename)
        if ext != '.pdf':
            raise NameError('I only support pdf for the moment')

        s = cairo.PDFSurface( self.filename, document_width, document_height )
        c = cairo.Context( s )
        
        c.rectangle(0, 0, document_width, document_height)
        c.set_source_rgb(*self.background_color);
        c.fill()

        c.set_source_rgb (*self.color) 
        
        c.select_font_face(self.fontname, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(self.text_size)

        offset_x = self.main_scale_size_points * 0.25 / 2
        offset_y = self.text_margin
        offset_y_tick = offset_y + text_height + self.text_margin
        for i in xrange( 0, int(1/self.vernier_resolution) + 1 ):
            x = ( self.vernier_size - self.vernier_resolution ) * i 
            n = 10 * i * self.vernier_resolution 
            if n == int(n):
                self.text_centered( c, offset_x + self.points(x), offset_y, "%d" % int(n) )
            if i % 5 == 0:
                self._say( "--- %0.2f" % self.points(x) )
                c.move_to( offset_x + self.points(x), offset_y_tick )
                c.line_to( offset_x + self.points(x), offset_y_tick + self.vernier_major_tick_size )
            else:
                self._say( "-   %0.2f" % self.points(x) )
                c.move_to( offset_x + self.points(x), offset_y_tick + self.vernier_major_tick_size )
                c.line_to( offset_x + self.points(x), offset_y_tick + self.vernier_major_tick_size - self.vernier_minor_tick_size)

        c.set_line_width (self.line_width)
        c.stroke ()

        offset_y += self.major_tick_size + text_height + self.text_margin + self.gap
        c.move_to( offset_x, offset_y )
        c.line_to( offset_x + self.main_scale_size_points, offset_y )
        for i in xrange(0, self.main_scale_size + 1):
            if i % 10 == 0: # Main tick each cm or each inch
                self._say( "--- %0.2f" % self.points(i) )
                c.move_to( offset_x + self.points(i), offset_y )
                c.line_to( offset_x + self.points(i), offset_y + self.major_tick_size )
                self.text_centered( c, offset_x + self.points(i), offset_y + self.major_tick_size, "%d" % i )
            else:
                self._say( "-" )
                c.move_to( offset_x + self.points(i), offset_y )
                c.line_to( offset_x + self.points(i), offset_y + self.minor_tick_size)

        c.set_line_width (self.line_width)
        c.stroke ()


        c.show_page()

def vernier(config):
    vernier = Vernier(config)
    vernier.draw()
