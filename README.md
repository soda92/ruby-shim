# ruby-shim

Replace ruby bat with shim on Windows.


## Getting started

Open a PowerShell terminal (version 5.1 or later) and from the PS C:\> prompt, run:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

Then:
```
scoop install python
pip install git+https://github.com/soda92/ruby-shim.git
```

Then:
```
python -m ruby_shim
```
