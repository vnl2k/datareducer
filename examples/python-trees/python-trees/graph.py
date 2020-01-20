import csv
import os
from typing import Dict, List, Any
from graphviz import Digraph

def graph_with_images(image_path: str):
  """
  Plots graph with custom node shapes supplied as images.
  """

  def createNode(graph, image_path, ID):
    graph.node(ID, image=f'{image_path}')

  def makeTable(title, image_path):
    return f"""<TABLE BORDER="2" CELLPADDING="0" CELLSPACING="0">
      <TR>
          <TD CELLPADDING="10" CELLSPACING="0" ALIGN="TEXT"><FONT face="Helvetica" point-size="30">{title}<BR ALIGN="LEFT"/></FONT></TD>
      </TR>
      <TR>
        <TD><IMG SRC="{image_path}"/></TD>
      </TR>
    </TABLE>"""

  def createFancyNode(graph, title, image_path, ID):
    graph.node(ID, label=f'<{makeTable(title, image_path)}>')

  graph = Digraph("graph_with_images", format='svg', node_attr={
    'label': "", 'width': "8", 'height': "8", 
    'fixedsize': "true", 'imagescale': "true", 'penwidth': "0"
    })
  graph.graph_attr['rankdir'] = 'LR'

  createNode(graph, image_path, "A")
  createNode(graph, image_path, "B")
  createNode(graph, image_path, "C")
  createNode(graph, image_path, "D")
  createNode(graph, image_path, "E")
  createFancyNode(graph, 'Dummy Tittle', image_path, "F")

  graph.edges(['AB', 'BC', 'AD', 'DE', 'CF', 'EF'])

  graph.render('grah.gv', view=True)

graph_with_images('C0178269_C3516203.svg')
# graph_with_images('C0178269_C3516203.jpg')
