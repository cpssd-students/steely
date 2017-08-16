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
- [ ] async lastfm plugin stuff  
- [ ] trigger decorators for plugins, not just main()  
- [ ] [izaakf](https://github.com/izaakf)'s secret idea

## credits
|plugin|author|
|---|---|
|bus|[AlexKraak](https://github.com/AlexKraak)|
|happy|[AlexKraak](https://github.com/AlexKraak)|
|ht|[AlexKraak](https://github.com/AlexKraak)|
|jokes|[EdwardDowling](https://github.com/EdwardDowling)|
|lastfm|[AlexKraak](https://github.com/AlexKraak)|
|linden|[CianLR](https://github.com/CianLR), [benmcmahon100](https://github.com/benmcmahon100)|
|skrrt|[AlexKraak](https://github.com/AlexKraak)|
|spongemock|[EdwardDowling](https://github.com/EdwardDowling)|
|train|[izaakf](https://github.com/izaakf)|
|urbandict|[EdwardDowling](https://github.com/EdwardDowling)|
|exp|[Byxor](https://github.com/Byxor)|
|roll|[devoxel](https://github.com/devoxel)|

## q&a

- why the shit are some names camelCase? that's not pep8
  - the fbchat module uses them for some reason
- why the shit isn't the linden plugin working?
  - ~~:(~~
  - :)
