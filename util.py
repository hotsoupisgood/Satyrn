import importlib
def getHtml(fileName):
    fs=open(fileName, 'r')
    
    newFile=[]
    newBlock=[]
    for line in fs:
        if 'plt.plot' in line:
            newBlock.append(line)
            newFile.append(newBlock)
            
            newBlock=[]
        else:
            newBlock.append(line)
    return newFile
