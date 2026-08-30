---
name: "course-material-tex"
description: "LaTeX 课程资料仓库项目规范：项目结构、排版环境、错误分类、OCR 清理、质量标准与多代理协作。"
metadata:
  short-description: "TeX 课程资料 - 项目规范与排版审核指南"
---

# 课程资料 TeX - 项目规范与排版审核指南

## 总则

本文件是课程资料 LaTeX 仓库的强制性规范。所有贡献者在提交前必须遵循。

---

## 快速参考

### 编译命令
```bash
python compile.py                     # 完整编译
python compile.py -s                  # 显示解答
python compile.py -c <idx>            # 编译单门课程
python example/update-example.py      # 重新生成示例 PDF
```

### 标准提交流程
```bash
git checkout master && git pull --rebase
git checkout -b feat/describe-change
git add <files> && git commit -m "<type>: <description>"
git fetch origin
git diff origin/master --name-status
git push origin feat/describe-change
gh pr create --base master --title "<type>: <description>"
```

| 类型 | 用途 | 示例 |
|------|------|------|
| feat | 新增内容 | feat: add QM 24Fall final |
| fix | 修复错误 | fix: correct Maxwell distribution exponent |
| docs | 文档更新 | docs: update SKILL.md |
| chore | 维护 | chore: update .gitignore |

---

## 一、项目结构

### 目录结构
```
exam/<课程名>/<教师>/       homework/<课程名>/<教师>/
figures/                    preamble.tex
compile.py                  example/update-example.py
```

### 文件命名
| 内容 | 格式 | 示例 |
|------|------|------|
| 试卷 | `<课程名>-<教师>-<年份学期>-<类型>.tex` | `电动力学-slj-25秋-期末.tex` |
| 作业 | `第<N>次作业.tex` 或 `第<N>章-<名称>.tex` | `第3次作业.tex` |
| 图片 | `<tex文件名>-fig<NN>.<扩展名>` | `hw03-fig01.png` |

- 年份两位数、学期 `春`/`秋`、类型 `期中`/`期末`/`模拟题N`/`免修考`/`样题`
- 教师名即子目录名（`common` 统考，`EX` 免修考）
- **`\heading{...}` 必须与文件名 stem 完全一致**；教师名含 `&` 时在 heading 中写 `\&`

---

## 二、排版规范与常见错误

以下环境/命令定义在 `preamble.tex` 中。**禁止**在单个 `.tex` 中重复定义。

### 文档结构
```latex
\heading{课程名-描述}

\begin{question}[可选标题]
  题面...
  \begin{enumerate}
    \item 子问 (a)    \item 子问 (b)
  \end{enumerate}
  \begin{solution}
    \begin{enumerate}
      \item (a) 的解答    \item (b) 的解答
    \end{enumerate}
  \end{solution}         % 必须在 \end{question} 之前
\end{question}
```

### 选择题 & 填空题
```latex
\begin{choiceoptions}[2]          % 禁止手写 A. B.
  \optionitem{选项一}  \optionitem{选项二}
\end{choiceoptions}
\blank[3cm]                       % 禁止 \rule 或 ______
```

### 数学常数（强制使用）
| 命令 | 错误写法 | 命令 | 错误写法 |
|------|----------|------|----------|
| `\ee^{x}` | `e^{x}` | `\ii` | `i`, `\mathrm{i}` |
| `\dd{x}` | `dx`, `\mathrm{d}x` | `\operatorname{E}[X]` | 裸 `E[X]` |

- **`e` 的边界**：指数函数 `e^{...}` → `\ee^{...}`；元电荷 `e^2`、`eB` 等不替换
- **`i` 的边界**：虚数单位 → `\ii`；下标（`_i`、`\psi_i`）不替换
- **`d` 的边界**：微分 → `\dd{x}`；变量（`d=2r`）不替换
- **`E[X]` 的边界**：统计期望 → `\operatorname{E}[X]`；物理能量不替换

### enumerate 嵌套
| 层级 | 标号 | 层级 | 标号 |
|------|------|------|------|
| 1 | (1)(2)(3) | 2 | (a)(b)(c) |
| 3 | (i)(ii)(iii) | | |

始终用嵌套 `enumerate`，禁止手写 `(a)(b)`。

### 图片 & 代码 & 答案
```latex
\pyfig[0.72\linewidth]{figures/filename.png}{图注}
\ansmath{E=mc^2}       \anstext{正确答案}

% 通用代码（需转义 _ & { }）   % 算法/伪代码（verbatim，无需转义）
\begin{ttbox} ... \end{ttbox}  \begin{codebox} ... \end{codebox}
% Python（verbatim + 行号）
\begin{pycode} ... \end{pycode}
```

### TikZ 图形（能画则优先于图片）
TikZ 图居中放置。仅 TikZ 无法高效复刻时（复杂几何、照片）才用 `\pyfig`。

```latex
% 二叉树
\begin{tikzpicture}[level distance=9mm,
  every node/.style={draw,circle,minimum size=6mm,inner sep=1pt},
  level 1/.style={sibling distance=26mm}]
\node {根} child {node {左子}} child {node {右子}};
\end{tikzpicture}

% 红黑树（同上，结点样式见下）
% blacknode/.style={draw,rectangle,fill=black,text=white,minimum size=6mm}
% rednode/.style={draw,circle,red,text=red,minimum size=6mm}

% 有向图
\begin{tikzpicture}[>=stealth]
  \node[draw,circle] (v1) at (0,0) {$V_1$};
  \node[draw,circle] (v2) at (2,0) {$V_2$};
  \draw[->,thick] (v1) -- (v2);
\end{tikzpicture}
```

### 错误分类

**A 类（严重）—— 必须修复**
| 代码 | 类型 | 描述 |
|------|------|------|
| A1 | 数学计算 | 数值/积分/导数/符号错误 |
| A2 | 物理推理 | 推理错误、量纲不匹配 |
| A3 | 建模错误 | 数学模型用错 |
| A4 | 条件缺失 | 题目条件不充分 |
| A5 | 答案不匹配 | 解答与题目不符 |
| A6 | OCR 严重 | 误读导致题意改变（`$2n$` → `$2^n$`） |

**B 类（排版）—— 应按优先级修复**
| 代码 | 问题 | 修复 |
|------|------|------|
| B1 | 裸数学常数 | `e^x`→`\ee^{x}`，`i`→`\ii`，`dx`→`\dd{x}` |
| B2 | 全角括号 `（）` | 改为 `()` |
| B3 | 手写列表 `(a)` | 用 `\begin{enumerate}` |
| B4 | 手写选项 `A. B.` | 用 `\begin{choiceoptions}` |
| B5 | 手绘填空线 `\rule` | 用 `\blank[宽度]` |
| B6 | 环境嵌套错误 | `\end{solution}` 须在 `\end{question}` 前 |
| B7 | `\heading` 缺失/多余 | 添加或修正 |
| B8 | 重复 `\newcommand` | 删除——`preamble.tex` 已定义 |
| B9 | 杂散 BEL 字节 0x07 | Python `\a` 转义残留，查找替换 |
| B10 | 宏中双反斜杠 | `\\\\qquad` → `\qquad` |
| B11 | `\dd{}` 空参数 | `\dd{\theta}` 非 `\dd{}\theta` |
| B12 | 裸 `E[X]` | → `\operatorname{E}[X]` |
| B13 | 解答不完整 | 补充推导步骤 |
| B14 | 重复行 | 删除 |
| B15 | 杂散字符 | 复制粘贴残留 |

**C 类（风格）**
- 复杂推导缺少解说 · 死代码残留 · 缩进不一致

### 审查要点（提交前逐项核对）
- [ ] `\heading{课程名-描述}` 为第一行，与文件名一致
- [ ] `question`/`solution`/`enumerate`/`choiceoptions` 结构正确，`\end{solution}` 在 `\end{question}` 前
- [ ] 无重复 `\newcommand`，无裸 `e`/`i`/`d`/`E[X]`，无全角 `（）`，无手写列表/选项/填空线
- [ ] 数学推导正确（无 A1），物理模型正确（无 A2/A3）
- [ ] 解答推导链完整（方法→代入→化简→结果），不以"解得"跳过步骤
- [ ] OCR 无乱码/断裂，数学符号正确
- [ ] `python compile.py` 0 错误；`git diff origin/master` 仅预期改动

---

## 三、OCR 清理指南

| 伪影 | 修复 | 伪影 | 修复 |
|------|------|------|------|
| `$2n$` 应为 `$2^n$` | 检查上下文 | r/t、0/O 混淆 | 校对 |
| `$...$` 跨行断开 | 合并 | `x_i` → `xi` | 重插 `_` `^` |
| `\frac{a}{b}` → `a/b` | 重建 | `\int_0^1` → `\int` | 恢复 |
| 乱码 / `\unichar` | UTF-8 编码 | 0x07 BEL 字节 | 删除 |

1. **结构**：恢复 `question`/`solution`/`enumerate` 环境
2. **数学**：重建 `\frac`、`\sum`、`\int`、`^`、`_`
3. **符号**：`e^x`→`\ee^{x}`，`i`→`\ii`，`dx`→`\dd{x}`，`E[X]`→`\operatorname{E}[X]`
4. **排版**：全角→半角，手写→环境，填空线→`\blank`
5. **验证**：编译、修复、对照原件

---

## 四、质量标准

### 各学科最低推导链
| 学科 | 必需步骤 |
|------|----------|
| 数学 | 方法/公式 → 代入 → 化简 → 关键技巧 → 结果 |
| 物理 | 模型 → 假设 → 坐标系 → 支配方程 → 求解 → 量纲检查 → 解释 |
| 统计 | 模型 → 分布 → 代入 → 估计 → 区间/检验结论 |
| 算法 | 思路 → 伪代码/递推 → 复杂度分析 → 正确性论证 |

### 需扩充的信号 & 规则
- "解得"后直接跳答案、复杂推导裸结果、缺受力分析图、使用"显然"/"易得" → 需补充中间步骤
- 只加必要步骤，不改原始结论；用普通段落（可加 `\textbf{解析：}`）；不超过原长 1.5 倍

---

## 五、普适性审查技巧（从实际修订中提炼）

> 以下技巧来自对 17 门课程、185 个 .tex 文件的逐题深入审查，按错误模式分类。审查者应逐条对照，避免同类错误遗漏。

### 5.1 量子力学常见错误

| 错误模式 | 典型表现 | 检查方法 |
|---------|---------|---------|
| **C-G 系数概率互换** | 角动量耦合中不同 $j$ 值的概率系统性互换 | 验证 $\sum_j P(j)=1$；塌缩态系数的模方等于对应概率 |
| **微扰矩阵元漏零** | 偶宇称态的一阶能量修正写了非零值，实际积分为零 | 检查被积函数的宇称性：奇函数; 偶态 $n=1$ 时 $\cos 2\phi$ 全空间积分为零 |
| **自旋投影概率算错** | $S_x$/$S_y$ 测量概率公式中系数计算错误 | 验证 $P(+)+P(-)=1$；用 $\braket{\psi}{S_\alpha}{\psi}$ 交叉检验 |
| **变分法 $E_1$ 符号混用** | 中间公式用 $E_1$（负值），数值代入用 $\|E_1\|$（正值），导致符号不一致 | 统一约定：全程用 $E_1<0$ 或全程用 $\|E_1\|>0$，中间公式与数值代入保持一致 |
| **波函数归一化系数** | 归一化常数漏因子或多因子 | 代入归一化积分 $\int\|\psi\|^2=1$ 验证 |

### 5.2 数学物理方法常见错误

| 错误模式 | 典型表现 | 检查方法 |
|---------|---------|---------|
| **v.p. 积分符号** | 围道积分留数定理应用时符号错误 | 追踪围道方向（逆时针正/顺时针负）；小圆弧绕极点半圈贡献 $\pm i\pi\operatorname{Res}$ |
| **自伴条件共轭遗漏** | $y(l)=\alpha y(0)$ 取复共轭时漏共轭 $\alpha$ | 复共轭作用于**所有**复数：$\bar{y}(l)=\bar{\alpha}\bar{y}(0)$，非 $\alpha\bar{y}(0)$ |
| **叠加解缺连接符** | 特解 + 齐次解两项间漏写 `+` 号 | 检查通解 $u=u_{\text{特}}+u_{\text{齐}}$ 的 `+` 号 |
| **cot/tan 方程虚部符号** | $\cot(\lambda l)=i\beta$ 的解 $\lambda$ 虚部符号错误 | 令 $z=\pi/2+w$，$\tan w=-i\beta$，$w=-i\operatorname{arctanh}\beta$，注意负号 |
| **$g_n(t)$ 多余因子** | 展开系数多出 $l$ 等长度因子 | 逐步验证 Fourier 系数 $\frac{2}{l}\int_0^l f(x)\sin\frac{n\pi x}{l}\dd{x}$ |

### 5.3 理论力学 / 电动力学常见错误

| 错误模式 | 典型表现 | 检查方法 |
|---------|---------|---------|
| **耦合振动质量比写反** | 高频模态比 $\psi/\phi$ 的分子分母互换 | 将模态比代回耦合方程组验证 |
| **角频率 vs 普通频率** | $\partial E/\partial J$ 等于 $1/T$（普通频率），误写为 $\omega$ | $\omega=2\pi\partial E/\partial J=2\pi/T$；区分 $\nu$ 与 $\omega$ |
| **守恒流 $J^\mu$ 因子** | Noether 流多 $c^2$ 因子或符号错 | 检查度规约定 $(+---)$ vs $(-+++)$；$J^\mu=\partial\mathcal{L}/\partial(\partial_\mu\phi)\delta\phi$ |
| **Faraday 旋转符号** | $k_+-k_-$ 的符号写反 | 圆偏振光色散关系 $n_\pm=\sqrt{1-\omega_p^2/(\omega(\omega\mp\omega_c))}$，展开时注意 $\mp$ |

### 5.4 固体物理常见错误

| 错误模式 | 典型表现 | 检查方法 |
|---------|---------|---------|
| **正格矢 / 倒格矢张冠李戴** | 晶面间距 $d=2\pi/\|\vb{G}\|$ 误用 $d=2\pi/\|\vb{R}\|$ | **量纲检查**：$d$ 应有长度量纲；$2\pi/\|\vb{R}\|$ 有波矢量纲 |
| **倒格矢公式** | BCC/FCC 倒格子类型互判错误 | BCC↔FCC 互为倒格子；倒格矢 $\vb{G}=\frac{2\pi}{a}(h\vb{b}_1+k\vb{b}_2+l\vb{b}_3)$ |

### 5.5 统计 / 数据结构常见错误

| 错误模式 | 典型表现 | 检查方法 |
|---------|---------|---------|
| **Bayes 后验算错** | 分子遗漏先验、分母遗漏归一化项 | 验证 $\sum P(H_i\|D)=1$ |
| **$\chi^2_{\min}$ 残合残差** | 残合值代入错误、残差平方和算错 | 逐步验证 $\chi^2=\sum(y_i-f(x_i;\hat\theta))^2/\sigma_i^2$ |
| **基尼系数中间步骤矛盾** | 最终结果正确但中间梯形面积求和错误 | 逐步验证每个梯形面积 $\frac{1}{2}(y_{i-1}+y_i)\Delta x$ |
| **广义表 Head/Tail 嵌套** | 运算公式嵌套层次错误，中途遇到空表 | 逐步执行 Head/Tail 操作，检查每步结果非空 |
| **压缩 Trie 叶结点错配** | 后缀 Trie 树中叶结点编号与边标签拼接不匹配 | 验证每条根→叶路径标签拼接等于对应后缀 |

### 5.6 通用审查技巧

| 技巧 | 说明 |
|------|------|
| **概率归一化检验** | 凡是概率/分布，立即检查 $\sum P_i=1$ 或 $\int p(x)\dd{x}=1$ |
| **量纲一致性检验** | 最终结果量纲必须与所求物理量一致；中间表达式量纲也须一致 |
| **特殊点代入检验** | Fourier 级数/展开式代入 $x=0,\pi$ 等特殊点，检查左右是否相等 |
| **宇称性检验** | 积分 $\int_{-a}^{a}f(x)\dd{x}$：$f$ 奇→积分零，$f$ 偶→$2\int_0^a$；微扰矩阵元常用 |
| **交叉项不假设为零** | $\langle(x_1-x_2)^2\rangle=\langle x_1^2\rangle+\langle x_2^2\rangle-2\langle x_1x_2\rangle$，**不可假设** $\langle x_1x_2\rangle=0$ |
| **中间步骤 vs 最终结果一致性** | 最终结果正确不代表中间步骤正确；逐步验证每个等号 |
| **符号约定一致性** | 同一推导中 $E_1<0$ vs $\|E_1\|$、度规 $(+---)$ vs $(-+++)$、$\ee^{+i\omega t}$ vs $\ee^{-i\omega t}$ 须全程统一 |
| **冗余解答文字** | 正文推导给出结论后，`\ansmath{}` 又框装同一结论 → 删除正文重复结论，保留 `\ansmath`；或保留正文推导，删除多余 `\ansmath` |
| **宏合规不一致** | 同一文件中有时用 `\dd{x}` 有时用 `dx` → 全文搜索裸 `d`/`e`/`i`/`E[`，统一替换 |
| **LaTeX 语法 typo** | `]` 应为 `\]`（公式结束符）；中文 typo 如"无究小"→"无穷小" → 编译检查 + 通读 |

### 5.7 TikZ 图审查要点

| 要点 | 说明 |
|------|------|
| **节点遮挡** | 检查 `\node at (x,y)` 坐标是否过近；增大 `sibling distance`/`level distance` |
| **标签遮挡** | 边标签用 `node[fill=white,inner sep=1pt]` 加白色底纹避免被线穿过 |
| **图意一致性** | TikZ 图中标签（如 A/B/C）须与 solution 文字描述一致；标签用反记 A1 错误 |
| **Trie/树完整性** | 压缩 Trie 的叶结点数 = 后缀数；每条根→叶路径拼接 = 对应后缀 |
| **图 vs 推导** | 图中数值/结构须与推导过程中的数值/结构一致 |

---

## 六、多代理协作

- **并行**：为每个代理分配不相交的课程目录
- **输出**：审查文件、A 类错误（记入 error.md）、B 类修复、Git 提交信息、需人工审查项
- **冲突**：`git merge origin/master` → 保留本地版 `git checkout --ours path/to/file.tex`

---

## 附录：常见编译错误
| 错误 | 原因 | 修复 |
|------|------|------|
| `Undefined control sequence` | 命令拼写错误 | 检查 `\` 命令名 |
| `Missing \endgroup` / `Missing $ inserted` | 环境或数学模式未配对 | 检查 `\begin`/`\end`、`$`/`$$` |
| `Extra } or forgotten $` | 花括号不匹配 | 逐层检查 `{` `}` |
| `Misplaced alignment tab &` | 文本中未转义 `&` | 写 `\&`（如 `cjh\&lxj`） |
| `Command \ee already defined` | `.tex` 中重复 `\newcommand` | 删除该行 |
| Package 编码错误 | 不可见 Unicode 字符 | 清理 OCR 残留 |
