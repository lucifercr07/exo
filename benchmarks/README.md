# Benchmarks

```
export AWS_PROFILE=duggup
export AWS_REGION=us-east-1
export AMI_ID=ami-04a81a99f5ec58529
export BENCHMARK_SG=sg-0d2077c321844b74b
export SSH_PEM_PATH=~/.ssh/ghi.pem
export SSH_KEYPAIR_NAME=ghi
export INSTANCE_ID=i-07a3f5fc71bc63046

export SERVICE=d
```

## Running `memtier` benchmark

```
cd benchmarks
bash run_mt1.sh
```

## Benchmarks

Benchmarks are hosted on a Grafana instance, here are the dashboards

- [Redis vs DiceDB Memtier Benchmarks](https://dicedb.grafana.net/public-dashboards/12cb13024353471db6750a53b6242aef)
