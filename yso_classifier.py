from astropy.table import Table,vstack
import numpy as np
import tensorflow as tf
import glob
import os

import argparse

parser = argparse.ArgumentParser(description='Routine for identifying pre-main sequence candidates from optical (BOSS or LAMOST) spectra',formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("tableIn",help="Input table containing outputs from BOSSNet, LineForest, as well as photometry from Gaia and 2MASS")
parser.add_argument("--tableOut",help="Filename of the output table",default='predictions.fits')
parser.add_argument("--logteff",help="Column name containing BOSSNet log Teff",default='logteff')
parser.add_argument("--logg",help="Column name containing BOSSNet logg",default='logg')
parser.add_argument("--g",help="Column name containing Gaia G mag",default='g')
parser.add_argument("--bp",help="Column name containing Gaia BP mag",default='bp')
parser.add_argument("--rp",help="Column name containing Gaia RP mag",default='rp')
parser.add_argument("--j",help="Column name containing 2MASS J mag",default='j')
parser.add_argument("--h",help="Column name containing 2MASS H mag",default='h')
parser.add_argument("--k",help="Column name containing 2MASS K mag",default='k')

#python lineforest.py example/table.fits --instrument LAMOST
#python python getyso.py line_predictions.fits 
def main(args):
    model=tf.keras.models.load_model('models/yso_class.model',compile=False)
    
    t=Table.read(args.tableIn)
    
    keys=[args.logteff,args.logg]
    keys1,keys2=[],[]
    for k in t.keys():
        if ('_eqw' in k) & ('std' not in k): keys1.append(k)
        if ('_abs' in k) & ('std' not in k): keys2.append(k)
    
    
    
    g=np.zeros((len(t),len(keys)+len(keys1)*2+len(keys2)+6),dtype=float)
    for i in range(len(keys)):
        g[:,i]=t[keys[i]]
    
    for i in range(len(keys1)):
        try:
            g[:,3*i+2]=np.log10(np.abs(t[keys1[i]].filled(np.nan)))
        except:
            g[:,3*i+2]=np.log10(np.abs(t[keys1[i]]))
        try:
            g[:,3*i+3]=np.log10(np.abs(t[keys2[i]].filled(np.nan)))
        except:
            g[:,3*i+3]=np.log10(np.abs(t[keys2[i]]))
        a=np.where(g[:,2*i+2]>0)[0]
        g[a,3*i+4]=1
        a=np.where(g[:,2*i+2]<0)[0]
        g[a,3*i+4]=-1
        a=np.where(np.isfinite(g[:,3*i+2])==False)[0]
        g[a,3*i+2]=0
        g[a,3*i+3]=0
        g[a,3*i+4]=0
    
    try:
        g[:,-6]=t[args.g].filled(0)/10-1
    except:
        g[:,-6]=t[args.g]/10-1
    try:
        g[:,-5]=t[args.bp].filled(0)/10-1
    except:
        g[:,-5]=t[args.bp]/10-1
    try:
        g[:,-4]=t[args.rp].filled(0)/10-1
    except:
        g[:,-4]=t[args.rp]/10-1
    try:
        g[:,-3]=t[args.j].filled(0)/10-1
    except:
        g[:,-3]=t[args.j]/10-1
    try:
        g[:,-2]=t[args.h].filled(0)/10-1
    except:
        g[:,-2]=t[args.h]/10-1
    try:
        g[:,-1]=t[args.k].filled(0)/10-1
    except:
        g[:,-1]=t[args.k]/10-1
    
    t['pms_spec'] = model.predict(g,batch_size=10000)
    t.write(args.tableOut,overwrite=True)
    print(t)
    
if __name__ == "__main__":
    args=parser.parse_args()
    main(args)
