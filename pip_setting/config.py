"""配置文件编辑: pip.ini 用 configparser, uv.toml 按行精准编辑。"""
import configparser
from pathlib import Path

UTF8 = "UTF8"


def _write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding=UTF8)


def set_ini_keys(path: Path, updates):
    """在 ini 文件里设置键值, updates 为 {小节: {键: 值}}
    文件由 configparser 标准化重写，注释不保留。"""
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(path, encoding=UTF8)
    for section, keys in updates.items():
        if not parser.has_section(section):
            parser.add_section(section)
        for k, v in keys.items():
            parser.set(section, k, v)
    with path.open("w", encoding=UTF8) as f:
        parser.write(f)


def remove_ini_keys(path: Path, updates):
    """从 ini 文件删除指定键；空小节连 header 删，文件删空则删文件。"""
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(path, encoding=UTF8)
    for section, keys in updates.items():
        if not parser.has_section(section):
            continue
        for k in keys:
            parser.remove_option(section, k)
        if not parser.options(section):
            parser.remove_section(section)
    if parser.sections():
        with path.open("w", encoding=UTF8) as f:
            parser.write(f)
    else:
        path.unlink()


def _default_line(lines):
    """default 键所在行号，没有则 None。uv.toml 里 default 键只出现在 [[index]] 块中。"""
    return next((i for i, l in enumerate(lines) if l.split("=")[0].strip() == "default"), None)


def set_uv_index(path: Path, url):
    """把 url 设为 uv 默认源：改写原默认块的 url; 无默认块则追加一个;
    其余 index 块的 default 置 false。除这些键外原文件内容不动。"""
    lines = path.read_text(encoding=UTF8).splitlines() if path.exists() else []
    target = _default_line(lines)
    for i, l in enumerate(lines):
        if i != target and l.split("=")[0].strip() == "default":
            lines[i] = "default = false"
    if target is None:
        lines += ([""] if lines else []) + ["[[index]]", f'url = "{url}"', "default = true"]
    else:
        start = max(i for i in range(target + 1) if lines[i].lstrip().startswith("[["))
        hit = next((i for i in range(start, target) if lines[i].split("=")[0].strip() == "url"), None)
        if hit is None:
            lines.insert(target, f'url = "{url}"')
        else:
            lines[hit] = f'url = "{url}"'
    _write(path, lines)


def remove_uv_index(path: Path):
    """删除标记为 default 的整个 index 块；文件删空则删文件。"""
    if not path.exists():
        return
    lines = path.read_text(encoding=UTF8).splitlines()
    target = _default_line(lines)
    if target is not None:
        start = max(i for i in range(target + 1) if lines[i].lstrip().startswith("[["))
        end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("[")), len(lines))
        del lines[start:end]
    if any(l.strip() for l in lines):
        path.write_text("\n".join(lines) + "\n", encoding=UTF8)
    else:
        path.unlink()
