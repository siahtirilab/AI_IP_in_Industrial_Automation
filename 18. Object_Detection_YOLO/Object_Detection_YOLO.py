from ultralytics import YOLO

model = YOLO('yolo26n.pt')

results = model("mall.jpg")

results[0].show()