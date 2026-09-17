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

- [x] fastbuild_5.10.236.yml（sm8475 样板）— ✅ 2026-09-18 跑绿（run 35250898100），AK3/release 产物抽验通过
- [x] 其余 11 个 x（2026-09-18 批量生成，源分支全部 ls-remote + Makefile 实测核对）
- [ ] hwid 校验版

## 首跑选源表（实测：ls-remote 分支 + 抓 Makefile 读 SUBLEVEL）

| workflow | 平台(芯片) | 官方源码分支（实测 = 该 x） | 替换源仓 |
|---|---|---|---|
| fastbuild_5.10.66.yml | mt6895(天玑8100) | android_kernel_5.10_oneplus_mt6895 @ `oneplus/mt6895_s_12.1_oneplus_10r` = 5.10.66 | vendor_mediatek_kernel_modules_mt6895 @ 同名分支（仅 cpu 有替换源，storage 条件跳过） |
| fastbuild_5.10.110.yml | mt6895(天玑8100) | android_kernel_5.10_oneplus_mt6895 @ `oneplus/mt6895_t_13.0.0` = 5.10.110 | 同上 |
| fastbuild_5.10.149.yml | mt6895(天玑8100) | android_kernel_5.10_oneplus_mt6895 @ `mt6895_t_13.1.0_oneplus_ace` = 5.10.149（注意无 oneplus/ 前缀） | 同上 |
| fastbuild_5.10.168.yml | mt6895(天玑8100) | android_kernel_5.10_oneplus_mt6895 @ `oneplus/mt6895_u_14.0.0_ace` = 5.10.168 | 同上 |
| fastbuild_5.10.198.yml | mt6983(天玑9000) | android_kernel_5.10_oneplus_mt6983 @ `oneplus_mt6983_u_14.0.0_nord_3_5g` = 5.10.198（无前缀） | android_kernel_modules_oneplus_mt6983 @ 同名分支（storage+cpu 全有） |
| fastbuild_5.10.209.yml | sm8475(骁龙8+Gen1) | android_kernel_common_oneplus_sm8475 @ `oneplus/sm8475_u_14.0.0_oneplus_11r_5g` = 5.10.209 | devicetree_sm8475 @ 同名分支 |
| fastbuild_5.10.226.yml | sm8475(骁龙8+Gen1) | android_kernel_common_oneplus_sm8475 @ `oneplus/sm8475_v_15.0.0_ace_2` = 5.10.226 | 同上 |
| fastbuild_5.15.74.yml | sm8550(骁龙8 Gen2) | android_kernel_common_oneplus_sm8550 @ `oneplus/sm8550_t_13.1.0_oneplus11` = 5.15.74 | devicetree_sm8550 @ 同名分支 |
| fastbuild_5.15.123.yml | sm8550(骁龙8 Gen2) | android_kernel_common_oneplus_sm8550 @ `oneplus/sm8550_u_14.0.0_oneplus11` = 5.15.123 | 同上 |
| fastbuild_5.15.167.yml | sm8550(骁龙8 Gen2) | android_kernel_common_oneplus_sm8550 @ `oneplus/sm8550_v_15.0.0_ace_2_pro` = 5.15.167 | 同上 |
| fastbuild_5.15.180.yml | sm8550(骁龙8 Gen2) | android_kernel_common_oneplus_sm8550 @ `oneplus/sm8550_b_16.0.0_ace_2_pro` = 5.15.180 | 同上（Nord CE4=sm7550、Find X6=mt6985 变体待加） |

实测补充：sm8450 @ `oneplus/sm8450_s_12.1_10_pro` 也是 5.10.66（10Pro 变体待加）；sm7550 b_16/v_15 均 = 5.15.180；mt6983 u_14 有 168(ace_2v)/198(nord3) 两条；mt6895 v_15 混有 209/236 两条；mt6985 无 5.15 源仓。SUSFS 5.15 用 ShirkNeko `gki-android13-5.15`（补丁实测存在）。天玑树 vendor-fix 全条件式（死链存在且替换源存在才动）。
