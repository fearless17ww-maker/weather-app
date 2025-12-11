import flet as ft
import requests

def main(page: ft.Page):
    # 1. 设置 App 的基本属性
    page.title = "我的天气 App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 700

    # 请替换为你自己的 API Key
    API_KEY = "6bd8e6d57f6e2c9506dcdca2b33b8616"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    # 2. 定义获取天气的函数
    def get_weather(e):
        city = city_input.value
        if not city:
            result_text.value = "请输入城市名称！"
            result_text.color = "red"
            page.update()
            return
        params = {
            "q": city,           # 这里输入 "北京" 也没问题
            "appid": API_KEY,    # 你的 API Key
            "units": "metric",   # 摄氏度
            "lang": "zh_cn"      # 确保返回的“天气描述”也是中文 (如：多云)
        }

        # 发送请求
  
        
        try:
            response = requests.get(BASE_URL, params=params) 
            data = response.json()
            print(f"DEBUG: 状态码={response.status_code}, 返回数据={response.json()}")
            data = response.json()
            if response.status_code == 200:
                # 解析数据
                temp = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                # 更新界面显示
                result_text.value = f"城市: {city}\n温度: {temp}°C\n天气: {weather_desc}\n湿度: {humidity}%"
                result_text.color = "blue"
                weather_icon.name = ft.Icons.CLOUD_DONE  # 简单的图标变化
            else:
                result_text.value = "没找到这个城市，请检查拼写。"
                result_text.color = "red"
                weather_icon.name = ft.Icons.ERROR
                
        except Exception as ex:
            result_text.value = "网络错误，请检查连接。"
            print(ex)

        page.update()

    # 3. 构建界面元素 (UI)
    
    # 输入框
    city_input = ft.TextField(
        label="输入城市 (例如: Beijing, Shanghai)", 
        width=280, 
        text_align=ft.TextAlign.CENTER
    )
    
    # 查询按钮
    search_btn = ft.ElevatedButton(
        text="查询天气", 
        on_click=get_weather,
        icon=ft.Icons.SEARCH
    )
    
    # 显示天气的图标
    weather_icon = ft.Icon(name=ft.Icons.SUNNY, size=50, color="orange")
    
    # 显示结果的文本
    result_text = ft.Text(value="等待查询...", size=20, text_align=ft.TextAlign.CENTER)

    # 4. 将元素添加到页面中
    page.add(
        ft.Column(
            [
                ft.Text("今日天气", size=30, weight="bold"),
                weather_icon,
                ft.Container(height=20), # 空白间隔
                city_input,
                search_btn,
                ft.Container(height=20), # 空白间隔
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# 运行 App (桌面模式预览)
ft.app(target=main)