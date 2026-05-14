from ultralytics import YOLO

model = YOLO('yolo26n.pt')

results = model("Cars.mp4", save=True, classes=[0] )
