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

## how to write help for your commands

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
|[bubble](steely/plugins/bubble.py)|[CianLR](https://github.com/CianLR/)| creditline
|[deepdream](steely/plugins/deepdream.py)|[CianLR](https://github.com/CianLR/)| creditline
|[haiku](steely/plugins/haiku.py)|[CianLR](https://github.com/CianLR/)| creditline
|[imgur](steely/plugins/imgur.py)|[CianLR](https://github.com/CianLR/)| creditline
|[linden](steely/plugins/linden.py)|[CianLR](https://github.com/CianLR/)| creditline
|[obscene](steely/plugins/obscene.py)|[CianLR](https://github.com/CianLR/)| creditline
|[parrot](steely/plugins/parrot.py)|[CianLR](https://github.com/CianLR/)| creditline
|[snoop](steely/plugins/snoop.py)|[CianLR](https://github.com/CianLR/)| creditline
|[streets](steely/plugins/streets.py)|[CianLR](https://github.com/CianLR/)| creditline
|[stretch](steely/plugins/stretch.py)|[CianLR](https://github.com/CianLR/)| creditline
|[tm](steely/plugins/tm.py)|[CianLR](https://github.com/CianLR/)| creditline
|[translate](steely/plugins/translate.py)|[CianLR](https://github.com/CianLR/)| creditline
|[btc](steely/plugins/btc.py)|[CianLR](https://github.com/CianLR/), [byxor](https://github.com/byxor/), [itsdoddsy](https://github.com/itsdoddsy/)| creditline
|[jokes](steely/plugins/jokes.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[mock](steely/plugins/mock.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[search](steely/plugins/search.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[urban](steely/plugins/urban.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[xkcd](steely/plugins/xkcd.py)|[EdwardDowling](https://github.com/EdwardDowling/)| creditline
|[numberwang](steely/plugins/numberwang.py)|[Hevehan](https://github.com/Hevehan/)| creditline
|[cowsay](steely/plugins/cowsay.py)|[Smurphicus](https://github.com/Smurphicus/)| creditline
|[owo](steely/plugins/owo.py)|[Smurphicus](https://github.com/Smurphicus/)| creditline
|[wednesday](steely/plugins/wednesday.py)|[Smurphicus](https://github.com/Smurphicus/)| creditline
|[bus](steely/plugins/bus.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[define](steely/plugins/define.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[github](steely/plugins/github.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[happy](steely/plugins/happy.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[skrrrt](steely/plugins/skrrrt.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[tilda](steely/plugins/tilda.py)|[alexkraak](https://github.com/alexkraak/)| creditline
|[coinflip](steely/plugins/coinflip.py)|[alexkraak](https://github.com/alexkraak/), [byxor](https://github.com/byxor/)| creditline
|[lastfm](steely/plugins/lastfm.py)|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|[vapor](steely/plugins/vapor.py)|[alexkraak](https://github.com/alexkraak/), [sentriz](https://github.com/sentriz/)| creditline
|[b](steely/plugins/b.py)|[byxor](https://github.com/byxor/)| creditline
|[haskell](steely/plugins/haskell.py)|[byxor](https://github.com/byxor/)| creditline
|[limp](steely/plugins/limp.py)|[byxor](https://github.com/byxor/)| creditline
|[responder](steely/plugins/responder.py)|[byxor](https://github.com/byxor/)| creditline
|[url](steely/plugins/url.py)|[byxor](https://github.com/byxor/)| creditline
|[basic_interpreter](steely/plugins/basic_interpreter.py)|[cianlr](https://github.com/cianlr/)| creditline
|[append](steely/plugins/append.py)|[devoxel](https://github.com/devoxel/)| creditline
|[beer](steely/plugins/beer.py)|[devoxel](https://github.com/devoxel/)| creditline
|[bug](steely/plugins/bug.py)|[devoxel](https://github.com/devoxel/)| creditline
|[geoip](steely/plugins/geoip.py)|[devoxel](https://github.com/devoxel/)| creditline
|[help](steely/plugins/help.py)|[devoxel](https://github.com/devoxel/)| creditline
|[roll](steely/plugins/roll.py)|[devoxel](https://github.com/devoxel/)| creditline
|[slag](steely/plugins/slag.py)|[devoxel](https://github.com/devoxel/)| creditline
|[roomcheck](steely/plugins/roomcheck.py)|[gruunday](https://github.com/gruunday/)| creditline
|[egypt](steely/plugins/egypt.py)|[iandioch](https://github.com/iandioch/)| creditline
|[emoji](steely/plugins/emoji.py)|[iandioch](https://github.com/iandioch/)| creditline
|[flip](steely/plugins/flip.py)|[iandioch](https://github.com/iandioch/)| creditline
|[flirty](steely/plugins/flirty.py)|[iandioch](https://github.com/iandioch/)| creditline
|[gex](steely/plugins/gex.py)|[iandioch](https://github.com/iandioch/)| creditline
|[goth](steely/plugins/goth.py)|[iandioch](https://github.com/iandioch/)| creditline
|[mayo](steely/plugins/mayo.py)|[iandioch](https://github.com/iandioch/)| creditline
|[prod](steely/plugins/prod.py)|[iandioch](https://github.com/iandioch/)| creditline
|[rune](steely/plugins/rune.py)|[iandioch](https://github.com/iandioch/)| creditline
|[scramble](steely/plugins/scramble.py)|[iandioch](https://github.com/iandioch/)| creditline
|[shout](steely/plugins/shout.py)|[iandioch](https://github.com/iandioch/)| creditline
|[sort](steely/plugins/sort.py)|[iandioch](https://github.com/iandioch/)| creditline
|[cat](steely/plugins/cat.py)|[itsdoddsy](https://github.com/itsdoddsy/)| creditline
|[choose](steely/plugins/choose.py)|[itsdoddsy](https://github.com/itsdoddsy/)| creditline
|[dog](steely/plugins/dog.py)|[itsdoddsy](https://github.com/itsdoddsy/)| creditline
|[hello](steely/plugins/hello.py)|[izaakf](https://github.com/izaakf/)| creditline
|[train](steely/plugins/train.py)|[izaakf](https://github.com/izaakf/)| creditline
|[vowel](steely/plugins/vowel.py)|[izaakf](https://github.com/izaakf/)| creditline
|[sentiment](steely/plugins/sentiment.py)|[oskarmcd](https://github.com/oskarmcd/)| creditline
|[angry](steely/plugins/angry.py)|[sentriz](https://github.com/sentriz/)| creditline
|[box](steely/plugins/box.py)|[sentriz](https://github.com/sentriz/)| creditline
|[send_to](steely/plugins/send_to.py)|[sentriz](https://github.com/sentriz/)| creditline
|[cage](steely/plugins/cage.py)|[sentriz](https://github.com/sentriz/)| creditline
|[eight](steely/plugins/eight.py)|[sentriz](https://github.com/sentriz/)| creditline
|[leet](steely/plugins/leet.py)|[sentriz](https://github.com/sentriz/)| creditline
|[lenny](steely/plugins/lenny.py)|[sentriz](https://github.com/sentriz/)| creditline
|[markov](steely/plugins/markov.py)|[sentriz](https://github.com/sentriz/)| creditline
|[middle](steely/plugins/middle.py)|[sentriz](https://github.com/sentriz/)| creditline
|[nose](steely/plugins/nose.py)|[sentriz](https://github.com/sentriz/)| creditline
|[paul](steely/plugins/paul.py)|[sentriz](https://github.com/sentriz/)| creditline
|[recordmarkov](steely/plugins/recordmarkov.py)|[sentriz](https://github.com/sentriz/)| creditline
|[recordstat](steely/plugins/recordstat.py)|[sentriz](https://github.com/sentriz/)| creditline
|[reload](steely/plugins/reload.py)|[sentriz](https://github.com/sentriz/)| creditline
|[restart](steely/plugins/restart.py)|[sentriz](https://github.com/sentriz/)| creditline
|[rpn](steely/plugins/rpn.py)|[sentriz](https://github.com/sentriz/)| creditline
|[sheriff](steely/plugins/sheriff.py)|[sentriz](https://github.com/sentriz/)| creditline
|[stats](steely/plugins/stats.py)|[sentriz](https://github.com/sentriz/)| creditline
|[tracker](steely/plugins/tracker.py)|[sentriz](https://github.com/sentriz/)| creditline
|[clap](steely/plugins/clap.py)|[sentriz](https://github.com/sentriz/), [devoxel](https://github.com/devoxel/)| creditline
|[dab](steely/plugins/dab.py)|[xCiaraG](https://github.com/xCiaraG/)| creditline
