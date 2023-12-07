# LineForest

Code to derive equivalent widths of youth-sensitive lines in optical (BOSS & LAMOST) spectra

To run:
Download the code and navigate to the folder containing it in the terminal. Then run
```
python lineforest.py example/table.fits --instrument LAMOST
```
```
positional arguments:
  tableIn                  Input table containing paths to individual spectra, and their respective RVs
optional arguments:
  -h, --help               show this help message and exit
  --tableOut TABLEOUT      Filename of the output table
  --path PATH              Column name containing paths
  --rv RV                  Column name containing RV information for each spectrum (in km/s)
  --instrument INSTRUMENT  Name of the spectrograph (BOSS or LAMOST currently supported,
                           others require a different loader)
```
By default produces predictions.fits file as an output.

# YSO classifier

Using outputs from LineForest, produces a probability of classifying a star as pre-main sequence or not.

For BOSSNet outputs, see Sizemore et al. (submitted)

To run:
```
python yso_classifier.py predictions.fits
```
```
positional arguments:
  tableIn              Input table containing outputs from BOSSNet, LineForest,
                       as well as photometry from Gaia and 2MASS

optional arguments:
  -h, --help           show this help message and exit
  --tableOut TABLEOUT  Filename of the output table
  --logteff LOGTEFF    Column name containing BOSSNet log Teff
  --logg LOGG          Column name containing BOSSNet logg
  --g G                Column name containing Gaia G mag
  --bp BP              Column name containing Gaia BP mag
  --rp RP              Column name containing Gaia RP mag
  --j J                Column name containing 2MASS J mag
  --h H                Column name containing 2MASS H mag
  --k K                Column name containing 2MASS K mag
```
