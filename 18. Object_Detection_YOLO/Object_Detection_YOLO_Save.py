from ultralytics import YOLO

model = YOLO('yolo26x.pt')

results = model("car.png")

results[0].save(filename="Car_Detection_YOLO.jpg")