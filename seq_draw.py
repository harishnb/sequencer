# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:50:54 2018

@author: harisbha
"""

from seqdiag import parser, builder, drawer

diagram_definition = u"""
   seqdiag {
      browser  -> webserver [label = "GET /index.html"];
      browser <- webserver;
   }
"""
tree = parser.parse_string(diagram_definition)
diagram = builder.ScreenNodeBuilder.build(tree)
draw = drawer.DiagramDraw('PDF', diagram, filename="diagram.pdf")
draw.draw()
draw.save()