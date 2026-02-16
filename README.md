# fr.what

My personal **wh**ealth **a**ssi**t**ant using [Termux](https://termux.dev).

## Install

```bash
curl -s https://raw.githubusercontent.com/gabe-frasz/fr.what/main/install.sh | bash
```

After installation, you MUST enable the crond service and add a cron job:

```bash
sv-enable crond
crontab -e
```

Add the following line to the end of the file:

```
0 18 * * 1-5 python /data/data/com.termux/files/home/fr.what/src/scripts/refresh-assets.py >> /data/data/com.termux/files/home/fr-what.log
```

## TODO

- [ ] Get latest updates from monitored companies (BR)
  - [ ] Scheduled GitHub Action
- [ ] Get latest updates from monitored companies (US)
  - [ ] SEC Edgar RSS feed (https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={TICKER}&type=&dateb=&owner=exclude&start=0&count=40&output=atom)
