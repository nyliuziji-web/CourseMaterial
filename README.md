# CourseMaterial

PKUPHY 往年题、模拟题与作业的 LaTeX 整理。

## 结构

```
CourseMaterial/
├── compile.ps1          # 编译脚本（PowerShell）
├── preamble.tex         # 公共宏包与格式
├── exam/                # 试卷（每门课一个子目录）
├── homework/            # 作业（每门课一个子目录）
└── build/               # 编译输出 PDF
```

## 编译

运行 `compile.bat`（Windows）或 `compile.ps1`（PowerShell），按菜单选择内容即可。

## 规范

- 每个 `.tex` 文件以 `\heading{课程名-项目名}` 开头，如 `\heading{实验物理中的统计方法-基本概念}`
- `\heading` 自动解析 `-` 前后的课程名和项目名，生成标题和目录项
- **试卷**：`exam/课程名/课程名-学期-类型.tex`
- **作业**：`homework/课程名/章节名.tex`
- **解答**：用 `solution` 环境，通过 `\ShowSolutionstrue/false` 控制显示
