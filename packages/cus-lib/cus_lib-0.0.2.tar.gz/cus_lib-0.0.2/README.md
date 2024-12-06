# `__init__.py`中写法
1. 使用方式
2. 导包，可选

```
cus_lib

Usage:

    from cus_log import setup_logger

    logger = setup_logger("test.log")
    logger.info('test cus_lib!')
"""

# after you launch code,can see 'test.log' file. 
```

# build

```bash
py -m build
```

# 分发

```bash
twine upload dist/*
# 输入token
```

