1. 克隆项目

首先，克隆这个项目到本地：

```
git clone https://github.com/yourusername/image-translation.git
cd image-translation
```
2. 安装依赖

在项目根目录下使用pip安装所需的Python库：

```
pip install -r requirements.txt
```

3. 获取百度**通用文字识别**API Key和Secret Key

访问 [百度AI平台](https://ai.baidu.com/) 注册并创建应用。

在项目根目录下创建.env文件。内容为

```
BAIDU_API_KEY=[你的API Key]
BAIDU_SECRET_KEY=[你的Secret Key]
```

程序效果如下：

![前](https://raw.githubusercontent.com/ChaoiteC/comic_translation/refs/heads/main/test1.jpg)

![后](https://raw.githubusercontent.com/ChaoiteC/comic_translation/refs/heads/main/test1_with_text.jpg)
