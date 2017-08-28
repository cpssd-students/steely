![banner](banner.png)

## to install  

```
$ git clone this
$ pip3 install --user -r requirements.txt
or, if you're in a new py3 virtualenv
$ pip install -r requirements.txt

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
|linden|[CianLR](https://github.com/CianLR/)| creditline
|stretch|[CianLR](https://github.com/CianLR/)| creditline
|jokes|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|mock|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|urban|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|xkcd|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|bus|[alexkraak](https://github.com/alexkraak/)| creditline
|define|[alexkraak](https://github.com/alexkraak/)| creditline
|github|[alexkraak](https://github.com/alexkraak/)| creditline
|happy|[alexkraak](https://github.com/alexkraak/)| creditline
|ht|[alexkraak](https://github.com/alexkraak/)| creditline
|skrrrt|[alexkraak](https://github.com/alexkraak/)| creditline
|tilda|[alexkraak](https://github.com/alexkraak/)| creditline
|lastfm|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|vapor|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|limp|[byxor](https://github.com/byxor/)| creditline
|url|[byxor](https://github.com/byxor/)| creditline
|help|[devoxel](https://github.com/devoxel/)| creditline
|roll|[devoxel](https://github.com/devoxel/)| creditline
|slag|[devoxel](https://github.com/devoxel/)| creditline
|train|[izaakf](https://github.com/izaakf/)| creditline
|sentiment|[oskarmcd](https://github.com/oskarmcd/)| creditline
|angry|[sentriz](https://github.com/sentriz/)| creditline
|box|[sentriz](https://github.com/sentriz/)| creditline
|cage|[sentriz](https://github.com/sentriz/)| creditline
|eight|[sentriz](https://github.com/sentriz/)| creditline
|lenny|[sentriz](https://github.com/sentriz/)| creditline
|nose|[sentriz](https://github.com/sentriz/)| creditline
|reload|[sentriz](https://github.com/sentriz/)| creditline
|restart|[sentriz](https://github.com/sentriz/)| creditline
|rpn|[sentriz](https://github.com/sentriz/)| creditline
|tracker|[sentriz](https://github.com/sentriz/)| creditline

## q&a

- why the shit are some names camelCase? that's not pep8
  - the fbchat module uses them for some reason
- why the shit isn't the linden plugin working?
  - ~~:(~~
  - :)
