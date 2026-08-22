# 项目介绍

本项目整理了赛艇上部分课程的往年试题（`exam/`）与作业（`homework/`），使用 LaTeX 重新排版，并借助 AI 或参照已有解答编写参考答案，方便同学们考前复习与作业速通。此外，项目还收集了公开的优质学习资料与学长学姐的课程评测（`material/`），助力学习、标记"雷区"。

往年题与作业可直接前往 `example/` 文件夹查看编译好的 PDF。如需自行组合试卷（E，Exam）或作业（H，Homework），可运行 `compile.py`。

# 提交贡献

如发现已有题目或解答存在错误，欢迎在 Issues 中反馈，维护人员将尽快修正。

如您拥有较新版本的考题、作业、优质资料或课程评测，或是有任何希望补充的内容，欢迎通过 Pull Request 提交。您可以按照 `SKILL.md` 中的项目规范提交 LaTeX 源码（可同步上传 PDF、Word 等格式的原件用于复核）；您也可以仅上传资料，维护人员将尽快协助转换为 LaTeX 源码。

非常感谢您的贡献——功在当下，利在千秋。

**一些 tips：**

我们十分推荐使用 AI 协作进行 LaTeX 排版与答案编写。您可以先使用 [MinerU 网页版](https://mineru.net/OpenSourceTools/Extractor) 将 PDF 转换为 Markdown 源码，再让 agent 参照 `SKILL.md` 的要求编写答案与 LaTeX 源码。

如果您从未配置过 agent，不妨先从 DeepSeek + Claude Code 起步，B 站上有不少相关教程；若不熟悉 Git 命令，可以让 agent 帮您安装 `gh`（GitHub 命令行工具）并配置账户信息，此后完全可以由 agent 代为完成提交、分支等各类操作。

## 声明

本项目仅用于个人学习交流。内容难免有错误疏漏，敬请指正；版权归原作者所有，侵删。
