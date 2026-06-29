# CourseMaterial

PKU 往年题、模拟题与作业的 LaTeX 整理。

如果你是第一次拿到这个项目，请参考这份手册：[docs/快速上手指南.md](docs/快速上手指南.md)。

## 目录结构

```
CourseMaterial/
├── compile.py           # 编译脚本（交互式选择题目 → 单个 PDF）
├── main.tex             # 编译入口，会被 compile.py 自动更新
├── preamble.tex         # 公共宏包与格式
├── exam/                # 试卷
├── homework/            # 作业
├── supplement/          # 补充资料
├── example/             # 编译好的现成内容（含批量更新脚本）
└── build/               # 编译输出的 pdf 存放地
```

## 编译方式

你可以直接进入 `example/` 查看其他用户已经编译好的 pdf。也可以：

```bash
python compile.py       
```

按菜单选择内容，可以进行定制化编译。如需批量更新 `example/` 下的全部 PDF：

```bash
python example/update-example.py
```

等价地，也可以在 `main.tex` 里面手动导入所需内容进行编译。

补充资料应直接进入 `supplement/<课程名>/` 查看。

## 提交规范

如果你想提交课程资料，请参考这份手册：[docs/协作者手册.md](docs/协作者手册.md)，非常非常欢迎感谢大家多多贡献！！

## 声明

题目版权归原作者所有，侵删。

本项目的往年题、作业题大多来自“赛艇先生”公众号或同学回忆，答案大多由 ai 生成。题目尽可能保留了来源的文件，答案尽可能进行了交叉检查，但难免有错误疏漏，请读者自行甄别。
