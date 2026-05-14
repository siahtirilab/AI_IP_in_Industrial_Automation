from ultralytics import YOLO

model = YOLO('yolo26x.pt')

results = model("Traffic.jpg", save=True, classes=[0] )

results[0].show()
print(model.names)