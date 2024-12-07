"""
Read a set of FITS files, in the ESPaDOnS spectra format from the CADC
Can be modified for other spectra formats,
if you know the structure of the records in the FITS file.
"""

import numpy as np
import astropy.io.fits as fits
from .. import obsSpec as spf

def espadons(flist, flistout=None, writeSpecHeader=False):
    """
    Convert a list of .fits files in the CADC ESPaDOnS format into
    text .s files. 

    The code provides two files in .s format:  
     
    * The UPENA normalized spectrum (n.s), with automated radial velocity corrections from the telluric lines.
    * The UPENA unnormalized spectrum (u.s), using the automated radial velocity correction from the normalized spectrum.
    This is done starting from the unnormalized spectrum without the automated 
    radial velocity correction, to which we apply the radial velocity
    correction determined from the normalized spectrum. The reason behind this
    is that the UPENA automated radial velocity determination performed on 
    unnormalized spectra does not produce consistently reliable results. 
    The content of the fits header is also saved in a .out text file.
    If flistout=None (default), the files are written at the same path as
    the fits-format data, with the '.fits' stripped, 
    and 'n.s' and 'u.s' appended to the filename root. 
    If flistout is a list of paths ending with a rootname, the files will be
    saved at that path with that rootname, and 'n.s' and 'u.s' appended to
    the filename root.

    :param flist: (list of strings) a list of ESPaDOnS filenames
    :param flistout: (list of strings) optional, list of output file rootnames
    :param writeSpecHeader: Flag for whether to write two lines of header in the
                         .s text file (True = include header)
    """

    if isinstance(flist, str): flist = [flist,]
    #Some basic error checking
    if not isinstance(flist, list):
        raise ValueError('in espadons(), the flist argument must be a Python '
                         'list of input file names (or a single file name)')
    if not (flistout is None):
        if isinstance(flistout, str): flistout = [flistout,]
        if not isinstance(flistout, list):
            raise ValueError('in espadons(), the flistout argument must be a '
                             'Python list of output file names')
        if len(flist) != len(flistout):
            raise ValueError('in espadons(), the list of input file names and '
                             'list of output file names must have the same length')
    
    for i, fname in enumerate(flist):
        print('converting ', fname.strip())
        if flistout is None:
            # striping of white spaces
            fnameOut = fname.strip()
            # removing the '.fits' from the end of the string, 
            # to create the root name for the output files. 
            fnameOut = fnameOut.rstrip('.fits')
        else:
            fnameOut = flistout[i]
        # open the fits file with astropy
        fitsSpec = fits.open(fname.strip())

        header = fitsSpec[0].header

        # Useful for debugging
        #print('File format info')
        #print(fitsSpec.info())
        #print('Header information')
        #print(repr(header))

        # We need to extract the radial velocity correction 
        # that was determined from the normalized spectrum,
        # so that we can apply it to the unnormalized spectrum

        # the radial velocity correction is in the comment section
        # of the header. Using the 'COMMENT' keyword returns a 
        # list of strings
        comments = header['COMMENT']
        # searching for the two strings in the comments that contains
        # the radial velocity correction:
        matches = [match for match in comments if
                   "radial velocity correction from telluric lines" in match]
        # the one calculated for the normalized spectrum is the first instance
        radvel = float(matches[0].split(':')[1])
        
        target = header['OBJECT']
        dateUTC = header['DATE-OB1']
        timeUTC = header['UTIME1']
        # extracting the table of data (24 columns)
        specTab = fitsSpec[0].data

        # The normalized spectrum with radial velocity correction from telluric lines
        # is the first 6 columns
        wln = specTab[0]
        specIn = specTab[1]
        specVn = specTab[2]
        specN1n = specTab[3]
        specN2n = specTab[4]
        specSign = specTab[5]
    
        # The unnormalized spectrum *without* the radial velocity correction
        # from the telluric lines is the last of 4 data blocks
        # (Use this since the radial velocity correction for the unnormalized 
        #  spectrum is unreliable)
        wlu = specTab[18]
        specIu = specTab[19]
        specVu = specTab[20]
        specN1u = specTab[21]
        specN2u = specTab[22]
        specSigu = specTab[23]
    
        fitsSpec.close()

        # Now we apply the velocity correction to the unnormalized data
        c = 299792.458  #speed of light in km/s, since radvel is in km/s
        wlu = wlu + wlu*radvel/c

        spec_n = spf.Spectrum(wln, specIn, specVn, specN1n, specN2n, specSign)
        spec_n.header = '***Reduced spectrum {:} {:} {:}\n'.format(
            target, dateUTC, timeUTC)
        spec_n.save(fnameOut+'n.s', saveHeader=writeSpecHeader)

        spec_u = spf.Spectrum(wlu, specIu, specVu, specN1u, specN2u, specSigu)
        spec_u.header = '***Reduced spectrum {:} {:} {:}\n'.format(
            target, dateUTC, timeUTC)
        spec_u.save(fnameOut+'u.s', saveHeader=writeSpecHeader)
        
        outHeader = open(fnameOut+'.out','w')
        outHeader.write(repr(header))
        outHeader.close()
    return
