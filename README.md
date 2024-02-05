# tg-gpt

```bash
docker build . -t tg-gpt
```

```bash
docker run -d --restart=always --name tg-gpt tg-gpt
```

```bash
docker run -d --restart=always  --privileged --dns 1.1.1.1 --sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun --name tg-gpt tg-gpt
```

```bash
docker tag  tg-gpt cr.yandex/crpp8ardv4ho3uda0ghk/tg-gpt:hello
```

```bash
docker push cr.yandex/crpp8ardv4ho3uda0ghk/tg-gpt:hello
```

```bash
docker run -d --restart=always --name tg-gpt-test cr.yandex/crpp8ardv4ho3uda0ghk/tg-gpt:hello
```
