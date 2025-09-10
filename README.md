# 3D-Object-Detection-Audi-A2D2
Mini 3D perception demo using the Audi A2D2 dataset: visualizes LiDAR point clouds with manually placed 3D bounding boxes alongside corresponding camera images. Demonstrates basic 3D object detection concepts and point cloud processing.

# Features

- Visualize LiDAR point clouds using [Open3D](http://www.open3d.org/)
- Overlay example 3D bounding boxes (manually placed for demo purposes)
- Display corresponding camera images
- Lightweight subset of the Audi A2D2 dataset for quick demo

## code explanation

Loads a LiDAR point cloud from the Audi A2D2 dataset using NumPy and converts it into an Open3D point cloud object.

Visualizes the 3D points in space, with manually placed 3D bounding boxes to demonstrate object localization understanding.

## What the output shows

A dense, colored point cloud representing the 3D structure of the scene captured by the LiDAR sensor.

Red and green cubes (bounding boxes) illustrate how objects would be annotated for 3D detection, confirming understanding of spatial positioning and perception.

## Future work

Process the full Audi A2D2 dataset, fusing LiDAR, camera, and radar data.

Develop automated 3D object detection models to identify vehicles, pedestrians, and other objects in real-time for autonomous driving applications.
