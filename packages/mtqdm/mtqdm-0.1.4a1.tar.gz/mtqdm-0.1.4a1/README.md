# mtqdm v0.1.4a1

> ⚠️ **Warning**: This project is VERY MUCH in alpha. While it works (a little bit), it was written in a single sitting exclusively using Cursor; which is amazing but also means I haven't authored a single line of code, or even read through tqdm, or rumps' docs. Expect major rough edges, but improvements are actively being made. Especially since this is a tool I'll be using myself.

Put tqdm on your menu bar.

## Usage

```bash
pip install mtqdm
```

My intentions for mtqdm is for it to be a *drop-in replacement* for **tqdm**.
So simply replace **tqdm** with **mtqdm** in your code.

```python
from mtqdm import mtqdm
for _ in mtqdm(range(100)):
    # ...
```

![mtqdm-0.1.4a1 in action](https://github.com/0oj/mtqdm/blob/main/examples/basic_usage.png?raw=true)

The progress bar from **tqdm** will still be displayed in the terminal. Additionally, a progress bar like the one above will appear in the menu bar. Clicking it will reveal metrics.

`100%|████████████████████| 100/100 [00:15<00:00,  6.50it/s]`