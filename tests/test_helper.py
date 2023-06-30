"""
First, open a new Maya scene, then create any polygon object and name it as "Mesh".
In addition, in order to demostrate the vertex color function, make sure you create
an empty color array first by selecting the mesh object first then running
"Mesh Display" -> "Apply Color"

Before running the script, make sure to include the repo path such that Maya can 
find this repo

import sys
sys.path.append('/path/to/the/repo')

(Make sure the /path/to/the/repo is replaced with the actual root directory on your device)

Then run this test_helper.py script in Maya's Script Editor 
exec(open("/path/to/the/repo/tests/test_helper.py").read())
"""

import maya_helper as helper

mesh = helper.get_mesh('Mesh')

vertices = helper.get_vertices(mesh)
print(vertices)

normals = helper.get_normals(mesh)
print(normals)

triangles = helper.get_triangles(mesh)
print(triangles)

uvs = helper.get_uvs(mesh)
print(uvs)

vertices[:, 0] += 2.0
helper.set_vertices(mesh, vertices)

helper.set_vertex_color_from_scalar_array(mesh, 'jet', normals[:, 2], -1.0, 1.0)