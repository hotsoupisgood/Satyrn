# Thebe (WIP)
![](https://thumbs.gfycat.com/GrossVerifiableAnemone-size_restricted.gif)  

Thebe is a python command line app. Its purpose is to let you run your code in cells like Jupyter but while using any editor. It does this by watching the cells for changes, and running them if it sees one.

- So far it only is tested to run on Mac and Ubuntu
- It probably has a metric dump truck full of bugs
- And it only works with matplotlib graphs

## Installation
### Dependencies:
#### Install pandoc:

##### on Mac via brew:
```
brew install pandoc
```

for linux see [pandoc.org](https://pandoc.org/installing.html#linux)

#### Install ipykernel:

```
python3 -m pip install ipykernel
python3 -m ipykernel install --user
```
### Install thebe  

Run: 	```pip install thebe``` 

## How to use

Run: 
```
thebe (File you want to run) (Port you want to display on)
```

To utilize cells encapsulate your code blocks in: ```$$$$```.
e.g.:

```
$$$$
from random import random
import numpy as np
import matplotlib.pyplot as plt
print(random())
$$$$
plt.plot(np.sin(np.arange(10)))
print(random())
$$$$
print(random())
$$$$
```
  
In your browser of choice go to ``` localhost:(Port number) ``` to look at your standard outputs, errors, and plots.

This program is still pretty early on so there's likely a lot of bugs.


