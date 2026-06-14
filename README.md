# CourseMaterial

PKU 往年题、模拟题与作业的 LaTeX 整理。

如果你是第一次拿到这个项目，请参考这份手册：[docs/快速上手指南.md](docs/快速上手指南.md)。

## 目录结构

```
CourseMaterial/
├── compile.ps1          # 编译脚本（Windows PowerShell）
├── compile.sh           # 编译脚本（macOS / Linux）
├── main.tex             # 编译入口，会被 compile.ps1 / compile.sh 自动更新
├── preamble.tex         # 公共宏包与格式
├── exam/                # 试卷（每门课一个子目录）
├── homework/            # 作业（每门课一个子目录）
├── lecture/             # 课程讲义与学习资料
├── example/             # 编译好的现成内容
└── build/               # 编译输出 PDF
```

## 编译方式

- **Windows**：运行 `compile.ps1`（PowerShell）
- **macOS / Linux**：运行 `./compile.sh`（需先 `chmod +x compile.sh`）

按菜单选择内容即可。等价地，也可以在 `main.tex` 里面手动导入所需内容进行编译。

你可以直接进入 `example/` 查看其他用户已经编译好的 pdf。

## 提交规范

如果你想提交课程资料，请参考这份手册：[docs/协作者手册.md](docs/协作者手册.md)，非常非常欢迎感谢大家多多贡献！！

## 声明

题目版权归原作者所有，侵删。

本项目的往年题、作业题大多来自“赛艇先生”公众号或同学回忆，答案大多由 ai 生成。题目尽可能保留了来源的文件，答案尽可能进行了交叉检查，但难免有错误疏漏，请读者自行甄别。
