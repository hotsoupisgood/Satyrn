# Thebe
![](https://thumbs.gfycat.com/GrossVerifiableAnemone-mobile.mp4)
Thebe's purpose is to allow for the easy running of python scripts that contain graphs. This idea spawned out of the utility which I saw in Jupyter and my desire to run vim as my editor.  
** This program only works with matplotlib graphs.

## Installation
### Dependencies:
Install pandoc:

on Mac via brew:
brew install pandoc

for linux see pandoc.org/installing.html

Install ipykernel:

```
python3 -m pip install ipykernel
python3 -m ipykernel install --user
```
### Install  

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


