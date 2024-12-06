Install [uv](https://docs.astral.sh/uv/).

Run locally:
```
uv run codeblocks --help
```

Modify `usage` block in our README.md:

```
uv run codeblocks usage README.md -- codeblocks --help
```

Publish:
```
uv publish
```