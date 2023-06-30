
import numpy as np
import maya.OpenMaya as OpenMaya
import matplotlib.cm as cm


def get_selection(name):
    """Return the selection list based on given name."""
    selection_list = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName(name, selection_list)
    selection = OpenMaya.MItSelectionList(selection_list, OpenMaya.MFn.kMesh)
    return selection


def get_mesh(name):
    """Return the mesh object based on given name."""
    selection = get_selection(name)
    dagPath = OpenMaya.MDagPath()
    selection.getDagPath(dagPath)
    mesh = OpenMaya.MFnMesh(dagPath)
    return mesh


def get_vertices(mesh, space=OpenMaya.MSpace.kObject):
    """Return the 3D vertex coordinates of the given mesh as an numpy array."""
    # Create an empty point array.
    point_array = OpenMaya.MPointArray()
    # Get the 3D vertex coordinates.
    mesh.getPoints(point_array, space)
    # Save the results to an numpy array.
    num_vertices = point_array.length()
    vertices = np.zeros((num_vertices, 3))
    for i in range(0, num_vertices):
        vertices[i,0] = point_array[i][0]
        vertices[i,1] = point_array[i][1]
        vertices[i,2] = point_array[i][2]
    return vertices


def set_vertices(mesh, vertices, space=OpenMaya.MSpace.kObject):
    """Set the 3D vertex coordinates of the given mesh based on the input numpy array."""
    assert(vertices.shape[1] == 3)
    # Create an empty point array.
    point_array = OpenMaya.MPointArray()
    point_array.setLength(vertices.shape[0])
    for i in range(0, point_array.length()):
        point_array.set(i,vertices[i,0],\
                          vertices[i,1],\
                          vertices[i,2])
    # Set the 3D vertex coordinates.
    mesh.setPoints(point_array, space)


def get_triangles(mesh):
    """Return the triangle table of the given mesh as an integer numpy array."""
    tri_counts   = OpenMaya.MIntArray()
    tri_vertices = OpenMaya.MIntArray()
    mesh.getTriangles(tri_counts, tri_vertices)
    num_triangles = 0
    for i in range(0, tri_counts.length()):
        num_triangles += tri_counts[i]
    triangles = np.zeros((num_triangles, 3), dtype=np.int32)
    for i in range(0, num_triangles):
        triangles[i,0] = tri_vertices[3*i+0]
        triangles[i,1] = tri_vertices[3*i+1]
        triangles[i,2] = tri_vertices[3*i+2]
    return triangles


def get_polygons(mesh):
    """Return the polygon table of the given mesh as a list of lists."""
    num_polygons = mesh.numPolygons()
    polygon_list = []
    for i in range(num_polygons):
        output = OpenMaya.MIntArray()
        mesh.getPolygonVertices(i, output)
        polygon_vertex_ids = []
        for j in range(output.length()):
            polygon_vertex_ids.append(output[j])
        polygon_list.append(polygon_vertex_ids)
    return polygon_list


def get_edges(mesh):
    """Return the edge table of the given mesh as an integer numpy array."""
    num_edges = mesh.numEdges()
    # Create an empty edge index array.
    edges = np.zeros((num_edges,2), dtype=np.int32)
    # use MScriptUtil to extract edge information.
    p_array = [0, 0]
    x = OpenMaya.MScriptUtil()
    x.createFromList(p_array, 2)
    edge_ptr = x.asInt2Ptr()
    for i in range(0, num_edges):
        mesh.getEdgeVertices(i, edge_ptr)
        edges[i,0] = x.getInt2ArrayItem(edge_ptr, 0, 0)
        edges[i,1] = x.getInt2ArrayItem(edge_ptr, 0, 1)
    return edges


def get_normals(mesh):
    """Return the 3D normal vectors of the given mesh as an numpy array."""
    num_vertices = mesh.numVertices()
    normals = np.zeros((num_vertices, 3))
    vector = OpenMaya.MVector()
    for i in range(0, num_vertices):
        mesh.getVertexNormal(i, vector)
        normals[i,0] = vector[0]
        normals[i,1] = vector[1]
        normals[i,2] = vector[2]
    return normals


def get_uv_indices(mesh):
    """Return the UV polygon table of the given mesh as a list of lists."""
    uv_counts = OpenMaya.MIntArray()
    uv_ids = OpenMaya.MIntArray()
    mesh.getAssignedUVs(uv_counts, uv_ids)
    num_faces = uvCounts.length()
    polygon_uv_list = []
    idx = 0
    for i in range(0, num_faces):
        polygon_uv_ids = []
        for j in range(idx, idx + uv_counts[i]):
            polygon_uv_ids.append(uv_ids[j])
        polygon_uv_list.append(polygon_uv_ids)
        idx = idx + uv_counts[i]
    return polygon_uv_list
    

def get_uvs(mesh):
    """Return the UV coordinates of the given mesh as an numpy array."""
    u_array = OpenMaya.MFloatArray()
    v_array = OpenMaya.MFloatArray()
    mesh.getUVs(u_array, v_array)
    assert(u_array.length() == v_array.length())
    num_uv = u_array.length()
    uv_array = np.zeros((num_uv, 2))
    for i in range(0, num_uv):
        uv_array[i,0] = u_array[i]
        uv_array[i,1] = v_array[i]
    return uv_array   
    

def set_uvs(mesh, uv_array):
    """Set the UV coordinates of the given mesh based on the input numpy array."""
    assert(uv_array.shape[1] == 2)
    num_uv = uv_array.shape[0]
    u_array = OpenMaya.MFloatArray(num_uv)
    v_array = OpenMaya.MFloatArray(num_uv)
    for i in range(0, num_uv):
        u_array[i] = uv_array[i,0]
        v_array[i] = uv_array[i,1]
    mesh.setUVs(u_array, v_array)    


def get_vertex_color(mesh):
    """Return the RGB vertex colors of the given mesh as an numpy array."""
    vc = OpenMaya.MColorArray()
    mesh.getVertexColors(vc)
    color = np.zeros((vc.length(), 3))
    for i in range(0, vc.length()):
        color[i,:] = np.array([vc[i][0], vc[i][1], vc[i][2]])
    return color


def set_vertex_color(mesh, colors):
    """Set the RGB vertex colors of the given mesh based on the input numpy array."""
    assert(colors.shape[1] == 3)
    num_vertices = colors.shape[0]
    vc = OpenMaya.MColorArray()
    vc.setLength(num_vertices)
    for i in range(0, num_vertices):
        vc.set(i, colors[i,0], colors[i,1], colors[i,2])
    vi = OpenMaya.MIntArray()
    vi.setLength(num_vertices)
    for i in range(0, num_vertices):
        vi.set(i, i)
    mesh.setVertexColors(vc, vi)


def set_vertex_color_from_scalar_array(mesh, cmap_name, scalar_array, min_a, max_a):
    """Set the vertex colors of the given mesh based on a scalar array. The function
       converts the scalar array into a color map first using matplotlib."""
    cmap = cm.get_cmap(cmap_name, 256)
    map_array = cmap(np.arange(256))[:,:-1]
    normalized_array = (scalar_array - min_a) / (max_a - min_a)
    normalized_array *= map_array.shape[0]
    normalized_array = normalized_array.tolist()
    mapped_color_array = np.zeros((scalar_array.shape[0], 3))
    for i in range(0, scalar_array.shape[0]):
        idx = int(normalized_array[i])
        if(idx < 0):
            idx = 0
        if(idx > map_array.shape[0]-1):
            idx = map_array.shape[0]-1
        mapped_color_array[i, :] = np.array([map_array[idx,0], map_array[idx,1], map_array[idx,2]])
    set_vertex_color(mesh, mapped_color_array)