# -*- coding: utf-8 -*-
"""五线命名验证: 下载 artifact -> 解 Image -> 读真实内核版本 -> 与文件名比对。

防「名叫 6.6.89 实际是 6.6.118」: Image 二进制内嵌编译时版本串
'Linux version X.Y.Z-...'，X.Y.Z 来自源码 Makefile，是唯一事实。
文件名结构: AnyKernel3_<KSU>_<KSUVER>_<KERNEL_VERSION>_<SUB_VERSION>_<KERNEL_NAME>[-mtk].zip
SUB_VERSION 形如 66/115/23_gki/89_mtk，取数字部分与 X.Y.Z 的第三段比对。
"""
import subprocess, json, os, re, sys, zipfile

RUNS = {
    '5.10': '35455403020',
    '5.15': '35455412779',
    '6.1':  '35455426105',
    '6.6':  '35455438683',
    '6.12': '35455447536',
}
WORK = os.path.abspath('_verify_naming')
REPO = 'BailinT/oppo_oplus_realme_all'

def download(url, dest):
    p = subprocess.run(['gh', 'api', url], capture_output=True)
    # gh api 输出是二进制 artifact（应用 octet-stream）
    with open(dest, 'wb') as f:
        f.write(p.stdout)
    return len(p.stdout)

def image_version(image_bytes):
    m = re.search(rb'Linux version (\d+\.\d+\.\d+)-([^\x00]{0,80})', image_bytes)
    if not m:
        return None, None
    return m.group(1).decode(), m.group(2)[:40].decode(errors='replace')

def main():
    os.makedirs(WORK, exist_ok=True)
    results, fails = [], []
    for line, rid in RUNS.items():
        p = subprocess.run(['gh', 'api', f'repos/{REPO}/actions/runs/{rid}/artifacts?per_page=100'], capture_output=True, text=True)
        d = json.loads(p.stdout)
        arts = [a for a in d['artifacts'] if a['name'].startswith('AnyKernel3_')]
        print(f'=== {line} ({rid}): {len(arts)} AK3 artifacts ===')
        for a in arts:
            name = a['name']
            m = re.match(r'AnyKernel3_\w+_\d+_([\d.]+)_(.+?)_(android[^-]+-[^-]+-.+?)(?:-mtk)?\.zip$', name)
            if not m:
                fails.append(f'{name}: 文件名结构解析失败')
                continue
            kver, sub, kname = m.group(1), m.group(2), m.group(3)
            sub_num = sub.split('_')[0]  # 23_gki -> 23, 89_mtk -> 89
            # 下载
            zpath = os.path.join(WORK, f'{line}_{sub}.zip')
            size = download(f'repos/{REPO}/actions/artifacts/{a["id"]}/zip', zpath)
            if size < 1000000 or open(zpath,'rb').read(2) != b'PK':
                fails.append(f'{name}: 下载异常 {size}B')
                continue
            # 解 Image
            img = None
            with zipfile.ZipFile(zpath) as z:
                for n in z.namelist():
                    if n == 'Image':
                        img = z.read(n)
                        break
            os.remove(zpath)
            if img is None:
                fails.append(f'{name}: 包内无 Image')
                continue
            ver, extra = image_version(img)
            ok = ver is not None and ver == f'{kver}.{sub_num}'
            status = 'OK ' if ok else '*** MISMATCH ***'
            print(f'  {status} {name}')
            print(f'        Image: Linux version {ver}-{extra}')
            results.append((name, ver, ok))
            if not ok:
                fails.append(f'{name}: Image 实际 {ver}, 文件名期望 {kver}.{sub_num}')
    print()
    print(f'共 {len(results)} 包, {sum(1 for r in results if r[2])} 匹配, {len(fails)} 异常')
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
