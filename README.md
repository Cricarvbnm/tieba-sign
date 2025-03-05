# Usage

**配置**$HOME/.config/tieba-sign/config.toml -> 工作目录为**项目根目录** ->
运行**tieba-sign.sh**或直接执行`PYTHONPATH=./src python ./src/tieba_sign`
（等价于让python能找到./src/tieba_sign这个包，并运行这个包）

如果工作目录不为项目根目录，那么需要向tieba-sign.sh传入一个位置参数，
比如：`tieba-sign.sh path/to/the/project`

# Config

Path: $HOME/.config/tieba-sign/config.toml

```toml
# 登录tieba后，打开网页控制台(F12)，刷新页面之后查看**网络**选项卡的tieba.baidu.com的请求头中的cookie，填写到这里即可
cookie = 'BAIDUID=xxxx; BDUSS=xxxx' 

[request]
concurrency=5 # default 3
```
