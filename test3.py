from playwright.sync_api import Playwright, sync_playwright
import cv2 as cv
import random


def targetx():
    img_datu = cv.imread('max_cut.png', 0)  # 裁剪后的大图
    edges_datu = cv.Canny(img_datu, 100, 200)

    img_xiaotu = cv.imread('xiaotu.png', 0)  # 小图
    edges_xiaotu = cv.Canny(img_xiaotu, 100, 200)

    method = cv.TM_CCOEFF
    res = cv.matchTemplate(edges_datu, edges_xiaotu, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = min_loc
    x_target = top_left[0]
    print('x_target=' + str(x_target))
    return x_target


# 鼠标过轨迹，否则会被小怪兽吃了！
def get_track(distance):  # distance为传入的总距离
    track = []
    current = 0
    mid = distance * 3 / 5
    t = 0.2
    v = 1
    while current < distance:
        if current < mid:
            a = 4
        else:
            a = -2
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    url = 'https://www.geetest.com/demo/slide-popup.html'
    page.goto(url)
    page.wait_for_timeout(2000)
    page.locator("text=点击按钮进行验证").click()
    page.wait_for_timeout(2000)
    page.locator(".geetest_slider_button").click()
    page.wait_for_timeout(2000)
    page.locator('//canvas[2]').screenshot(path="max.png")  # 截图验证码
    page.wait_for_timeout(2000)
    img = cv.imread("max.png", flags=1)  # flags=1 读取彩色图像(BGR)
    element = page.query_selector('//body[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[2]')  # xpath 滑块小元素
    box = element.bounding_box()
    xmin, ymin, w, h = int(box["width"]), 0, 261, 161  # 矩形裁剪区域 (ymin:ymin+h, xmin:xmin+w) 的位置参数
    imgCrop = img[ymin:ymin + h, xmin:xmin + w].copy()  # 切片获得裁剪后保留的图像区域
    cv.imwrite('max_cut.png', imgCrop)  # 保存裁剪的图像
    page.wait_for_timeout(2000)
    x = int(box["x"] + box["width"] / 2)
    y = int(box["y"] + box["height"] / 2)
    page.mouse.move(x + random.randint(-5, 5), y + random.randint(-5, 5))  # 小滑动拖动的滑块中心位置
    page.wait_for_timeout(500)
    page.mouse.down()
    page.wait_for_timeout(500)
    x_target = targetx() + int(box["width"])
    track_list = get_track(x_target)
    i = 0
    for track in track_list:
        page.mouse.move(x + track, y + random.randint(-2, 2), steps=2)
        x = x + track
        if i < 0.8 * track_list.__len__():
            page.wait_for_timeout(random.randint(50, 80))
        else:
            page.wait_for_timeout(random.randint(150, 200))
        i = i + 1
    page.wait_for_timeout(500)
    page.mouse.up()
    page.wait_for_timeout(1000)
    # print(page.content())
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
