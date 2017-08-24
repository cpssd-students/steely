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
|---|---------------|
|hel|[devoxel](https://github.com/devoxel/)| creditline
|eight|[sentriz](https://github.com/sentriz/)| creditline
|cage|[sentriz](https://github.com/sentriz/)| creditline
|reload|[sentriz](https://github.com/sentriz/)| creditline
|train|[izaakf](https://github.com/izaakf/)| creditline
|roll|[devoxel](https://github.com/devoxel/)| creditline
|xkcd|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|ht|[alexkraak](https://github.com/alexkraak/)| creditline
|nose|[sentriz](https://github.com/sentriz/)| creditline
|box|[sentriz](https://github.com/sentriz/)| creditline
|tilda|[alexkraak](https://github.com/alexkraak/)| creditline
|github|[alexkraak](https://github.com/alexkraak/)| creditline
|tracker|[sentriz](https://github.com/sentriz/)| creditline
|lastfm|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|rpn|[sentriz](https://github.com/sentriz/)| creditline
|angr|[sentriz](https://github.com/sentriz/)| creditline
|vapor|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|lenn|[sentriz](https://github.com/sentriz/)| creditline
|url|[byxor](https://github.com/byxor/)| creditline
|jokes|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|slag|[devoxel](https://github.com/devoxel/)| creditline
|ha|[alexkraak](https://github.com/alexkraak/)| creditline
|stretch|[CianLR](https://github.com/CianLR/)| creditline
|lim|[byxor](https://github.com/byxor/)| creditline
|mock|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|sentiment|[oskarmcd](https://github.com/oskarmcd/)| creditline
|linden|[CianLR](https://github.com/CianLR/)| creditline
|bus|[alexkraak](https://github.com/alexkraak/)| creditline
|skrrrt|[alexkraak](https://github.com/alexkraak/)| creditline
|restart|[sentriz](https://github.com/sentriz/)| creditline
|urban|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|define|[alexkraak](https://github.com/alexkraak/)| creditline

## q&a

- why the shit are some names camelCase? that's not pep8
  - the fbchat module uses them for some reason
- why the shit isn't the linden plugin working?
  - ~~:(~~
  - :)
