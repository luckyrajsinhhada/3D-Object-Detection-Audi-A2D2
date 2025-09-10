import open3d as o3d
import numpy as np

lidar_file = "D:\\audi-a2d2-demo\data\lidar/20190401145936_lidar_frontcenter_000000080.npz"

data = np.load(lidar_file)
pointcloud = data['pcloud_points']  # this is the correct key

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pointcloud[:, :3])  # take x,y,z

o3d.visualization.draw_geometries([pcd])

