from ultralytics import YOLO

model =YOLO('yolo26n.pt')

results = model("People.mp4", save=True)