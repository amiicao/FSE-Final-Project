# FSE
## PyCharm 无法识别工程？

PyCharm可能无法正确识别工程。这种情况下：

1. 删掉 `finalproject/.idea ` 文件夹
2. 使用 PyCharm 打开 `finalproject` 文件夹，现在 PyCharm 已经可以正确识别出 project
3. PyCharm 中，File -> Settings(Preferences) -> Project: finalproject -> Python Interpreter
4. 应该已经可以在下拉列表中选择之前配置好的 Pipenv 虚拟环境。否则齿轮图标 -> Add
5. 选 Pipenv Environment。如果没装 Pipenv，先 `pip install pipenv`
6. 右键 `main.py` -> Run

