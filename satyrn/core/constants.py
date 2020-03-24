CellDelimiter='####\n'
Cell={'cellCount':'', 'hash':'', 'code':'', 'datetime':'', 'changed': False, 'stdout':'', 'stderr':'', 'image/png':''}
CellDict={'id':[], 'hash':[], 'code':[], 'datetime':[], 'changed': [], 'stdout':[], 'stderr':[], 'image/png':[]}
GetPlot="from binascii import b2a_base64\nimport io\nbuf = io.BytesIO()\nplt.savefig(buf, format = 'png')\nbuf.seek(0)\nprint(b2a_base64(buf.getvalue()).decode())\nplt.close()"
LedgerSkeleton={'ledger':'', 'cells':'', 'global_scope':'', 'local_scope':''}
CellSkeleton={}
DefaultGraph='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Opempqaorq7OH/X19f16fwCAgTDkA/B0dXd3x8KFC6O5uTlqamr69d4rV66Mzs7O/LF3795+vT8AwEAYNtgTeC81NTVRVlYWHR0dvcY7Ojqirq7uhPNfffXVaGtri3nz5uXHcrlcREQMGzYsdu3aFZMnTz6juVRUVERFRcUZXQsAMFQM+SeA5eXlMXPmzGhpacmP5XK5aGlpiTlz5pxw/pQpU2Lnzp3R2tqaP+bPnx/XXntttLa2+rUtAJC8If8EMCJi+fLlsXjx4pg1a1bMnj071qxZE4cPH44lS5ZERMSiRYti/Pjx0dTUFJWVlTF16tRe148aNSoiotf4z372s9izZ0/s27cvIiJ27doVERF1dXUnfbIIAHCuKIoAXLBgQRw4cCBWrVoV7e3tMWPGjNi0aVP+D0P27NkTpaWn9zDz6aefzgdkRMRNN90UERGrV6+Oe+65p9/mDgAw1BTF5wAOVT5HCACKj9fvIngPIAAA/UsAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACRGAAIAJEYAAgAkRgACACSmqAJw7dq1MWHChKisrIyGhobYtm1bn65bv359lJSUxA033NBrPMuyWLVqVYwdOzaGDx8ejY2NsXv37kJMHQBgyCiaANywYUMsX748Vq9eHTt27Ijp06fH3LlzY//+/e96XVtbW9x5551x1VVXnfC1v/iLv4i/+qu/ikceeSReeOGFGDFiRMydOzfeeeedQi0DAGDQFU0Afu1rX4tbb701lixZEpdeemk88sgjcf7558djjz12ymt6enrilltuiXvvvTcmTZrU62tZlsWaNWviC1/4Qlx//fXx27/92/Gtb30r9u3bFxs3biz0cgAABk1RBODRo0dj+/bt0djYmB8rLS2NxsbG2Lp16ymvu++++2LMmDGxbNmyE772+uuvR3t7e697VldXR0NDwynveeTIkejq6up1AAAUm6IIwIMHD0ZPT0/U1tb2Gq+trY329vaTXrNly5ZYt25dNDc3n/Trx687nXs2NTVFdXV1/qivrz/dpQAADLqiCMDT1d3dHQsXLozm5uaoqanpt/uuXLkyOjs788fevXv77d4AAANl2GBPoC9qamqirKwsOjo6eo13dHREXV3dCee/+uqr0dbWFvPmzcuP5XK5iIgYNmxY7Nq1K39dR0dHjB07ttc9Z8yYcdJ5VFRUREVFxVmvBwBgMBXFE8Dy8vKYOXNmtLS05MdyuVy0tLTEnDlzTjh/ypQpsXPnzmhtbc0f8+fPj2uvvTZaW1ujvr4+Jk6cGHV1db3u2dXVFS+88MJJ7wkAcK4oiieAERHLly+PxYsXx6xZs2L27NmxZs2aOHz4cCxZsiQiIhYtWhTjx4+PpqamqKysjKlTp/a6ftSoURERvcbvuOOOuP/+++Piiy+OiRMnxt133x3jxo074fMCAQDOJUUTgAsWLIgDBw7EqlWror29PWbMmBGbNm3K/xHHnj17orT09B5ofu5zn4vDhw/HJz/5yTh06FBceeWVsWnTpqisrCzEEgAAhoSSLMuywZ5Eserq6orq6uro7OyMqqqqwZ4OANAHXr+L5D2AAAD0HwEIAJAYAQgAkBgBCACQGAEIAJAYAQgAkBgBCACQGAEIAJAYAQgAkBgBCACQGAEIAJAYAQgAkBgBCACQGAEIAJAYAQgAkBgBCACQGAEIAJCYYYM9gWKWZVlERHR1dQ3yTACAvjr+un38dTxFAvAsdHd3R0REfX39IM8EADhd3d3dUV1dPdjTGBQlWcr5e5ZyuVzs27cvRo4cGSUlJYM9nbPW1dUV9fX1sXfv3qiqqhrs6QwKe/BL9sEeRNiD4+zDubcHWZZFd3d3jBs3LkpL03w3nCeAZ6G0tDQuuOCCwZ5Gv6uqqjon/gE/G/bgl+yDPYiwB8fZh3NrD1J98ndcmtkLAJAwAQgAkJiye+65557BngRDR1lZWVxzzTUxbFi67w6wB79kH+xBhD04zj7Yg3ONPwIBAEiMXwEDACRGAAIAJEYAAgAkRgACACRGAJ7D1q5dGxMmTIjKyspoaGiIbdu2vev5hw4dittuuy3Gjh0bFRUVcckll8R3vvOdXue8+eab8fGPfzxGjx4dw4cPj2nTpsV//Md/FHIZZ62/92HChAlRUlJywnHbbbcVeilnrL/3oKenJ+6+++6YOHFiDB8+PCZPnhxf/OIXh/R/V7O/96C7uzvuuOOOuOiii2L48OHxoQ99KH70ox8Vehln7XT24Zprrjnpz/pHP/rR/DlZlsWqVati7NixMXz48GhsbIzdu3cPxFLOWH/vwVNPPRXXXXddjB49OkpKSqK1tXUglnHW+nMfjh07FitWrIhp06bFiBEjYty4cbFo0aLYt2/fQC2H05VxTlq/fn1WXl6ePfbYY9l//dd/Zbfeems2atSorKOj46TnHzlyJJs1a1b2B3/wB9mWLVuy119/Pfv3f//3rLW1NX/Oz372s+yiiy7KPvGJT2QvvPBC9tprr2XPPvts9pOf/GSglnXaCrEP+/fvz95666388dxzz2URkX3ve98boFWdnkLswQMPPJCNHj06e+aZZ7LXX389+/a3v529733vyx588MGBWtZpKcQe3Hjjjdmll16aff/73892796drV69Oquqqsr+53/+Z6CWddpOdx9++tOf9vpZf+mll7KysrLs8ccfz5/z5S9/Oauurs42btyY/fjHP87mz5+fTZw4Mfu///u/AVrV6SnEHnzrW9/K7r333qy5uTmLiOzFF18coNWcuf7eh0OHDmWNjY3Zhg0bspdffjnbunVrNnv27GzmzJkDuCpOhwA8R82ePTu77bbb8v+7p6cnGzduXNbU1HTS8x9++OFs0qRJ2dGjR095zxUrVmRXXnllv8+1kAqxD7/uM5/5TDZ58uQsl8ud9XwLoRB78NGPfjRbunRpr7E//MM/zG655Zb+mXQ/6+89ePvtt7OysrLsmWee6TX+wQ9+MPv85z/ffxPvZ6e7D7/u61//ejZy5Mjs5z//eZZlWZbL5bK6urrsq1/9av6cQ4cOZRUVFdnf/d3f9e/k+0l/78Gvev3114smAAu5D8dt27Yti4jsjTfeOOv50v/8CvgcdPTo0di+fXs0Njbmx0pLS6OxsTG2bt160muefvrpmDNnTtx2221RW1sbU6dOjS996UvR09PT65xZs2bFxz72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'

EmptyGraph='iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAPYQAAD2EBqD+naQAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDMuMC4zLCBodHRwOi8vbWF0cGxvdGxpYi5vcmcvnQurowAACMlJREFUeJzt1jEBACAMwDDAv+fhAo4mCnp2z8wsAAAyzu8AAADeMoAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiDCAAQIwBBACIMYAAADEGEAAgxgACAMQYQACAGAMIABBjAAEAYgwgAECMAQQAiDGAAAAxBhAAIMYAAgDEGEAAgBgDCAAQYwABAGIMIABAjAEEAIgxgAAAMQYQACDGAAIAxBhAAIAYAwgAEGMAAQBiLiZ5B7ynp7JiAAAAAElFTkSuQmCC'
