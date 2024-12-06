import logging
import os
import pathlib
import platform
import typing

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")

__all__ = (
    "get_python_ver",
    "get_python_ver_major",
    "get_config_filepath",
    "get_embed_archive_name",
    "get_assets_dir",
    "get_depends_filepath",
    "get_embed_dir",
    "get_embed_filepath",
    "get_lib_dir",
    "get_dist_dir",
    "get_runtime_dir",
)

_cache_dir: typing.Optional[pathlib.Path] = None
_embed_dir: typing.Optional[pathlib.Path] = None
_lib_dir: typing.Optional[pathlib.Path] = None
_assets_dir: typing.Optional[pathlib.Path] = None
_config_path: typing.Optional[pathlib.Path] = None
_depends_path: typing.Optional[pathlib.Path] = None
_embed_path: typing.Optional[pathlib.Path] = None
_python_ver: typing.Optional[str] = None
_python_ver_major: typing.Optional[str] = None
_arch: typing.Optional[str] = None
_archive_file: typing.Optional[str] = None


def get_python_ver() -> str:
    global _python_ver

    if not _python_ver:
        _python_ver = platform.python_version()
        logging.info(f"python版本: [{_python_ver}]")

    return _python_ver


def get_python_ver_major() -> str:
    global _python_ver_major

    if not _python_ver_major:
        _python_ver_major = ".".join(platform.python_version_tuple()[:2])
        logging.info(f"python主版本: [{_python_ver_major}]")

    return _python_ver_major


def _get_arch() -> str:
    global _arch

    if not _arch:
        _arch = platform.machine().lower()
        logging.info(f"系统架构: [{_arch}]")

    return _arch


def _get_cached_dir() -> pathlib.Path:
    """获取系统缓存目录"""

    global _cache_dir

    if _cache_dir is None:
        env = os.getenv("FSPACKER_CACHE_DIR")
        _cache_dir = pathlib.Path(env) if env else None

        if _cache_dir:
            _cache_dir = pathlib.Path(_cache_dir).expanduser()
        else:
            _cache_dir = pathlib.Path("~").expanduser() / ".cache" / "fspacker"

        if not _cache_dir.exists():
            logging.info(f"创建缓存文件夹: [{_cache_dir}]")
            _cache_dir.mkdir(parents=True)
        else:
            logging.info(f"缓存文件夹: [{_cache_dir}]")

    return _cache_dir


def get_config_filepath() -> pathlib.Path:
    global _config_path

    if _config_path is None:
        _config_path = _get_cached_dir() / "config.json"
        logging.info(f"配置文件: [{_config_path}]")

    return _config_path


def get_embed_archive_name() -> str:
    """获取 embed 文件压缩包名称"""
    global _archive_file

    if _archive_file is None:
        _archive_file = f"python-{get_python_ver()}-embed-{_get_arch()}.zip"

    return _archive_file


def get_assets_dir() -> pathlib.Path:
    """获取 assets 文件夹"""
    global _assets_dir

    if _assets_dir is None:
        _assets_dir = pathlib.Path(__file__).parent / "assets"
        assert _assets_dir.exists()
        logging.info(f"获取 assets 目录: [{_assets_dir}]")

    return _assets_dir


def get_depends_filepath() -> pathlib.Path:
    global _depends_path

    if _depends_path is None:
        _depends_path = get_assets_dir() / "depends.toml"
        logging.info(f"依赖文件: [{_depends_path}]")

    return _depends_path


def get_embed_dir() -> pathlib.Path:
    """获取 embed 文件夹"""
    global _embed_dir

    if _embed_dir is None:
        _embed_dir = _get_cached_dir() / "embed-repo"

        if not _embed_dir.exists():
            logging.info(f"创建 embed 库目录: [{_embed_dir}]")
            _embed_dir.mkdir(parents=True)
        else:
            logging.info(f"embed 库目录: [{_embed_dir}]")

    return _embed_dir


def get_embed_filepath() -> pathlib.Path:
    global _embed_path

    if _embed_path is None:
        _embed_path = get_embed_dir() / get_embed_archive_name()
        logging.info(f"embed 压缩包路径: [{_embed_path}]")

    return _embed_path


def get_lib_dir() -> pathlib.Path:
    global _lib_dir

    if _lib_dir is None:
        env = os.getenv("FSPACKER_LIB_DIR")
        _lib_dir = pathlib.Path(env) if env else None

        if _lib_dir:
            _lib_dir = pathlib.Path(_lib_dir).expanduser()
            logging.info(f"获取环境变量库目录: [{_lib_dir}]")
        else:
            _lib_dir = _get_cached_dir() / "lib-repo"
            logging.info(
                f"未设置环境变量[FSPACKER_LIB_DIR], 获取默认库目录: [{_lib_dir}]"
            )

        if not _lib_dir.exists():
            logging.info(f"创建库目录: {_lib_dir}")
            _lib_dir.mkdir(exist_ok=True, parents=True)

    return _lib_dir


def get_dist_dir(project_dir: pathlib.Path) -> pathlib.Path:
    return project_dir / "dist"


def get_runtime_dir(project_dir: pathlib.Path) -> pathlib.Path:
    return get_dist_dir(project_dir) / "runtime"
