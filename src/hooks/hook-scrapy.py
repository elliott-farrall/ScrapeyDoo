from PyInstaller.utils.hooks import collect_submodules, collect_data_files # type: ignore

hiddenimports = (
    collect_submodules("scrapy") +
    collect_submodules("scrapy_user_agents") +
    collect_submodules("scrapy_user_agents.middlewares") +
    collect_submodules("scrapy_proxies")
)
datas = collect_data_files("scrapy")
