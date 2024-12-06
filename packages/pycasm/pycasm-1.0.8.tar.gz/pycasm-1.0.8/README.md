# pycas

使用 python 完成 casmooc.cn 上的课程学习

<img src="./screenshot.png" style="width: 80%; margin: 0 10%;" />

## 安装

```
pip install pycasm
```

## 获取 access token

1. 打开 [https://www.casmooc.cn/#/personal/index](https://www.casmooc.cn/)， 完成登录
2. `F12` 打开浏览器控制台，按 `CTRL + R` 或 `F5` 刷新页面，复制请求头中的 `x-access-token` 值到剪贴板

<img src="./screenshot_1.png" style="width: 80%; margin: 0 10%;">

## 运行

```python
pycas -tk <paste access token>
```

设置课程列表 位置 & 大小, `-p 1`: 第一页, `-s 100`: 列表大小 100

```python
pycas -tk <paste access token> -p 1 -s 100
```

更多帮助

```python
pycas -h
```
