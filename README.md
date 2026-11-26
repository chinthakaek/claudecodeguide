# Claude Code: A Beginner's Guide and Best Practices

A practical guide for people new to [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), Anthropic's AI coding assistant for the terminal.

- **Read it online:** see the GitHub Pages link in this repo's About section
- **Source:** [`Claude_Code_Guide.md`](Claude_Code_Guide.md)

## Updating the site

`index.html` is generated from the Markdown. After editing `Claude_Code_Guide.md`:

```bash
pip install markdown          # first time only
python3 tools/build.py Claude_Code_Guide.md index.html
git add -A && git commit -m "Update guide" && git push
```

GitHub Pages republishes automatically within a minute or two.

## Disclaimer

Community guide. Not an official Anthropic publication, and not affiliated with or endorsed by Anthropic.
