# 欧加真 5.x 内核快速构建（5.10 / 5.15）

OPPO/一加/真我 老平台 GKI 内核自动化编译（照 cctv18 三仓的 fastbuild 模式）。

## 支持的内核版本

### 5.10.x（android12-5.10，KMI gen 9）

| x | 平台 | 覆盖机型 | 官方源码分支 |
|---|---|---|---|
| 5.10.66 | mt6895 / sm8450 | 一加10R、Ace Race、一加10Pro | oneplus/mt6895_s_12.1_* 、sm8450_s_12.1_10_pro |
| 5.10.110 | mt6895 / mt6983 | Ace Racing、Ace 2V | oneplus/mt6895_t_13.0.0 、mt6983_t_13.0 |
| 5.10.149 | mt6895 / mt6983 | Ace、Ace Racing、一加平板、Nord 3 | 13.1 分支 |
| 5.10.168 | mt6895 / mt6983 | 10R、Ace、Ace Race、Ace 2V | 14.0 分支 |
| 5.10.198 | mt6983 | Nord 3 5G | oneplus_mt6983_u_14.0.0_nord_3_5g |
| 5.10.209 | mt6895 / mt6983 / sm8450 / sm8475 | 10R、一加平板、一加10Pro、一加11R、Ace Pro | u_14.0.0 / v_15.0.0 分支 |
| 5.10.226 | mt6983 / sm8450 / sm8475 | Ace 2V、Nord 3、一加平板、一加10Pro、Ace 2、Ace Pro、一加11R | v_15.0.0 分支 |
| 5.10.236 | mt6895 / mt6983 / sm8450 / sm8475 | Ace、Ace Race、Ace 2V、Nord 3、一加平板、一加10Pro、Ace 2、一加11R、一加10T | b_16.0.0 / v_15.0.0 分支 |

### 5.15.x（android13-5.15，KMI gen 8）

| x | 平台 | 覆盖机型 |
|---|---|---|
| 5.15.74 | sm8550 | 一加11（ColorOS 13.1） |
| 5.15.123 | sm8550 | 一加11（ColorOS 14） |
| 5.15.167 | sm8550 | 一加11、Ace 2 Pro、Ace 3、一加12R、OnePlus Open（ColorOS 15） |
| 5.15.180 | sm8550 / sm7550 / mt6985 | 一加11、Ace 2 Pro、Ace 3、一加12R、Open、Nord CE4、Find X6、Find N3 Flip（ColorOS 16） |

## 编译方式

- 源码：OnePlusOSS 官方 common 仓（gki_defconfig + make LLVM=1）
- 死链修复：官方 common 仓的 `drivers/soc/oplus/storage` 等是指向未开源 vendor 的死链，
  workflow 内自动从 `android_kernel_modules_and_devicetree_*` 仓拉取真实文件替换
- SUSFS：ShirkNeko/susfs4ksu（gki-android12-5.10 / gki-android13-5.15 分支）
- 工具链：Clang 20（r547379）
- 产物：AK3 包（AnyKernel3）

## 与 cctv18 三仓的差异

1. SUSFS 源不同：cctv18 的 susfs4oki 无 5.x 分支，改用 ShirkNeko/susfs4ksu
2. 新增 vendor-fix 步骤：官方 common 仓死链修复（cctv18 是在自家源码仓里预先修好的）
3. 暂不支持 Droidspaces（ntsync 为 6.6+ 特性）
4. 5.10 专用的 CVE 补丁暂缺（cve-2026-43499 补丁为 6.1 专用）

## 状态

- [x] fastbuild_5.10.236.yml（sm8475 样板）
- [ ] 其余 11 个 x
- [ ] hwid 校验版
