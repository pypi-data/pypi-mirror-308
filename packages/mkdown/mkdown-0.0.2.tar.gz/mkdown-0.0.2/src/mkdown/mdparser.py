import functools
import json
from pathlib import Path
from typing import Any

import bleach
from bs4 import BeautifulSoup
import commonmark
import markdown
import markdown2


class MarkdownConverter:
    """An extended wrapper class for markdown to HTML conversion libraries.
    Supports multiple markdown flavors, caching, sanitization, and custom extensions.
    """

    SUPPORTED_ENGINES = [
        "python-markdown",
        "mistune",
        "markdown2",
        "commonmark",
        "markdownify",
        "mdx_math",
    ]

    # Cache for converter instances
    _converter_cache = {}

    def __init__(
        self,
        engine: str = "python-markdown",
        cache_enabled: bool = True,
        sanitize: bool = True,
        pretty_output: bool = False,
    ):
        """Initialize the markdown converter.

        Args:
            engine (str): The markdown engine to use
            cache_enabled (bool): Whether to cache converter instances
            sanitize (bool): Whether to sanitize HTML output
            pretty_output (bool): Whether to format HTML output
        """
        if engine not in self.SUPPORTED_ENGINES:
            raise ValueError(f"Unsupported engine. Choose from: {self.SUPPORTED_ENGINES}")

        self.engine = engine
        self.cache_enabled = cache_enabled
        self.sanitize = sanitize
        self.pretty_output = pretty_output
        self._setup_engine()

    def _get_cache_key(self, extensions: list[str] | None, **kwargs) -> str:
        """Generate a cache key based on configuration."""
        cache_data = {
            "engine": self.engine,
            "extensions": sorted(extensions) if extensions else None,
            **kwargs,
        }
        return json.dumps(cache_data, sort_keys=True)

    @functools.lru_cache(maxsize=128)
    def _get_cached_converter(self, cache_key: str):
        """Get or create a cached converter instance."""
        return self._converter_cache.get(cache_key)

    def _setup_engine(self):
        """Set up the chosen markdown engine with default configurations."""
        if self.engine == "python-markdown":
            import markdown

            self.converter = markdown.Markdown(extensions=["extra"])
        elif self.engine == "mistune":
            import mistune

            self.converter = mistune.create_markdown()
        elif self.engine == "markdown2":
            import markdown2

            self.converter = markdown2.Markdown()
        elif self.engine == "commonmark":
            import commonmark

            self.converter = commonmark.Parser()
        elif self.engine == "mdx_math":
            self.converter = markdown.Markdown(extensions=["mdx_math"])

    def load_custom_extension(self, extension_path: str | Path) -> Any:
        """Load a custom markdown extension from a Python file.

        Args:
            extension_path: Path to the extension file
        Returns:
            The loaded extension class/object
        """
        extension_path = Path(extension_path)
        if not extension_path.exists():
            raise FileNotFoundError(f"Extension file not found: {extension_path}")

        import importlib.util

        spec = importlib.util.spec_from_file_location(extension_path.stem, extension_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Extension

    def sanitize_html(self, html_content: str, **kwargs) -> str:
        """Sanitize HTML content using bleach.

        Args:
            html_content: HTML content to sanitize
            **kwargs: Additional bleach options
        Returns:
            Sanitized HTML content
        """
        allowed_tags = kwargs.get("allowed_tags", bleach.ALLOWED_TAGS)
        allowed_attributes = kwargs.get("allowed_attributes", bleach.ALLOWED_ATTRIBUTES)
        allowed_protocols = kwargs.get("allowed_protocols", bleach.ALLOWED_PROTOCOLS)

        return bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            protocols=allowed_protocols,
            strip=kwargs.get("strip", True),
            strip_comments=kwargs.get("strip_comments", True),
        )

    def format_html(self, html_content: str) -> str:
        """Format HTML content for better readability."""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.prettify()

    def convert(
        self,
        text: str,
        extensions: list[str] | None = None,
        admonitions: bool = False,
        custom_extensions: list[str | Path] | None = None,
        sanitize_options: dict | None = None,
        **kwargs,
    ) -> str:
        """Convert markdown text to HTML with extended options.

        Args:
            text: The markdown text to convert
            extensions: List of extensions to use
            admonitions: Whether to enable admonitions
            custom_extensions: List of paths to custom extensions
            sanitize_options: Options for HTML sanitization
            **kwargs: Additional engine-specific options

        Returns:
            The converted HTML text
        """
        # Load custom extensions if provided
        if custom_extensions:
            loaded_extensions = [
                self.load_custom_extension(ext) for ext in custom_extensions
            ]
            if extensions:
                extensions.extend(loaded_extensions)
            else:
                extensions = loaded_extensions

        # Get cached converter or create new one
        if self.cache_enabled:
            cache_key = self._get_cache_key(extensions, **kwargs)
            converter = self._get_cached_converter(cache_key)
            if converter:
                html_content = converter.convert(text)
            else:
                html_content = self._convert_with_engine(
                    text, extensions, admonitions, **kwargs
                )
                self._converter_cache[cache_key] = self.converter
        else:
            html_content = self._convert_with_engine(
                text, extensions, admonitions, **kwargs
            )

        # Apply sanitization if enabled
        if self.sanitize:
            sanitize_options = sanitize_options or {}
            html_content = self.sanitize_html(html_content, **sanitize_options)

        # Format output if enabled
        if self.pretty_output:
            html_content = self.format_html(html_content)

        return html_content

    def _convert_with_engine(
        self, text: str, extensions: list[str] | None, admonitions: bool, **kwargs
    ) -> str:
        """Handle conversion with specific engine."""
        if self.engine == "python-markdown":
            return self._convert_python_markdown(text, extensions, admonitions, **kwargs)
        if self.engine == "mistune":
            return self._convert_mistune(text, **kwargs)
        if self.engine == "markdown2":
            return self._convert_markdown2(text, extensions, admonitions, **kwargs)
        if self.engine == "commonmark":
            return self._convert_commonmark(text, **kwargs)
        if self.engine == "mdx_math":
            return self._convert_mdx_math(text, extensions, **kwargs)
        raise ValueError(f"Unsupported engine: {self.engine}")

    def _convert_commonmark(self, text: str, **kwargs) -> str:
        """Handle commonmark specific conversion."""
        parser = commonmark.Parser()
        renderer = commonmark.HtmlRenderer(**kwargs)
        ast = parser.parse(text)
        return renderer.render(ast)

    def _convert_mdx_math(self, text: str, extensions: list[str] | None, **kwargs) -> str:
        """Handle mdx_math specific conversion."""
        ext_list = extensions or ["mdx_math"]
        if "mdx_math" not in ext_list:
            ext_list.append("mdx_math")

        md = markdown.Markdown(extensions=ext_list)
        return md.convert(text)

    # ... (previous conversion methods remain the same)

    @staticmethod
    def get_supported_extensions(engine: str) -> list[str]:
        """Get list of supported extensions for the specified engine."""
        extension_map = {
            "python-markdown": markdown.util.get_installed_extensions(),
            "markdown2": markdown2.DEFAULT_EXTRAS,
            "mistune": ["tables", "footnotes", "strikethrough", "task_lists"],
            "commonmark": ["smartpunct", "table", "strikethrough"],
            "mdx_math": ["mdx_math", "extra", "codehilite"],
        }
        return extension_map.get(engine, [])
