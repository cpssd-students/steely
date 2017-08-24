![banner](banner.png)

## to install  

```
$ git clone this
$ pip3 install --user -r requirements.txt
```

## to run
```
$ mv config.py.sample config.py
$ edit config.py
$ python3 steelybot.py
```
(`config.py` is in `.gitignore`)

## to run tests
```
$ make test
```
or simply...
```
$ nosetest
```

If the tests are failing to import, you probably aren't in the virtualenv.

## how to write help for you commands

Throw a doc string in the top of the plugin.

If it's short just make it one line but if its `thicc` and has subcommands check
steely/plugins/linden for an example.

## todo
- [x] async lastfm plugin stuff  
- [ ] trigger decorators for plugins, not just main()  
- [ ] [izaakf](https://github.com/izaakf)'s secret idea

## credits
|plugin|author|
|---|---|
|bus|[AlexKraak](https://github.com/AlexKraak)| pluginline
|happy|[AlexKraak](https://github.com/AlexKraak)| pluginline
|ht|[AlexKraak](https://github.com/AlexKraak)| pluginline
|jokes|[EdwardDowling](https://github.com/EdwardDowling)| pluginline
|lastfm|[AlexKraak](https://github.com/AlexKraak)| pluginline
|linden|[CianLR](https://github.com/CianLR), [benmcmahon100](https://github.com/benmcmahon100)| pluginline
|skrrt|[AlexKraak](https://github.com/AlexKraak)| pluginline
|spongemock|[EdwardDowling](https://github.com/EdwardDowling)| pluginline
|train|[izaakf](https://github.com/izaakf)| pluginline
|urbandict|[EdwardDowling](https://github.com/EdwardDowling)| pluginline
|exp|[Byxor](https://github.com/Byxor)| pluginline
|roll|[devoxel](https://github.com/devoxel)| pluginline

## q&a

- why the shit are some names camelCase? that's not pep8
  - the fbchat module uses them for some reason
- why the shit isn't the linden plugin working?
  - ~~:(~~
  - :)
