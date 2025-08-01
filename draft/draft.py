import base64
import io
import re
import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from skimage.filters import threshold_local
from scipy.ndimage import interpolation as inter

# Base64解码
base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAAAiCAIAAABHmckwAAAEH0lEQVR4XsXZS0hWURAH8AoprKggaJFBi1YVtXBVIgRRmRCEpfRY1KqwFi2kReUiiYLapWWQPaAoKHoIBekiciMUBVEY0UISoXBjD4LIhTbNd8c7zp0559zHx0d/Bjn3nHPBn3Pu9TUL0tLXfwBLz+bJn4NL9NT/yyw9EWXlyA4sOSPZ706ewpKrgdR++4hVOXNPx0t5eb7ntby0cYPf1A9CzGZ80+LBMtlYesGkfna7nkpLLrMbDLGZI/G52OcGu7kgg7wAGILm4eajYsUPBmPGDtNAymnGsqWTSx5slndM3OaiJWm2qyq7Hg7TQJpVk6W5BF5/5YEqXvaZOb5uWy112D7MlsRgu+SMzzz0aAcWXbLZ3WGJRzN/CSzYhthWmxds531hMBgzfiQ2ggnvBqugmVqdBayiwGDMFmbBZ3qPy1s4oxuaaKDMzFYPM5ozgSloRvDCRVWy9CYTC4ak2YKdk04zgyFpBtFqZc4BVtSM7AJgO0PxmRe0rQIDhtisXmBZwRaZ0ewEgzArnk9LQbNiMxiymVPAmybraSBt/Op2mrcd66EBxQfm5AJTfGYLBmPOBFaqqv3bnWa+S5pzgVXprSJorulqxoK0JkPSnABXr94oL8EDhsjMeyoHJvPErX59DwBpuci8c+17vU+kgmAQ5gC469IAZAbXvhnjG5WWwbiUai4IBmG2S1AeeLR5XcBstTXRwcZkMetnWJlTwc4lCpkDYIjMtqUYaYYMYHqN8ZMcMBcHQ2T2LUEhsFyS8/wYy5aqDiuzL5nA4DE7J2XQXBj89vMWZVZCeflu4AbdVRGws+RdEuksudkHVkuSp842bUYzswPRYEiaGQxBM++hWGExMK+q3iJ479NPCkxJZU+D9+35zVP2XS2jqPL7E8cKywErLeZi51Y0O8E3D/djyRmVmQ6zOQy2cZpl1A+bKmEwiKOLG/5euE+Trx5POcGUADtxpMmswLuff5WXNk7wh+srsGgcBkP8DdkZ2V5f4fHWt0Uh9ljTCy6wz7DPnMp2RrIDKRNMpe+MI7uNZg2GyOw81cXMkJnNGfn1hUpOWqGqBS3X5H4VZjvAEHVYvsY43OrvjYnPJktysZcvnQMeOcWCcTJsprjBFKcZYjaaK8cmcCDSiS8wnk81u8HzO6f/UOozQ3zCK8TOBYY85hL4atsP/Dh+dq4sNDM7NcXYgfjAp8+Pt949B0EwGPO9ltKfmZe1NgJ3mMwyko2Dn3V9akPhNHRu1lNx7rVepoEPTFGPLsWaJZvNM0cazZZNQXOZ4PbeIXmZag6DqckQybHnVMkt02EzgYE7XDP1jAYBc/YT7gyZ2+/cxYI0cxgMsbmqLv0f18qsweA3Y5PLZHOfia3MT45Ur2ko/U7LB9tmcuQEj8k8r/vQzHIwBP4HKyZchjsrUlIAAAAASUVORK5CYII="
image_data = re.sub(r'^data:image/.+;base64,', '', base64_data)
image_bytes = base64.b64decode(image_data)

# 创建PIL图像
image = Image.open(io.BytesIO(image_bytes))


# 高级预处理函数
def advanced_preprocess(img):
    # 转换为OpenCV格式
    img = np.array(img)

    # 1. 灰度转换
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # 2. 自适应阈值二值化 - 更好处理光照不均
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    # 3. 降噪处理
    denoised = cv2.medianBlur(binary, 3)

    # 4. 形态学操作 - 膨胀连接断裂字符
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(denoised, kernel, iterations=1)

    # 5. 边缘检测辅助字符分割
    edges = cv2.Canny(dilated, 50, 150)

    # 6. 轮廓检测并过滤小噪点
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(dilated)
    for cnt in contours:
        if cv2.contourArea(cnt) > 10:  # 过滤小噪点
            cv2.drawContours(mask, [cnt], -1, 255, -1)

    # 7. 应用掩码
    result = cv2.bitwise_and(dilated, dilated, mask=mask)

    # 8. 锐化处理
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(result, -1, kernel)

    # 9. 尺寸放大（提高分辨率）
    scaled = cv2.resize(sharpened, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    return Image.fromarray(scaled)


# 图像预处理
processed_image = advanced_preprocess(image)

# 优化OCR配置
custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# 尝试不同PSM模式提高识别率
psm_modes = [7, 8, 10, 13]
results = []

for psm in psm_modes:
    config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed_image, config=config)
    clean_text = re.sub(r'[^A-Z0-9]', '', text)
    if clean_text:
        results.append(clean_text)

# 选择最可能的结果（长度4-6个字符）
best_result = ""
for res in results:
    if 4 <= len(res) <= 6:
        best_result = res
        break

if not best_result and results:
    best_result = results[0]  # 如果没有合适长度，取第一个结果

print(f"识别结果: {best_result}")

# 保存预处理后的图像用于调试
processed_image.save("processed_verification.png")
print("预处理后的图像已保存为 'processed_verification.png'，请检查该图像以调整参数")