# colonizer

Command-line tool that lets you register a package on PyPi or npm before you have any code ready. This is a terrible tool for bad people. It's potentially damaging to the OSS ecosystem. Please don't use it!

## Installation

```bash
$ pip install colonizer
```

## Usage

Again, I don't recommend using this, but if you must...

**For Python:**

```bash
$ colonizer --pypi your_package_name
```

By default, it will use the author information from your local git config, but you can explicitly specify this like so:

```bash
$ colonizer --pypi your_package_name --author your_username --author-email your_email
```

**For Node:**

```bash
$ colonizer --npm your_package_name
```
