# PyJATS

This is a quick and dirty python tool to deserialise JATS xml into something more useable inside python.

It ain't fast, and probably ain't pretty, but it gets text out of the XML and for now that's enough.

To use it:

```python
from pyjats.parser import parse_xml

article_sections = parse_xml(file_path)
```

This will only work with a file object because reasons, you should wrap a string (e.g. one you got from an xml request to the EuropePMC API) in a `io.StringIO` to have it work.