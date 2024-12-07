# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_better_broadcast']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0,<3.0.0',
 'nonebot-plugin-waiter==0.8.0',
 'nonebot2>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-better-broadcast',
    'version': '1.0.4',
    'description': 'nonebot2 plugin, boardcast your message to every groups',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <img src="https://github.com/WStudioGroup/hifumi-plugins/blob/main/remove.photos-removed-background.png" width="200">\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-better-broadcast\n\n_✨ 将你的信息广播到所有群聊，支持多种类型 ✨_\n\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/captain-wangrun-cn/nonebot-plugin-better-broadcast.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-better-broadcast">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-better-broadcast.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n\n</div>\n\n## 📖 介绍\n\n将你的信息广播到所有群聊，支持多种类型\n\n> [!IMPORTANT]\n> 如果需要广播聊天记录，请使用Napcat，因为使用了forward_group_single_msg接口（本人小白awa）\n\n## 💿 安装\n\n<details open>\n<summary>使用 nb-cli 安装</summary>\n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装\n\n    nb plugin install nonebot-plugin-better-broadcast\n\n</details>\n\n<details>\n<summary>使用包管理器安装</summary>\n在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令\n\n<details>\n<summary>pip</summary>\n\n    pip install nonebot-plugin-better-broadcast\n</details>\n\n\n打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入\n\n    plugins = ["nonebot_plugin_better_broadcast"]\n\n</details>\n\n## ⚙️ 配置\n\n在 nonebot2 项目的`.env`文件中添加下表中的必填配置\n\n| 配置项          | 类型   | 必填 | 默认值 | 说明                  |\n|:------------:|:----:|:---:|:---:|:-------------------:|\n| bc_blacklist | list | 否  | [ ]  | 群聊黑名单，广播时将不会发送到这些群聊 |\n\n## 🎉 使用\n### 指令表\n| 指令 | 权限 | 需要@ | 范围 | 说明 |\n|:-----:|:----:|:----:|:----:|:----:|\n| 发送广播 | 主人 | 否 | 私聊、群聊 | 顾名思义 |\n| 撤回广播 | 主人 | 否 | 私聊、群聊 | 撤回上一条广播的消息 |\n### 效果图\n<img src="imgs/QQ20241109-123325.png">\n<img src="imgs/QQ20241109-123336.png">\n\n## 📃 更新日志\n### 1.0.4（2024.11.15）\n- 🧋添加了“撤回广播”指令和取消广播，更改了插件信息\n',
    'author': 'WR',
    'author_email': 'wangrun114514@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/captain-wangrun-cn/nonebot-plugin-better-broadcast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
