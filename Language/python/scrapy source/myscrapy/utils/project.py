import os
import warnings
from importlib import import_module
from pathlib import Path

from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.conf import closest_scrapy_cfg, get_config, init_env

ENVVAR = "SCRAPY_SETTINGS_MODULE"
DATADIR_CFG_SECTION = "datadir"


def inside_project():
    """运行环境是否在爬虫项目中的依据就是能否找到 scrapy.cfg 文件，
    如果能找到，则说明是在爬虫项目中，否则就认为是执行的全局命令。"""
    scrapy_module = os.environ.get("SCRAPY_SETTINGS_MODULE")
    if scrapy_module is not None:
        try:
            import_module(scrapy_module)
        except ImportError as exc:
            warnings.warn(
                f"Cannot import scrapy settings module {scrapy_module}: {exc}"
            )
        else:
            return True
    return bool(closest_scrapy_cfg())


def project_data_dir(project="default") -> str:
    """Return the current project data dir, creating it if it doesn't exist"""
    if not inside_project():
        raise NotConfigured("Not inside a project")
    cfg = get_config()
    if cfg.has_option(DATADIR_CFG_SECTION, project):
        d = Path(cfg.get(DATADIR_CFG_SECTION, project))
    else:
        scrapy_cfg = closest_scrapy_cfg()
        if not scrapy_cfg:
            raise NotConfigured(
                "Unable to find scrapy.cfg file to infer project data dir"
            )
        d = (Path(scrapy_cfg).parent / ".scrapy").resolve()
    if not d.exists():
        d.mkdir(parents=True)
    return str(d)


def data_path(path: str, createdir=False) -> str:
    """
    Return the given path joined with the .scrapy data directory.
    If given an absolute path, return it unmodified.
    """
    path_obj = Path(path)
    if not path_obj.is_absolute():
        if inside_project():
            path_obj = Path(project_data_dir(), path)
        else:
            path_obj = Path(".scrapy", path)
    if createdir and not path_obj.exists():
        path_obj.mkdir(parents=True)
    return str(path_obj)


def get_project_settings():
    # 检查环境变量中是否有 'SCRAPY_SETTINGS_MODULE'
    if ENVVAR not in os.environ:
        project = os.environ.get("SCRAPY_PROJECT", "default")
        # 初始化环境 找到用户配置文件settings.py 设置到环境变量SCRAPY_SETTINGS_MODULE中
        init_env(project)
    # 加载default_settings.py文件中的默认配置
    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        # 添加用户配置，覆盖默认配置
        settings.setmodule(settings_module_path, priority="project")

    valid_envvars = {
        "CHECK",
        "PROJECT",
        "PYTHON_SHELL",
        "SETTINGS_MODULE",
    }
    # 如果环境变量中有其他scrapy相关配置也覆盖

    scrapy_envvars = {
        k[7:]: v
        for k, v in os.environ.items()
        if k.startswith("SCRAPY_") and k.replace("SCRAPY_", "") in valid_envvars
    }

    settings.setdict(scrapy_envvars, priority="project")

    return settings
