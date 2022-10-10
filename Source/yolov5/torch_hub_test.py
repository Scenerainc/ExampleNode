import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 이미지
img = ['C:/Users/tkryu/Desktop/Work Space/test_image/dnr.jpg']

# 추론
results = model(img)

# 결과
# results.print()
results.show()
# results.save() # Save image to 'runs/detect\exp'

# results.xyxy[0]  # 예측 (tensor)
# results.pandas().xyxy[0]  # 예측 (pandas)