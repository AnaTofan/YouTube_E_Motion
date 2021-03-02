from scipy.cluster import  hierarchy
import matplotlib.pyplot as plt
import cluster
videotitles,words,data=cluster.readfile('SolarEnergy.txt')
Z=hierarchy.linkage(data,'single')
plt.figure()
dn=hierarchy.dendrogram(Z,labels=videotitles)
hierarchy.set_link_color_palette(['m','c','y','k'])
fig,axes=plt.subplots(1,2, figsize=(8,3))
dn2=hierarchy.dendrogram(Z,ax=axes[1],above_threshold_color='k',orientation='left',labels=videotitles)
dn1=hierarchy.dendrogram(Z,ax=axes[0],above_threshold_color='m',orientation='top',labels=videotitles)

plt.show()