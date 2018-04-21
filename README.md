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

## thanks (related to the cpssd steely instance)
  - to [CianLR](https://github.com/cianLR/) for bailing me out of DO bills to get the dbs/logs backs
  - to [devoxel](https://github.com/devoxel) for hosting after the bailout
  - the contributors below

## credits
|plugin|author|
|---|---------------|
|[haiku](steely/plugins/haiku.py)|[CianLR](https://github.com/CianLR/)| creditline
|[linden](steely/plugins/linden.py)|[CianLR](https://github.com/CianLR/)| creditline
|[obscene](steely/plugins/obscene.py)|[CianLR](https://github.com/CianLR/)| creditline
|[snoop](steely/plugins/snoop.py)|[CianLR](https://github.com/CianLR/)| creditline
|[stretch](steely/plugins/stretch.py)|[CianLR](https://github.com/CianLR/)| creditline
|[jokes](steely/plugins/jokes.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[mock](steely/plugins/mock.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[urban](steely/plugins/urban.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[xkcd](steely/plugins/xkcd.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[bus](steely/plugins/bus.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[define](steely/plugins/define.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[github](steely/plugins/github.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[happy](steely/plugins/happy.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[skrrrt](steely/plugins/skrrrt.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[tilda](steely/plugins/tilda.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[coinflip](steely/plugins/coinflip.py)|[alexkraak](https://github.com/alexkraak/), [byxor](https://github.com/byxor/)| creditline
|[lastfm](steely/plugins/lastfm.py)|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|[vapor](steely/plugins/vapor.py)|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|[limp](steely/plugins/limp.py)|[byxor](https://github.com/byxor/)| creditline
|[url](steely/plugins/url.py)|[byxor](https://github.com/byxor/)| creditline
|[basic_interpreter](steely/plugins/basic_interpreter.py)|[cianlr](https://github.com/cianlr/)| creditline
|[help](steely/plugins/help.py)|[devoxel](https://github.com/devoxel/)| creditline
|[roll](steely/plugins/roll.py)|[devoxel](https://github.com/devoxel/)| creditline
|[slag](steely/plugins/slag.py)|[devoxel](https://github.com/devoxel/)| creditline
|[roomcheck](steely/plugins/roomcheck.py)|[gruunday](https://github.com/gruunday/)| creditline
|[gex](steely/plugins/gex.py)|[iandioch](https://github.com/iandioch/)| creditline
|[scramble](steely/plugins/scramble.py)|[iandioch](https://github.com/iandioch/)| creditline
|[sort](steely/plugins/sort.py)|[iandioch](https://github.com/iandioch/)| creditline
|[hello](steely/plugins/hello.py)|[izaakf](https://github.com/izaakf/)| creditline
|[train](steely/plugins/train.py)|[izaakf](https://github.com/izaakf/)| creditline
|[vowel](steely/plugins/vowel.py)|[izaakf](https://github.com/izaakf/)| creditline
|[sentiment](steely/plugins/sentiment.py)|[oskarmcd](https://github.com/oskarmcd/)| creditline
|[angry](steely/plugins/angry.py)|[sentriz](https://github.com/sentriz/)| creditline
|[box](steely/plugins/box.py)|[sentriz](https://github.com/sentriz/)| creditline
|[ca](steely/plugins/ca.py)|[sentriz](https://github.com/sentriz/)| creditline
|[cage](steely/plugins/cage.py)|[sentriz](https://github.com/sentriz/)| creditline
|[eight](steely/plugins/eight.py)|[sentriz](https://github.com/sentriz/)| creditline
|[leet](steely/plugins/leet.py)|[sentriz](https://github.com/sentriz/)| creditline
|[lenny](steely/plugins/lenny.py)|[sentriz](https://github.com/sentriz/)| creditline
|[markov](steely/plugins/markov.py)|[sentriz](https://github.com/sentriz/)| creditline
|[middle](steely/plugins/middle.py)|[sentriz](https://github.com/sentriz/)| creditline
|[nose](steely/plugins/nose.py)|[sentriz](https://github.com/sentriz/)| creditline
|[recordmarkov](steely/plugins/recordmarkov.py)|[sentriz](https://github.com/sentriz/)| creditline
|[recordstat](steely/plugins/recordstat.py)|[sentriz](https://github.com/sentriz/)| creditline
|[reload](steely/plugins/reload.py)|[sentriz](https://github.com/sentriz/)| creditline
|[restart](steely/plugins/restart.py)|[sentriz](https://github.com/sentriz/)| creditline
|[rpn](steely/plugins/rpn.py)|[sentriz](https://github.com/sentriz/)| creditline
|[stats](steely/plugins/stats.py)|[sentriz](https://github.com/sentriz/)| creditline
|[tracker](steely/plugins/tracker.py)|[sentriz](https://github.com/sentriz/)| creditline
|[clap](steely/plugins/clap.py)|[sentriz](https://github.com/sentriz/), [devoxel](https://github.com/devoxel/)| creditline
