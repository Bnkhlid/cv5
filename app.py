import cv2
import numpy as np
from PIL import Image
from util import get_limits

# تعريف الألوان الممكنة
colors = {
    "Yellow": [0, 255, 255],
    "Red": [0, 0, 255],
    "Green": [0, 255, 0],
    "Blue": [255, 0, 0]
}

# اختيار اللون من المستخدم
print("Available colors:")
for c in colors:
    print("-", c)
choice = input("Enter color name: ").capitalize()
color = colors.get(choice, [0, 255, 255])  # افتراضي Yellow إذا ادخل خطأ

# فتح الكاميرا
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not found! Check the camera index.")
    exit()

# دالة تنظيف الماسك (إزالة التشويش)
def clean_mask(mask):
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # تحويل الصورة إلى HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # حساب حدود اللون باستخدام util.get_limits
    lowerLimit, upperLimit = get_limits(color=color)

    # عمل الماسك وتنظيفه
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask = clean_mask(mask) 

    # تحديد المربع حول الجسم الملون
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, choice, (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    # عرض الفيديو
    cv2.imshow('frame', detected_frame)

    # للخروج اضغط q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
