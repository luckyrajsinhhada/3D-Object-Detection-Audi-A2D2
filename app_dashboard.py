import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import cv2
import os
import base64
import json



lidar_folder = r"H:\audi-a2d2-demo\data\lidar"
image_folder = r"H:\audi-a2d2-demo\data\camera"


lidar_files = sorted([f for f in os.listdir(lidar_folder) if f.endswith('.npz')])
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg'))])

num_frames = min(len(lidar_files), len(image_files))
if num_frames == 0:
    raise ValueError("No LiDAR or camera files found!")


def create_box_corners(box):
    x, y, z, dx, dy, dz, yaw = box
    x_c = [dx/2, dx/2, -dx/2, -dx/2, dx/2, dx/2, -dx/2, -dx/2]
    y_c = [dy/2, -dy/2, -dy/2, dy/2, dy/2, -dy/2, -dy/2, dy/2]
    z_c = [dz/2, dz/2, dz/2, dz/2, -dz/2, -dz/2, -dz/2, -dz/2]
    R = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0, 0, 1]
    ])
    corners = np.dot(R, np.vstack([x_c, y_c, z_c]))
    corners[0, :] += x
    corners[1, :] += y
    corners[2, :] += z
    return corners.T
app = dash.Dash(__name__)
app.title = "Audi A2D2 LiDAR + Camera Dashboard"

app.layout = html.Div([
    html.H1("Audi A2D2 Dashboard", style={'text-align': 'center'}),
    
    html.Label("Select Frame:"),
    dcc.Slider(
        id='frame-slider',
        min=0,
        max=num_frames-1,
        step=1,
        value=0,
        marks={i: str(i) for i in range(0, num_frames, max(1, num_frames//10))},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    
    html.Div([
        dcc.Graph(id='lidar-graph', style={'width': '60vw', 'height': '70vh', 'display': 'inline-block'}),
        html.Img(id='camera-image', style={'width': '35vw', 'height': '70vh', 'display': 'inline-block', 'margin-left': '20px'})
    ])
])


@app.callback(
    [Output('lidar-graph', 'figure'),
     Output('camera-image', 'src')],
    [Input('frame-slider', 'value')]
)
def update_frame(frame_idx):
    
    lidar_path = os.path.join(lidar_folder, lidar_files[frame_idx])
    lidar_data = np.load(lidar_path)
    
 
    if 'pcloud_points' in lidar_data.files:
        lidar_points = lidar_data['pcloud_points'][:, :3]
    else:
        raise KeyError(f"LiDAR .npz file {lidar_files[frame_idx]} missing 'pcloud_points' key")

    fig = go.Figure(data=[go.Scatter3d(
        x=lidar_points[:,0],
        y=lidar_points[:,1],
        z=lidar_points[:,2],
        mode='markers',
        marker=dict(size=2, color=lidar_points[:,2], colorscale='Viridis')
    )])
    fig.update_layout(scene=dict(aspectmode='data'))

  
    json_file = os.path.splitext(image_files[frame_idx])[0] + ".json"
    json_path = os.path.join(image_folder, json_file)
    if os.path.exists(json_path):
        try:
            with open(json_path) as f:
                data = json.load(f)
            boxes = np.array([[b['x'], b['y'], b['z'], b['dx'], b['dy'], b['dz'], b['yaw']] 
                              for b in data.get('boxes', [])])
            for box in boxes:
                corners = create_box_corners(box)
                edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
                for e in edges:
                    fig.add_trace(go.Scatter3d(
                        x=corners[e,0],
                        y=corners[e,1],
                        z=corners[e,2],
                        mode='lines',
                        line=dict(color='red', width=3)
                    ))
        except Exception as ex:
            print(f"Warning: could not read JSON for frame {frame_idx}: {ex}")


    img_path = os.path.join(image_folder, image_files[frame_idx])
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode('.png', img)
    img_b64 = base64.b64encode(buffer).decode()

    return fig, f"data:image/png;base64,{img_b64}"

if __name__ == '__main__':
    app.run(debug=True)
