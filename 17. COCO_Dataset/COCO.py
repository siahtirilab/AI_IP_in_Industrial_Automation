from ultralytics import YOLO

model = YOLO('yolo26n.pt')

print(model.names)