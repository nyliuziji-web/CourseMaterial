# CourseMaterial

PKUPHY 往年题、模拟题与作业的 LaTeX 整理。

## 结构

```
CourseMaterial/
├── compile.ps1          # 编译脚本（Windows PowerShell）
├── compile.sh           # 编译脚本（macOS / Linux）
├── main.tex             # 编译入口，会被 compile.ps1 / compile.sh 自动更新
├── preamble.tex         # 公共宏包与格式
├── exam/                # 试卷（每门课一个子目录）
├── homework/            # 作业（每门课一个子目录）
├── example/             # 编译好的现成内容
└── build/               # 编译输出 PDF
```

## 编译

- **Windows**：运行 `compile.ps1`（PowerShell）
- **macOS / Linux**：运行 `./compile.sh`（需先 `chmod +x compile.sh`）

按菜单选择内容即可。等价地，也可以在 `main.tex` 里面手动导入所需内容进行编译。

## 规范

- 每个 `.tex` 文件以 `\heading{课程名-项目名}` 开头
- `\heading` 自动解析 `-` 前后的课程名和项目名，生成标题和目录项
- **试卷**：`exam/课程名/课程名-学期-类型.tex`
- **作业**：`homework/课程名/章节名.tex`
- **解答**：用 `solution` 环境，通过 `\ShowSolutionstrue/false` 控制显示
