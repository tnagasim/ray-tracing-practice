# %%
import numpy as np
import meshio
import plotly.graph_objects as go

# %%
mesh_data = meshio.read('data/bun_zipper.obj')
vertices = mesh_data.points
triangles = mesh_data.cells['triangle']

# %%
def rot_x(t):
    return np.array([
        [1, 0, 0],
        [0, np.cos(t), -np.sin(t)],
        [0, np.sin(t), np.cos(t)]
        ])

# %%
def rot_z(t):
    return np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t), np.cos(t), 0],
        [0, 0, 1]
        ])


# %%
A = rot_x(np.pi/4)
B = rot_z(4*np.pi/9+np.pi/4)

new_vertices = np.dot(vertices[:, :3], np.dot(B, A).T)

# %%
x = new_vertices[:, 0]
y = new_vertices[:, 1]
z = new_vertices[:, 2]
I = triangles[:, 0]
J = triangles[:, 1]
K = triangles[:, 2]

tri_points = new_vertices[triangles-np.min(triangles)]

# %%
pl_mygrey = [0, 'rgb(153, 153, 153)'], [1., 'rgb(255, 255, 255)']

pl_mesh = go.Mesh3d(
    x=x, y=y, z=z, colorscale=pl_mygrey, intensity=z,
    flatshading=True, i=I, j=J, k=K, name='Bunny', showscale=False)

# %%
lightposition = dict(x=0, y=0, z=0)
lighting = dict(
    ambient=0.18, diffuse=1, fresnel=0.1, specular=1, roughness=0.05,
    facenormalsepsilon=1e-15, vertexnormalsepsilon=1e-15
)
pl_mesh.update(
    cmin=-0.5, lighting=lighting, lightposition=lightposition
)

# %%
Xe = []
Ye = []
Ze = []
for T in tri_points:
    Xe.extend([T[k%3][0] for k in range(4)]+[None])
    Ye.extend([T[k%3][1] for k in range(4)]+[None])
    Ze.extend([T[k%3][2] for k in range(4)]+[None])

lines = go.Scatter3d(
    x=Xe, y=Ye, z=Ze, mode='lines', name='',
    line=dict(color='rgb(70,70,70)', width=1)
)

# %%
layout = go.Layout(
    scene_xaxis_visible=False,
    scene_yaxis_visible=False,
    scene_zaxis_visible=False,
    paper_bgcolor='rgb(128,128,128)'
)

# %%
fig = go.Figure(data=[pl_mesh, lines], layout=layout)

# %%
import plotly
plotly.offline.init_notebook_mode()
plotly.offline.iplot(fig, show_link=False)

# %%
