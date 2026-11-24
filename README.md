# fsize

List files in a directory tree with their sizes and show a total.

## Usage

```
python fsize.py [path] [--sort size|name] [--top N]
```

Examples:

```
python fsize.py                    # scan the current directory
python fsize.py Downloads --top 10  # 10 largest files
python fsize.py --sort name --top 5
```
