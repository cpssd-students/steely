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
- [x] [izaakf](https://github.com/izaakf)'s secret idea

## credits
|plugin|author|
|---|---------------|
|haiku|[CianLR](https://github.com/CianLR/)| creditline
|linden|[CianLR](https://github.com/CianLR/)| creditline
|obscene|[CianLR](https://github.com/CianLR/)| creditline
|snoop|[CianLR](https://github.com/CianLR/)| creditline
|stretch|[CianLR](https://github.com/CianLR/)| creditline
|jokes|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|mock|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|urban|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|xkcd|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|bus|[alexkraak](https://github.com/alexkraak/)| creditline
|define|[alexkraak](https://github.com/alexkraak/)| creditline
|github|[alexkraak](https://github.com/alexkraak/)| creditline
|happy|[alexkraak](https://github.com/alexkraak/)| creditline
|skrrrt|[alexkraak](https://github.com/alexkraak/)| creditline
|tilda|[alexkraak](https://github.com/alexkraak/)| creditline
|coinflip|[alexkraak](https://github.com/alexkraak/), [byxor](https://github.com/byxor/)| creditline
|lastfm|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|vapor|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|limp|[byxor](https://github.com/byxor/)| creditline
|url|[byxor](https://github.com/byxor/)| creditline
|basic_interpreter|[cianlr](https://github.com/cianlr/)| creditline
|help|[devoxel](https://github.com/devoxel/)| creditline
|roll|[devoxel](https://github.com/devoxel/)| creditline
|slag|[devoxel](https://github.com/devoxel/)| creditline
|roomcheck|[gruunday](https://github.com/gruunday/)| creditline
|gex|[iandioch](https://github.com/iandioch/)| creditline
|scramble|[iandioch](https://github.com/iandioch/)| creditline
|sort|[iandioch](https://github.com/iandioch/)| creditline
|hello|[izaakf](https://github.com/izaakf/)| creditline
|train|[izaakf](https://github.com/izaakf/)| creditline
|vowel|[izaakf](https://github.com/izaakf/)| creditline
|sentiment|[oskarmcd](https://github.com/oskarmcd/)| creditline
|angry|[sentriz](https://github.com/sentriz/)| creditline
|box|[sentriz](https://github.com/sentriz/)| creditline
|ca|[sentriz](https://github.com/sentriz/)| creditline
|cage|[sentriz](https://github.com/sentriz/)| creditline
|eight|[sentriz](https://github.com/sentriz/)| creditline
|leet|[sentriz](https://github.com/sentriz/)| creditline
|lenny|[sentriz](https://github.com/sentriz/)| creditline
|markov|[sentriz](https://github.com/sentriz/)| creditline
|middle|[sentriz](https://github.com/sentriz/)| creditline
|nose|[sentriz](https://github.com/sentriz/)| creditline
|recordmarkov|[sentriz](https://github.com/sentriz/)| creditline
|recordstat|[sentriz](https://github.com/sentriz/)| creditline
|reload|[sentriz](https://github.com/sentriz/)| creditline
|restart|[sentriz](https://github.com/sentriz/)| creditline
|rpn|[sentriz](https://github.com/sentriz/)| creditline
|stats|[sentriz](https://github.com/sentriz/)| creditline
|tracker|[sentriz](https://github.com/sentriz/)| creditline
|clap|[sentriz](https://github.com/sentriz/), [devoxel](https://github.com/devoxel/)| creditline

## q&a

- why the shit are some names camelCase? that's not pep8
  - the fbchat module uses them for some reason
- why the shit isn't the linden plugin working?
  - ~~:(~~
  - :)
