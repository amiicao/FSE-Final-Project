# FSE
## PyCharm 无法识别工程？

PyCharm可能无法正确识别工程。这种情况下：

1. 删掉 `finalproject/.idea ` 文件夹
2. 使用 PyCharm 打开 `finalproject` 文件夹，现在 PyCharm 已经可以正确识别出 project
3. PyCharm 中，File -> Settings(Preferences) -> Project: finalproject -> Python Interpreter
4. 应该已经可以在下拉列表中选择之前配置好的 Pipenv 虚拟环境。否则齿轮图标 -> Add
5. 选 Pipenv Environment。如果没装 Pipenv，先 `pip install pipenv`
6. 右键 `main.py` -> Run



## 关于登录验证码——PIL库 （也许）无法从pycharm直接安装
- 请到网页：https://www.lfd.uci.edu/~gohlke/pythonlibs/ 上搜索 pillow 或 PIL
- 下载相对应python版本的PIL库，如 Pillow-8.2.0-cp37-cp37m-win_amd64.whl
- 再在项目本地进入虚拟环境 `venv\Scripts\activate` （windows 环境）
- 先输入 `pip install wheel`
- 再输入 `pip install $绝对目录$/$库名字$（如Pillow-8.2.0-cp37-cp37m-win_amd64.whl）`

