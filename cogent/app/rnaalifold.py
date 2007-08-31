#!/usr/bin/env python

from cogent.app.util import CommandLineApplication,\
    CommandLineAppResult, ResultPath
from cogent.app.parameters import Parameter, FlagParameter, ValuedParameter,\
    MixedParameter,Parameters, _find_synonym

__author__ = "Shandy Wikman"
__copyright__ = "Copyright 2007, The Cogent Project"
__contributors__ = ["Shandy Wikman"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Shandy Wikman"
__email__ = "ens01svn@cs.umu.se"
__status__ = "Development"

class RNAalifold(CommandLineApplication):
    """Application controller for RNAalifold application

    reads aligned RNA sequences from stdin or file.aln and calculates
    their minimum free energy (mfe) structure,  partition  function
    (pf)  and  base pairing probability matrix.

OPTIONS
       -cv <float>
              Set  the weight of the covariance term in the energy function to
              factor. Default is 1.


       -nc <float>
              Set the penalty for non-compatible sequences in  the  covariance
              term of the energy function to factor. Default is 1.

       -E     Score pairs with endgaps same as gap-gap pairs.

       -mis   Output \"most informative sequence\" instead of simple consensus:
              For each column of the alignment output the set  of  nucleotides
              with frequence greater than average in IUPAC notation.

       -p     Calculate  the  partition  function and base pairing probability
              matrix in addition to the mfe structure. Default is  calculation
              of mfe structure only.

       -noLP  Avoid  structures without lonely pairs (helices of length 1). In
              the mfe case structures with lonely pairs are  strictly  forbid-
              den.  For  partition  function folding this disallows pairs that
              can only occur isolated.  Setting this option provides a signif-
              icant speedup.

       The -T, -d, -4, -noGU, -noCloseGU, -e, -P, -nsp, options should work as
       in RNAfold

       If using -C constraints will be read from stdin, the alignment  has  to
       given as a filename on the command line.

       For more info see respective man pages. 

    """


    _parameters = {
        '-cv':ValuedParameter(Prefix='-',Name='cv',Delimiter=' '),
        '-nc':ValuedParameter(Prefix='-',Name='nc',Delimiter=' '),
        '-E':FlagParameter(Prefix='-',Name='E'),
        '-mis':FlagParameter(Prefix='-',Name='mis'),
        '-noLP':FlagParameter(Prefix='-',Name='noLP'),
        '-T':ValuedParameter(Prefix='-',Name='T',Value=37,Delimiter=' '),
        '-4':FlagParameter(Prefix='-',Name=4),
        '-d':MixedParameter(Prefix='-',Name='d',Delimiter=''),
        '-noGU':FlagParameter(Prefix='-',Name='noGU'),
        '-noCloseGU':FlagParameter(Prefix='-',Name='noCloseGU'),
        '-e':ValuedParameter(Prefix='-',Name='e',Delimiter=' '),
        '-P':ValuedParameter(Prefix='-',Name='P',Delimiter=' '),
        '-nsp':ValuedParameter(Prefix='-',Name='nsp',Delimiter=' '),
        '-C':FlagParameter(Prefix='-',Name='C')}
    
    _synonyms = {'Temperature':'-T','Temp':'-T','EnergyRange':'-e'}

        
    _command = 'RNAalifold'
    _input_handler = '_input_as_string'
