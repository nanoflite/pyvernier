import sys
sys.path.insert( 0, ".." )

from pyvernier import vernier

config = {
            'filename': 'example_1.pdf',        # Name of the file
            'main_scale_size': 200,             # Size of the main scale in mm
            'vernier_size': 5,                  # Width between two ticks on the vernier scale
            'vernier_resolution': 0.1,          # Resolution for the vernier scale (0.1 or 0.05 are sane values) 
            'major_tick_size': 5,               # Major tick size for the main scale
            'minor_tick_size': 3,               # Minor tick size for the main scale
            'vernier_major_tick_size': 5,       # Major tick size for the vernier scale
            'vernier_minor_tick_size': 3,       # Minor tick size for the vernier scale
            'line_width': 0.1,                  # Width of all lines
            'text_margin': 0.5,                 # Margin around the text
            'text_size': 3,                     # Size of the text
            'gap': 2,                           # Gap between main and vernier scale
            'font_name': 'CMU Concrete',        # Name of the font - Those classic TeX fonts!
    }

vernier(config)
