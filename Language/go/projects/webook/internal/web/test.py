from flask import Flask, redirect, request, jsonify, session
import requests
import time

app = Flask(__name__)
app.secret_key = "your_random_secret_key_789"  # 替换为随机复杂字符串

# 飞书开放平台配置（替换为你的实际信息）
FEISHU_CONFIG = {
    "APP_ID": "你的飞书应用APP_ID",
    "APP_SECRET": "你的飞书应用APP_SECRET",
    "REDIRECT_URI": "你的回调地址",  # 如：https://xxx.ngrok.io/feishu/callback
    "SCOPE": "user:info.basic"  # 基础用户信息权限，按需扩展
}

# 1. 生成飞书授权二维码链接
@app.route("/feishu/login")
def feishu_login():
    # 飞书授权页面URL（扫码登录核心入口）
    auth_url = (
        "https://open.feishu.cn/open-apis/authen/v1/index"
        f"?app_id={FEISHU_CONFIG['APP_ID']}"
        f"&redirect_uri={FEISHU_CONFIG['REDIRECT_URI']}"
        f"&scope={FEISHU_CONFIG['SCOPE']}"
        "&response_type=code"  # 固定值，授权码模式
        "&state=feishu_csrf_123"  # 防CSRF，自定义
    )
    return redirect(auth_url)

# 2. 飞书授权回调接口（需配置到飞书开放平台）
@app.route("/feishu/callback")
def feishu_callback():
    # 获取飞书返回的授权码code
    code = request.args.get("code")
    state = request.args.get("state")

    # 校验state，防止CSRF攻击
    if state != "feishu_csrf_123":
        return jsonify({"code": -1, "msg": "非法请求，state校验失败"})

    if not code:
        return jsonify({"code": -1, "msg": "用户取消授权"})

    # 3. 用code换取access_token和user_id
    token_url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
    token_params = {
        "app_id": FEISHU_CONFIG["APP_ID"],
        "app_secret": FEISHU_CONFIG["APP_SECRET"],
        "code": code,
        "grant_type": "authorization_code"  # 固定值
    }

    try:
        # 发送POST请求获取token（飞书接口要求POST）
        token_response = requests.post(token_url, json=token_params, timeout=10)
        token_result = token_response.json()

        # 飞书接口返回格式：{"code":0, "msg":"success", "data": {...}}
        if token_result["code"] != 0:
            return jsonify({"code": -1, "msg": f"获取token失败：{token_result['msg']}"})

        access_token = token_result["data"]["access_token"]  # 用户级access_token
        user_id = token_result["data"]["user_id"]  # 飞书用户唯一标识
        expires_in = token_result["data"]["expires_in"]  # token有效期（秒）

        # 4. 拉取用户详细信息
        user_info_url = f"https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
        # 请求头需携带access_token
        headers = {"Authorization": f"Bearer {access_token}"}

        user_response = requests.get(user_info_url, headers=headers, timeout=10)
        user_result = user_response.json()

        if user_result["code"] != 0:
            return jsonify({"code": -1, "msg": f"获取用户信息失败：{user_result['msg']}"})

        # 提取核心用户信息
        user_data = {
            "user_id": user_id,
            "name": user_result["data"]["name"],  # 姓名
            "avatar": user_result["data"]["avatar_url"],  # 头像
            "email": user_result["data"].get("email"),  # 邮箱（需权限）
            "mobile": user_result["data"].get("mobile")  # 手机号（需权限）
        }

        # 5. 业务侧登录逻辑：存入session，标记登录状态
        session["feishu_user"] = user_data
        session["login_time"] = time.time()

        # 跳转到登录后的页面
        return redirect("/feishu/profile")

    except requests.exceptions.RequestException as e:
        return jsonify({"code": -1, "msg": f"网络请求异常：{str(e)}"})

# 3. 登录后展示用户信息
@app.route("/feishu/profile")
def feishu_profile():
    user = session.get("feishu_user")
    if not user:
        return redirect("/feishu/login")

    return jsonify({
        "code": 0,
        "msg": "飞书登录成功",
        "data": user
    })

# 4. 退出登录
@app.route("/feishu/logout")
def feishu_logout():
    session.pop("feishu_user", None)
    return jsonify({"code": 0, "msg": "退出成功"})

if __name__ == "__main__":
    # 本地测试端口，需与内网穿透端口一致
    app.run(host="0.0.0.0", port=5000, debug=True)