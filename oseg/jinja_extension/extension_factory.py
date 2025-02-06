from oseg import jinja_extension as j, configs


class ExtensionFactory:
    @staticmethod
    def factory(config: "configs.BaseConfig") -> "j.BaseExtension":
        if isinstance(config, configs.CSharpConfig):
            return j.CSharpExtension(config)

        if isinstance(config, configs.JavaConfig):
            return j.JavaExtension(config)

        if isinstance(config, configs.PhpConfig):
            return j.PhpExtension(config)

        if isinstance(config, configs.PythonConfig):
            return j.PythonExtension(config)

        if isinstance(config, configs.RubyConfig):
            return j.RubyExtension(config)

        if isinstance(config, configs.TypescriptNodeConfig):
            return j.TypescriptNodeExtension(config)

        raise NotImplementedError

    @staticmethod
    def default_generator_names() -> list[str]:
        return [
            j.CSharpExtension.NAME,
            j.JavaExtension.NAME,
            j.PhpExtension.NAME,
            j.PythonExtension.NAME,
            j.RubyExtension.NAME,
            j.TypescriptNodeExtension.NAME,
        ]
