# PyLet

Install: `pip install .` to install the package.

Usage: 
Check the help message for the command line interface:
```bash
pylet --help
```

Start a pylet cluster:
```bash
# head node
pylet start
```

```bash
# worker node
pylet start --head <head-node-ip>:<port>
```

Submit a job:
```bash
pylet submit python examples/foo.py # this will return a job id
```

Check the status of the job:
```bash
pylet get-result <job-id>
```

TODO:
1. Check cluster status: `pylet status`
2. Shutdown cluster: `pylet shutdown`
3. Get task logs: `pylet logs <job-id>`