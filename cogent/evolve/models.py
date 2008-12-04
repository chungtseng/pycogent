#! /usr/bin/env python
"""A collection of pre-defined models.  These are provided for convenience so that
users do not need to keep reconstructing the standard models.  We encorage users
to think about the assumptions in these models and consider if their problem could
benefit from a user defined model.
Note that models that do not traditionally deal with gaps are implemented with
gap recoding that will convert gaps to Ns, and model gaps set to False."""
#The models are constructed in a strait forward manner with no attempt to condense
#this file using functions etc. to allow each model to serve as an example for users
#wishing to construct their own models

import numpy
from cogent.evolve import substitution_model, predicate

__author__ = "Matthew Wakefield"
__copyright__ = "Copyright 2007-2008, The Cogent Project"
__credits__ = ["Matthew Wakefield", "Peter Maxwell", "Gavin Huttley"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Matthew Wakefield"
__email__ = "matthew.wakefield@wehi.edu.au"
__status__ = "Production"

nucleotide_models = ['JC69','F81','HKY85', 'GTR']

codon_models = ['GY94', 'H04G', 'H04GK', 'H04GGK']

protein_models = [ 'DSO78', 'AH96', 'AH96_mtmammals', 'JTT92', 'WG01']

# Nucleotide Models
def JC69():
    """Jukes and Cantor's 1969 model"""
    return substitution_model.Nucleotide(
            equal_motif_probs = True,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'JC69'
            )
    

def F81():
    """Felsenstein's 1981 model"""
    return substitution_model.Nucleotide(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'F81',
            )
    

def HKY85():
    """Hasegawa, Kishino and Yanamo 1985 model"""
    return substitution_model.Nucleotide(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'HKY85',
            predicates = {
                'kappa' : 'transition',
                },
            )
    

def GTR():
    """General Time Reversible nucleotide substitution model."""
    MotifChange = predicate.MotifChange
    preds = [MotifChange(x,y) for x,y in ['AC', 'AG', 'AT', 'CG', 'CT']]
    return substitution_model.Nucleotide(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'GTR',
            predicates = preds
            )
    

# Codon Models
def GY94():
    """Goldman and Yang 1994 codon substitution model.
    
    see, N Goldman and Z Yang, Mol. Biol. Evol., 11(5):725-36, 1994."""
    return Y98()
    

def Y98():
    """Yang's 1998 substitution model, a derivative of the GY94.
    see Z Yang. Mol. Biol. Evol., 15(5):568-73, 1998"""
    return substitution_model.Codon(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'Y98',
            predicates = {
                'kappa' : 'transition',
                'omega' : 'replacement',
                },
            )
    

def H04G():
    """Huttley 2004 CpG substitution model. Includes a term for substitutions
    to or from CpG's.
    
    see, GA Huttley. Mol Biol Evol, 21(9):1760-8"""
    cg = predicate.MotifChange('CG').aliased('G')
    kappa = (~predicate.MotifChange('R','Y')).aliased('kappa')
    omega = predicate.replacement.aliased('omega')
    return substitution_model.Codon(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'H04G',
            predicates = [cg, kappa, omega],
            )
    

def H04GK():
    """Huttley 2004 CpG substitution model. Includes a term for transition
    substitutions to or from CpG's.
    
    see, GA Huttley. Mol Biol Evol, 21(9):1760-8"""
    cg = predicate.MotifChange('CG').aliased('G')
    kappa = (~predicate.MotifChange('R','Y')).aliased('K')
    cg_k = (cg & kappa).aliased('G.K')
    omega = predicate.replacement.aliased('omega')
    return substitution_model.Codon(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'H04GK',
            predicates = [cg_k, kappa, omega],
            )
    

def H04GGK():
    """Huttley 2004 CpG substitution model. Includes a general term for
    substitutions to or from CpG's and an adjustment for CpG transitions.
    
    see, GA Huttley. Mol Biol Evol, 21(9):1760-8"""
    cg = predicate.MotifChange('CG').aliased('G')
    kappa = (~predicate.MotifChange('R','Y')).aliased('K')
    cg_k = (cg & kappa).aliased('G.K')
    omega = predicate.replacement.aliased('omega')
    return substitution_model.Codon(
            motif_probs = None,
            do_scaling = True,
            model_gaps = False,
            recode_gaps = True,
            name = 'H04GGK',
            predicates = [cg, cg_k, kappa, omega],
            )
    

# Protein Models

# Empirical Protein Models

DSO78_matrix = numpy.array(
    [[  0.00000000e+00,   3.60000000e+01,   1.20000000e+02,   1.98000000e+02,
        1.80000000e+01,   2.40000000e+02,   2.30000000e+01,   6.50000000e+01,
        2.60000000e+01,   4.10000000e+01,   7.20000000e+01,   9.80000000e+01,
        2.50000000e+02,   8.90000000e+01,   2.70000000e+01,   4.09000000e+02,
        3.71000000e+02,   2.08000000e+02,   0.00000000e+00,   2.40000000e+01],
       [  3.60000000e+01,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
        0.00000000e+00,   1.10000000e+01,   2.80000000e+01,   4.40000000e+01,
        0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
        1.90000000e+01,   0.00000000e+00,   2.30000000e+01,   1.61000000e+02,
        1.60000000e+01,   4.90000000e+01,   0.00000000e+00,   9.60000000e+01],
       [  1.20000000e+02,   0.00000000e+00,   0.00000000e+00,   1.15300000e+03,
        0.00000000e+00,   1.25000000e+02,   8.60000000e+01,   2.40000000e+01,
        7.10000000e+01,   0.00000000e+00,   0.00000000e+00,   9.05000000e+02,
        1.30000000e+01,   1.34000000e+02,   0.00000000e+00,   9.50000000e+01,
        6.60000000e+01,   1.80000000e+01,   0.00000000e+00,   0.00000000e+00],
       [  1.98000000e+02,   0.00000000e+00,   1.15300000e+03,   0.00000000e+00,
        0.00000000e+00,   8.10000000e+01,   4.30000000e+01,   6.10000000e+01,
        8.30000000e+01,   1.10000000e+01,   3.00000000e+01,   1.48000000e+02,
        5.10000000e+01,   7.16000000e+02,   1.00000000e+00,   7.90000000e+01,
        3.40000000e+01,   3.70000000e+01,   0.00000000e+00,   2.20000000e+01],
       [  1.80000000e+01,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
        0.00000000e+00,   1.50000000e+01,   4.80000000e+01,   1.96000000e+02,
        0.00000000e+00,   1.57000000e+02,   9.20000000e+01,   1.40000000e+01,
        1.10000000e+01,   0.00000000e+00,   1.40000000e+01,   4.60000000e+01,
        1.30000000e+01,   1.20000000e+01,   7.60000000e+01,   6.98000000e+02],
       [  2.40000000e+02,   1.10000000e+01,   1.25000000e+02,   8.10000000e+01,
        1.50000000e+01,   0.00000000e+00,   1.00000000e+01,   0.00000000e+00,
        2.70000000e+01,   7.00000000e+00,   1.70000000e+01,   1.39000000e+02,
        3.40000000e+01,   2.80000000e+01,   9.00000000e+00,   2.34000000e+02,
        3.00000000e+01,   5.40000000e+01,   0.00000000e+00,   0.00000000e+00],
       [  2.30000000e+01,   2.80000000e+01,   8.60000000e+01,   4.30000000e+01,
        4.80000000e+01,   1.00000000e+01,   0.00000000e+00,   7.00000000e+00,
        2.60000000e+01,   4.40000000e+01,   0.00000000e+00,   5.35000000e+02,
        9.40000000e+01,   6.06000000e+02,   2.40000000e+02,   3.50000000e+01,
        2.20000000e+01,   4.40000000e+01,   2.70000000e+01,   1.27000000e+02],
       [  6.50000000e+01,   4.40000000e+01,   2.40000000e+01,   6.10000000e+01,
        1.96000000e+02,   0.00000000e+00,   7.00000000e+00,   0.00000000e+00,
        4.60000000e+01,   2.57000000e+02,   3.36000000e+02,   7.70000000e+01,
        1.20000000e+01,   1.80000000e+01,   6.40000000e+01,   2.40000000e+01,
        1.92000000e+02,   8.89000000e+02,   0.00000000e+00,   3.70000000e+01],
       [  2.60000000e+01,   0.00000000e+00,   7.10000000e+01,   8.30000000e+01,
        0.00000000e+00,   2.70000000e+01,   2.60000000e+01,   4.60000000e+01,
        0.00000000e+00,   1.80000000e+01,   2.43000000e+02,   3.18000000e+02,
        3.30000000e+01,   1.53000000e+02,   4.64000000e+02,   9.60000000e+01,
        1.36000000e+02,   1.00000000e+01,   0.00000000e+00,   1.30000000e+01],
       [  4.10000000e+01,   0.00000000e+00,   0.00000000e+00,   1.10000000e+01,
        1.57000000e+02,   7.00000000e+00,   4.40000000e+01,   2.57000000e+02,
        1.80000000e+01,   0.00000000e+00,   5.27000000e+02,   3.40000000e+01,
        3.20000000e+01,   7.30000000e+01,   1.50000000e+01,   1.70000000e+01,
        3.30000000e+01,   1.75000000e+02,   4.60000000e+01,   2.80000000e+01],
       [  7.20000000e+01,   0.00000000e+00,   0.00000000e+00,   3.00000000e+01,
        9.20000000e+01,   1.70000000e+01,   0.00000000e+00,   3.36000000e+02,
        2.43000000e+02,   5.27000000e+02,   0.00000000e+00,   1.00000000e+00,
        1.70000000e+01,   1.14000000e+02,   9.00000000e+01,   6.20000000e+01,
        1.04000000e+02,   2.58000000e+02,   0.00000000e+00,   0.00000000e+00],
       [  9.80000000e+01,   0.00000000e+00,   9.05000000e+02,   1.48000000e+02,
        1.40000000e+01,   1.39000000e+02,   5.35000000e+02,   7.70000000e+01,
        3.18000000e+02,   3.40000000e+01,   1.00000000e+00,   0.00000000e+00,
        4.20000000e+01,   1.03000000e+02,   3.20000000e+01,   4.95000000e+02,
        2.29000000e+02,   1.50000000e+01,   2.30000000e+01,   9.50000000e+01],
       [  2.50000000e+02,   1.90000000e+01,   1.30000000e+01,   5.10000000e+01,
        1.10000000e+01,   3.40000000e+01,   9.40000000e+01,   1.20000000e+01,
        3.30000000e+01,   3.20000000e+01,   1.70000000e+01,   4.20000000e+01,
        0.00000000e+00,   1.53000000e+02,   1.03000000e+02,   2.45000000e+02,
        7.80000000e+01,   4.80000000e+01,   0.00000000e+00,   0.00000000e+00],
       [  8.90000000e+01,   0.00000000e+00,   1.34000000e+02,   7.16000000e+02,
        0.00000000e+00,   2.80000000e+01,   6.06000000e+02,   1.80000000e+01,
        1.53000000e+02,   7.30000000e+01,   1.14000000e+02,   1.03000000e+02,
        1.53000000e+02,   0.00000000e+00,   2.46000000e+02,   5.60000000e+01,
        5.30000000e+01,   3.50000000e+01,   0.00000000e+00,   0.00000000e+00],
       [  2.70000000e+01,   2.30000000e+01,   0.00000000e+00,   1.00000000e+00,
        1.40000000e+01,   9.00000000e+00,   2.40000000e+02,   6.40000000e+01,
        4.64000000e+02,   1.50000000e+01,   9.00000000e+01,   3.20000000e+01,
        1.03000000e+02,   2.46000000e+02,   0.00000000e+00,   1.54000000e+02,
        2.60000000e+01,   2.40000000e+01,   2.01000000e+02,   8.00000000e+00],
       [  4.09000000e+02,   1.61000000e+02,   9.50000000e+01,   7.90000000e+01,
        4.60000000e+01,   2.34000000e+02,   3.50000000e+01,   2.40000000e+01,
        9.60000000e+01,   1.70000000e+01,   6.20000000e+01,   4.95000000e+02,
        2.45000000e+02,   5.60000000e+01,   1.54000000e+02,   0.00000000e+00,
        5.50000000e+02,   3.00000000e+01,   7.50000000e+01,   3.40000000e+01],
       [  3.71000000e+02,   1.60000000e+01,   6.60000000e+01,   3.40000000e+01,
        1.30000000e+01,   3.00000000e+01,   2.20000000e+01,   1.92000000e+02,
        1.36000000e+02,   3.30000000e+01,   1.04000000e+02,   2.29000000e+02,
        7.80000000e+01,   5.30000000e+01,   2.60000000e+01,   5.50000000e+02,
        0.00000000e+00,   1.57000000e+02,   0.00000000e+00,   4.20000000e+01],
       [  2.08000000e+02,   4.90000000e+01,   1.80000000e+01,   3.70000000e+01,
        1.20000000e+01,   5.40000000e+01,   4.40000000e+01,   8.89000000e+02,
        1.00000000e+01,   1.75000000e+02,   2.58000000e+02,   1.50000000e+01,
        4.80000000e+01,   3.50000000e+01,   2.40000000e+01,   3.00000000e+01,
        1.57000000e+02,   0.00000000e+00,   0.00000000e+00,   2.80000000e+01],
       [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
        7.60000000e+01,   0.00000000e+00,   2.70000000e+01,   0.00000000e+00,
        0.00000000e+00,   4.60000000e+01,   0.00000000e+00,   2.30000000e+01,
        0.00000000e+00,   0.00000000e+00,   2.01000000e+02,   7.50000000e+01,
        0.00000000e+00,   0.00000000e+00,   0.00000000e+00,   6.10000000e+01],
       [  2.40000000e+01,   9.60000000e+01,   0.00000000e+00,   2.20000000e+01,
        6.98000000e+02,   0.00000000e+00,   1.27000000e+02,   3.70000000e+01,
        1.30000000e+01,   2.80000000e+01,   0.00000000e+00,   9.50000000e+01,
        0.00000000e+00,   0.00000000e+00,   8.00000000e+00,   3.40000000e+01,
        4.20000000e+01,   2.80000000e+01,   6.10000000e+01,   0.00000000e+00]])

DSO78_freqs = {'A': 0.087126912873087131, 'C': 0.033473966526033475,
         'E': 0.04952995047004953, 'D': 0.046871953128046873,
         'G': 0.088611911388088618, 'F': 0.039771960228039777,
         'I': 0.036885963114036892, 'H': 0.033617966382033626,
         'K': 0.08048191951808048, 'M': 0.014752985247014754,
         'L': 0.085356914643085369, 'N': 0.040431959568040438,
         'Q': 0.038254961745038257, 'P': 0.050679949320050689,
         'S': 0.069576930423069588, 'R': 0.040903959096040908,
         'T': 0.058541941458058543, 'W': 0.010493989506010494,
         'V': 0.064717935282064723, 'Y': 0.029915970084029919}

JTT92_matrix = numpy.array(
        [[   0., 56., 81.,  105., 15.,  179., 27., 36., 35., 30., 54.,
               54.,  194., 57., 58.,  378.,  475.,  298.,  9., 11.],
       [  56.,  0., 10.,  5., 78., 59., 69., 17.,  7., 23., 31.,
               34., 14.,  9.,  113.,  223., 42., 62.,  115.,  209.],
       [  81., 10.,  0.,  767.,  4.,  130.,  112., 11., 26.,  7., 15.,
              528., 15., 49., 16., 59., 38., 31.,  4., 46.],
       [ 105.,  5.,  767.,  0.,  5.,  119., 26., 12.,  181.,  9., 18.,
               58., 18.,  323., 29., 30., 32., 45., 10.,  7.],
       [  15., 78.,  4.,  5.,  0.,  5., 40., 89.,  4.,  248., 43.,
               10., 17.,  4.,  5., 92., 12., 62., 53.,  536.],
       [ 179., 59.,  130.,  119.,  5.,  0., 23.,  6., 27.,  6., 14.,
               81., 24., 26.,  137.,  201., 33., 47., 55.,  8.],
       [  27., 69.,  112., 26., 40., 23.,  0., 16., 45., 56., 33.,
              391.,  115.,  597.,  328., 73., 46., 11.,  8.,  573.],
       [  36., 17., 11., 12., 89.,  6., 16.,  0., 21.,  229.,  479.,
               47., 10.,  9., 22., 40.,  245.,  961.,  9., 32.],
       [  35.,  7., 26.,  181.,  4., 27., 45., 21.,  0., 14., 65.,
              263., 21.,  292.,  646., 47.,  103., 14., 10.,  8.],
       [  30., 23.,  7.,  9.,  248.,  6., 56.,  229., 14.,  0.,  388.,
               12.,  102., 72., 38., 59., 25.,  180., 52., 24.],
       [  54., 31., 15., 18., 43., 14., 33.,  479., 65.,  388.,  0.,
               30., 16., 43., 44., 29.,  226.,  323., 24., 18.],
       [  54., 34.,  528., 58., 10., 81.,  391., 47.,  263., 12., 30.,
                0., 15., 86., 45.,  503.,  232., 16.,  8., 70.],
       [ 194., 14., 15., 18., 17., 24.,  115., 10., 21.,  102., 16.,
               15.,  0.,  164., 74.,  285.,  118., 23.,  6., 10.],
       [  57.,  9., 49.,  323.,  4., 26.,  597.,  9.,  292., 72., 43.,
               86.,  164.,  0.,  310., 53., 51., 20., 18., 24.],
       [  58.,  113., 16., 29.,  5.,  137.,  328., 22.,  646., 38., 44.,
               45., 74.,  310.,  0.,  101., 64., 17.,  126., 20.],
       [ 378.,  223., 59., 30., 92.,  201., 73., 40., 47., 59., 29.,
              503.,  285., 53.,  101.,  0.,  477., 38., 35., 63.],
       [ 475., 42., 38., 32., 12., 33., 46.,  245.,  103., 25.,  226.,
              232.,  118., 51., 64.,  477.,  0.,  112., 12., 21.],
       [ 298., 62., 31., 45., 62., 47., 11.,  961., 14.,  180.,  323.,
               16., 23., 20., 17., 38.,  112.,  0., 25., 16.],
       [   9.,  115.,  4., 10., 53., 55.,  8.,  9., 10., 52., 24.,
                8.,  6., 18.,  126., 35., 12., 25.,  0., 71.],
       [  11.,  209., 46.,  7.,  536.,  8.,  573., 32.,  8., 24., 18.,
               70., 10., 24., 20., 63., 21., 16., 71.,  0.]])

JTT92_freqs = {'A': 0.076747923252076758, 'C': 0.019802980197019805, 'E': 0.061829938170061841, 'D': 0.05154394845605155, 'G': 0.073151926848073159, 'F': 0.040125959874040135, 'I': 0.053760946239053767, 'H': 0.022943977056022944, 'K': 0.058675941324058678, 'M': 0.023825976174023829, 'L': 0.091903908096091905, 'N': 0.042644957355042652, 'Q': 0.040751959248040752, 'P': 0.050900949099050907, 'S': 0.068764931235068771, 'R': 0.051690948309051694, 'T': 0.058564941435058568, 'W': 0.014260985739014262, 'V': 0.066004933995066004, 'Y': 0.032101967898032102}

AH96_matrix = numpy.array(
        [[    0.  , 59.93, 17.67,  9.77,  6.37, 120.71, 13.9 ,
                96.49,  8.36, 25.46, 141.88, 26.95, 54.31,  1.9 ,
                23.18, 387.86, 480.72, 195.06,  1.9 ,  6.48],
       [   59.93,  0.  ,  1.9 ,  1.9 , 70.8 , 30.71, 141.49,
                62.73,  1.9 , 25.65,  6.18, 58.94, 31.26, 75.24,
               103.33, 277.05, 179.97,  1.9 , 33.6 , 254.77],
       [   17.67,  1.9 ,  0.  , 583.55,  4.98, 56.77, 113.99,
                 4.34,  2.31,  1.9 ,  1.9 , 794.38, 13.43, 55.28,
                 1.9 , 69.02, 28.01,  1.9 , 19.86, 21.21],
       [    9.77,  1.9 , 583.55,  0.  ,  2.67, 28.28, 49.12,
                 3.31, 313.86,  1.9 ,  1.9 , 63.05, 12.83, 313.56,
                 1.9 , 54.71, 14.82, 21.14,  1.9 , 13.12],
       [    6.37, 70.8 ,  4.98,  2.67,  0.  ,  1.9 , 48.16,
                84.67,  6.44, 216.06, 90.82, 15.2 , 17.31, 19.11,
                 4.69, 64.29, 33.85,  6.35,  7.84, 465.58],
       [  120.71, 30.71, 56.77, 28.28,  1.9 ,  0.  ,  1.9 ,
                 5.98, 22.73,  2.41,  1.9 , 53.3 ,  1.9 ,  6.75,
                23.03, 125.93, 11.17,  2.53, 10.92,  3.21],
       [   13.9 , 141.49, 113.99, 49.12, 48.16,  1.9 ,  0.  ,
                12.26, 127.67, 11.49, 11.97, 496.13, 60.97, 582.4 ,
               165.23, 77.46, 44.78,  1.9 ,  7.08, 670.14],
       [   96.49, 62.73,  4.34,  3.31, 84.67,  5.98, 12.26,
                 0.  , 19.57, 329.09, 517.98, 27.1 , 20.63,  8.34,
                 1.9 , 47.7 , 368.43, 1222.94,  1.9 , 25.01],
       [    8.36,  1.9 ,  2.31, 313.86,  6.44, 22.73, 127.67,
                19.57,  0.  , 14.88, 91.37, 608.7 , 50.1 , 465.58,
               141.4 , 105.79, 136.33,  1.9 , 24.  , 51.17],
       [   25.46, 25.65,  1.9 ,  1.9 , 216.06,  2.41, 11.49,
               329.09, 14.88,  0.  , 537.53, 15.16, 40.1 , 39.7 ,
                15.58, 73.61, 126.4 , 91.67, 32.44, 44.15],
       [  141.88,  6.18,  1.9 ,  1.9 , 90.82,  1.9 , 11.97,
               517.98, 91.37, 537.53,  0.  , 65.41, 18.84, 47.37,
                 1.9 , 111.16, 528.17, 387.54, 21.71, 39.96],
       [   26.95, 58.94, 794.38, 63.05, 15.2 , 53.3 , 496.13,
                27.1 , 608.7 , 15.16, 65.41,  0.  , 73.31, 173.56,
                13.24, 494.39, 238.46,  1.9 , 10.68, 191.36],
       [   54.31, 31.26, 13.43, 12.83, 17.31,  1.9 , 60.97,
                20.63, 50.1 , 40.1 , 18.84, 73.31,  0.  , 137.29,
                23.64, 169.9 , 128.22,  8.23,  4.21, 16.21],
       [    1.9 , 75.24, 55.28, 313.56, 19.11,  6.75, 582.4 ,
                 8.34, 465.58, 39.7 , 47.37, 173.56, 137.29,  0.  ,
               220.99, 54.11, 94.93, 19.  ,  1.9 , 38.82],
       [   23.18, 103.33,  1.9 ,  1.9 ,  4.69, 23.03, 165.23,
                 1.9 , 141.4 , 15.58,  1.9 , 13.24, 23.64, 220.99,
                 0.  ,  6.04,  2.08,  7.64, 21.95,  1.9 ],
       [  387.86, 277.05, 69.02, 54.71, 64.29, 125.93, 77.46,
                47.7 , 105.79, 73.61, 111.16, 494.39, 169.9 , 54.11,
                 6.04,  0.  , 597.21,  1.9 , 38.58, 64.92],
       [  480.72, 179.97, 28.01, 14.82, 33.85, 11.17, 44.78,
               368.43, 136.33, 126.4 , 528.17, 238.46, 128.22, 94.93,
                 2.08, 597.21,  0.  , 204.54,  9.99, 38.73],
       [  195.06,  1.9 ,  1.9 , 21.14,  6.35,  2.53,  1.9 ,
              1222.94,  1.9 , 91.67, 387.54,  1.9 ,  8.23, 19.  ,
                 7.64,  1.9 , 204.54,  0.  ,  5.37,  1.9 ],
       [    1.9 , 33.6 , 19.86,  1.9 ,  7.84, 10.92,  7.08,
                 1.9 , 24.  , 32.44, 21.71, 10.68,  4.21,  1.9 ,
                21.95, 38.58,  9.99,  5.37,  0.  , 26.25],
       [    6.48, 254.77, 21.21, 13.12, 465.58,  3.21, 670.14,
                25.01, 51.17, 44.15, 39.96, 191.36, 16.21, 38.82,
                 1.9 , 64.92, 38.73,  1.9 , 26.25,  0.  ]])

AH96_freqs = {
            'A': 0.071999999999999995, 'C': 0.0060000000000000001, 'E': 0.024, 'D': 0.019, 'G': 0.056000000000000001, 'F': 0.060999999999999999, 'I': 0.087999999999999995, 'H': 0.028000000000000001, 'K': 0.023, 'M': 0.053999999999999999, 'L': 0.16900000000000001, 'N': 0.039, 'Q': 0.025000000000000001, 'P': 0.053999999999999999, 'S': 0.071999999999999995, 'R': 0.019, 'T': 0.085999999999999993, 'W': 0.029000000000000001, 'V': 0.042999999999999997, 'Y': 0.033000000000000002}

AH96_mtmammals_matrix = numpy.array(
        [[ 0.00000000e+00, 0.00000000e+00, 1.10000000e+01, 0.00000000e+00,
               0.00000000e+00, 7.80000000e+01, 8.00000000e+00, 7.50000000e+01,
               0.00000000e+00, 2.10000000e+01, 7.60000000e+01, 2.00000000e+00,
               5.30000000e+01, 0.00000000e+00, 3.20000000e+01, 3.42000000e+02,
               6.81000000e+02, 3.98000000e+02, 5.00000000e+00, 0.00000000e+00],
       [  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               7.00000000e+00, 0.00000000e+00, 3.05000000e+02, 4.10000000e+01,
               0.00000000e+00, 2.70000000e+01, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 1.86000000e+02, 3.47000000e+02,
               1.14000000e+02, 0.00000000e+00, 6.50000000e+01, 5.30000000e+02],
       [  1.10000000e+01, 0.00000000e+00, 0.00000000e+00, 5.69000000e+02,
               5.00000000e+00, 7.90000000e+01, 1.10000000e+01, 0.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 8.64000000e+02,
               2.00000000e+00, 4.90000000e+01, 0.00000000e+00, 1.60000000e+01,
               0.00000000e+00, 1.00000000e+01, 0.00000000e+00, 0.00000000e+00],
       [  0.00000000e+00, 0.00000000e+00, 5.69000000e+02, 0.00000000e+00,
               0.00000000e+00, 2.20000000e+01, 2.20000000e+01, 0.00000000e+00,
               2.15000000e+02, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 2.74000000e+02, 0.00000000e+00, 2.10000000e+01,
               4.00000000e+00, 2.00000000e+01, 0.00000000e+00, 0.00000000e+00],
       [  0.00000000e+00, 7.00000000e+00, 5.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 5.70000000e+01,
               0.00000000e+00, 2.46000000e+02, 1.10000000e+01, 6.00000000e+00,
               1.70000000e+01, 0.00000000e+00, 0.00000000e+00, 9.00000000e+01,
               8.00000000e+00, 6.00000000e+00, 0.00000000e+00, 6.82000000e+02],
       [  7.80000000e+01, 0.00000000e+00, 7.90000000e+01, 2.20000000e+01,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.70000000e+01,
               0.00000000e+00, 0.00000000e+00, 1.80000000e+01, 1.12000000e+02,
               0.00000000e+00, 5.00000000e+00, 0.00000000e+00, 1.00000000e+00],
       [  8.00000000e+00, 3.05000000e+02, 1.10000000e+01, 2.20000000e+01,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 2.60000000e+01, 0.00000000e+00, 4.58000000e+02,
               5.30000000e+01, 5.50000000e+02, 2.32000000e+02, 2.00000000e+01,
               1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.52500000e+03],
       [  7.50000000e+01, 4.10000000e+01, 0.00000000e+00, 0.00000000e+00,
               5.70000000e+01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               6.00000000e+00, 2.32000000e+02, 3.78000000e+02, 1.90000000e+01,
               5.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               3.60000000e+02, 2.22000000e+03, 0.00000000e+00, 1.60000000e+01],
       [  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 2.15000000e+02,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 6.00000000e+00,
               0.00000000e+00, 4.00000000e+00, 5.90000000e+01, 4.08000000e+02,
               1.80000000e+01, 2.42000000e+02, 5.00000000e+01, 6.50000000e+01,
               5.00000000e+01, 0.00000000e+00, 0.00000000e+00, 6.70000000e+01],
       [  2.10000000e+01, 2.70000000e+01, 0.00000000e+00, 0.00000000e+00,
               2.46000000e+02, 0.00000000e+00, 2.60000000e+01, 2.32000000e+02,
               4.00000000e+00, 0.00000000e+00, 6.09000000e+02, 0.00000000e+00,
               4.30000000e+01, 2.00000000e+01, 6.00000000e+00, 7.40000000e+01,
               3.40000000e+01, 1.00000000e+02, 1.20000000e+01, 2.50000000e+01],
       [  7.60000000e+01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               1.10000000e+01, 0.00000000e+00, 0.00000000e+00, 3.78000000e+02,
               5.90000000e+01, 6.09000000e+02, 0.00000000e+00, 2.10000000e+01,
               0.00000000e+00, 2.20000000e+01, 0.00000000e+00, 4.70000000e+01,
               6.91000000e+02, 8.32000000e+02, 1.30000000e+01, 0.00000000e+00],
       [  2.00000000e+00, 0.00000000e+00, 8.64000000e+02, 0.00000000e+00,
               6.00000000e+00, 4.70000000e+01, 4.58000000e+02, 1.90000000e+01,
               4.08000000e+02, 0.00000000e+00, 2.10000000e+01, 0.00000000e+00,
               3.30000000e+01, 8.00000000e+00, 4.00000000e+00, 4.46000000e+02,
               1.10000000e+02, 0.00000000e+00, 6.00000000e+00, 1.56000000e+02],
       [  5.30000000e+01, 0.00000000e+00, 2.00000000e+00, 0.00000000e+00,
               1.70000000e+01, 0.00000000e+00, 5.30000000e+01, 5.00000000e+00,
               1.80000000e+01, 4.30000000e+01, 0.00000000e+00, 3.30000000e+01,
               0.00000000e+00, 5.10000000e+01, 9.00000000e+00, 2.02000000e+02,
               7.80000000e+01, 0.00000000e+00, 7.00000000e+00, 8.00000000e+00],
       [  0.00000000e+00, 0.00000000e+00, 4.90000000e+01, 2.74000000e+02,
               0.00000000e+00, 0.00000000e+00, 5.50000000e+02, 0.00000000e+00,
               2.42000000e+02, 2.00000000e+01, 2.20000000e+01, 8.00000000e+00,
               5.10000000e+01, 0.00000000e+00, 2.46000000e+02, 3.00000000e+01,
               0.00000000e+00, 3.30000000e+01, 0.00000000e+00, 5.40000000e+01],
       [  3.20000000e+01, 1.86000000e+02, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 1.80000000e+01, 2.32000000e+02, 0.00000000e+00,
               5.00000000e+01, 6.00000000e+00, 0.00000000e+00, 4.00000000e+00,
               9.00000000e+00, 2.46000000e+02, 0.00000000e+00, 3.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 1.60000000e+01, 0.00000000e+00],
       [  3.42000000e+02, 3.47000000e+02, 1.60000000e+01, 2.10000000e+01,
               9.00000000e+01, 1.12000000e+02, 2.00000000e+01, 0.00000000e+00,
               6.50000000e+01, 7.40000000e+01, 4.70000000e+01, 4.46000000e+02,
               2.02000000e+02, 3.00000000e+01, 3.00000000e+00, 0.00000000e+00,
               6.14000000e+02, 0.00000000e+00, 1.70000000e+01, 1.07000000e+02],
       [  6.81000000e+02, 1.14000000e+02, 0.00000000e+00, 4.00000000e+00,
               8.00000000e+00, 0.00000000e+00, 1.00000000e+00, 3.60000000e+02,
               5.00000000e+01, 3.40000000e+01, 6.91000000e+02, 1.10000000e+02,
               7.80000000e+01, 0.00000000e+00, 0.00000000e+00, 6.14000000e+02,
               0.00000000e+00, 2.37000000e+02, 0.00000000e+00, 0.00000000e+00],
       [  3.98000000e+02, 0.00000000e+00, 1.00000000e+01, 2.00000000e+01,
               6.00000000e+00, 5.00000000e+00, 0.00000000e+00, 2.22000000e+03,
               0.00000000e+00, 1.00000000e+02, 8.32000000e+02, 0.00000000e+00,
               0.00000000e+00, 3.30000000e+01, 0.00000000e+00, 0.00000000e+00,
               2.37000000e+02, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
       [  5.00000000e+00, 6.50000000e+01, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 1.20000000e+01, 1.30000000e+01, 6.00000000e+00,
               7.00000000e+00, 0.00000000e+00, 1.60000000e+01, 1.70000000e+01,
               0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.40000000e+01],
       [  0.00000000e+00, 5.30000000e+02, 0.00000000e+00, 0.00000000e+00,
               6.82000000e+02, 1.00000000e+00, 1.52500000e+03, 1.60000000e+01,
               6.70000000e+01, 2.50000000e+01, 0.00000000e+00, 1.56000000e+02,
               8.00000000e+00, 5.40000000e+01, 0.00000000e+00, 1.07000000e+02,
               0.00000000e+00, 0.00000000e+00, 1.40000000e+01, 0.00000000e+00]])
               
AH96_mtmammals_freqs = {
            'A': 0.069199999999999998, 'C': 0.0064999999999999997,
            'E': 0.023599999999999999, 'D': 0.018599999999999998,
            'G': 0.0557, 'F': 0.061100000000000002,
            'I': 0.090499999999999997, 'H': 0.027699999999999999,
            'K': 0.022100000000000002, 'M': 0.056099999999999997,
            'L': 0.16750000000000001, 'N': 0.040000000000000001,
            'Q': 0.023800000000000002, 'P': 0.053600000000000002,
            'S': 0.072499999999999995, 'R': 0.0184,
            'T': 0.086999999999999994, 'W': 0.0293,
            'V': 0.042799999999999998, 'Y': 0.034000000000000002}
            
WG01_matrix = numpy.array(
        [[ 0.      , 1.02704 , 0.738998, 1.58285 , 0.210494, 1.41672 ,
              0.316954, 0.193335, 0.906265, 0.397915, 0.893496, 0.509848,
              1.43855 , 0.908598, 0.551571, 3.37079 , 2.12111 , 2.00601 ,
              0.113133, 0.240735 ],
       [ 1.02704 , 0.      , 0.0302949, 0.021352, 0.39802 , 0.306674,
              0.248972, 0.170135, 0.0740339, 0.384287, 0.390482, 0.265256,
              0.109404, 0.0988179, 0.528191, 1.40766 , 0.512984, 1.00214 ,
              0.71707 , 0.543833 ],
       [ 0.738998, 0.0302949, 0.      , 6.17416 , 0.0467304, 0.865584,
              0.930676, 0.039437, 0.479855, 0.0848047, 0.103754, 5.42942 ,
              0.423984, 0.616783, 0.147304, 1.07176 , 0.374866, 0.152335,
              0.129767, 0.325711 ],
       [ 1.58285 , 0.021352, 6.17416 , 0.      , 0.0811339, 0.567717,
              0.570025, 0.127395, 2.58443 , 0.154263, 0.315124, 0.947198,
              0.682355, 5.46947 , 0.439157, 0.704939, 0.822765, 0.588731,
              0.156557, 0.196303 ],
       [ 0.210494, 0.39802 , 0.0467304, 0.0811339, 0.      , 0.049931,
              0.679371, 1.05947 , 0.088836, 2.11517 , 1.19063 , 0.0961621,
              0.161444, 0.0999208, 0.102711, 0.545931, 0.171903, 0.649892,
              1.52964 , 6.45428  ],
       [ 1.41672 , 0.306674, 0.865584, 0.567717, 0.049931, 0.      ,
              0.24941 , 0.0304501, 0.373558, 0.0613037, 0.1741  , 1.12556 ,
              0.24357 , 0.330052, 0.584665, 1.34182 , 0.225833, 0.187247,
              0.336983, 0.103604 ],
       [ 0.316954, 0.248972, 0.930676, 0.570025, 0.679371, 0.24941 ,
              0.      , 0.13819 , 0.890432, 0.499462, 0.404141, 3.95629 ,
              0.696198, 4.29411 , 2.13715 , 0.740169, 0.473307, 0.118358,
              0.262569, 3.87344  ],
       [ 0.193335, 0.170135, 0.039437, 0.127395, 1.05947 , 0.0304501,
              0.13819 , 0.      , 0.323832, 3.17097 , 4.25746 , 0.554236,
              0.0999288, 0.113917, 0.186979, 0.31944 , 1.45816 , 7.8213  ,
              0.212483, 0.42017  ],
       [ 0.906265, 0.0740339, 0.479855, 2.58443 , 0.088836, 0.373558,
              0.890432, 0.323832, 0.      , 0.257555, 0.934276, 3.01201 ,
              0.556896, 3.8949  , 5.35142 , 0.96713 , 1.38698 , 0.305434,
              0.137505, 0.133264 ],
       [ 0.397915, 0.384287, 0.0848047, 0.154263, 2.11517 , 0.0613037,
              0.499462, 3.17097 , 0.257555, 0.      , 4.85402 , 0.131528,
              0.415844, 0.869489, 0.497671, 0.344739, 0.326622, 1.80034 ,
              0.665309, 0.398618 ],
       [ 0.893496, 0.390482, 0.103754, 0.315124, 1.19063 , 0.1741  ,
              0.404141, 4.25746 , 0.934276, 4.85402 , 0.      , 0.198221,
              0.171329, 1.54526 , 0.683162, 0.493905, 1.51612 , 2.05845 ,
              0.515706, 0.428437 ],
       [ 0.509848, 0.265256, 5.42942 , 0.947198, 0.0961621, 1.12556 ,
              3.95629 , 0.554236, 3.01201 , 0.131528, 0.198221, 0.      ,
              0.195081, 1.54364 , 0.635346, 3.97423 , 2.03006 , 0.196246,
              0.0719167, 1.086    ],
       [ 1.43855 , 0.109404, 0.423984, 0.682355, 0.161444, 0.24357 ,
              0.696198, 0.0999288, 0.556896, 0.415844, 0.171329, 0.195081,
              0.      , 0.933372, 0.679489, 1.61328 , 0.795384, 0.314887,
              0.139405, 0.216046 ],
       [ 0.908598, 0.0988179, 0.616783, 5.46947 , 0.0999208, 0.330052,
              4.29411 , 0.113917, 3.8949  , 0.869489, 1.54526 , 1.54364 ,
              0.933372, 0.      , 3.0355  , 1.02887 , 0.857928, 0.301281,
              0.215737, 0.22771  ],
       [ 0.551571, 0.528191, 0.147304, 0.439157, 0.102711, 0.584665,
              2.13715 , 0.186979, 5.35142 , 0.497671, 0.683162, 0.635346,
              0.679489, 3.0355  , 0.      , 1.22419 , 0.554413, 0.251849,
              1.16392 , 0.381533 ],
       [ 3.37079 , 1.40766 , 1.07176 , 0.704939, 0.545931, 1.34182 ,
              0.740169, 0.31944 , 0.96713 , 0.344739, 0.493905, 3.97423 ,
              1.61328 , 1.02887 , 1.22419 , 0.      , 4.37802 , 0.232739,
              0.523742, 0.786993 ],
       [ 2.12111 , 0.512984, 0.374866, 0.822765, 0.171903, 0.225833,
              0.473307, 1.45816 , 1.38698 , 0.326622, 1.51612 , 2.03006 ,
              0.795384, 0.857928, 0.554413, 4.37802 , 0.      , 1.38823 ,
              0.110864, 0.291148 ],
       [ 2.00601 , 1.00214 , 0.152335, 0.588731, 0.649892, 0.187247,
              0.118358, 7.8213  , 0.305434, 1.80034 , 2.05845 , 0.196246,
              0.314887, 0.301281, 0.251849, 0.232739, 1.38823 , 0.      ,
              0.365369, 0.31473  ],
       [ 0.113133, 0.71707 , 0.129767, 0.156557, 1.52964 , 0.336983,
              0.262569, 0.212483, 0.137505, 0.665309, 0.515706, 0.0719167,
              0.139405, 0.215737, 1.16392 , 0.523742, 0.110864, 0.365369,
              0.      , 2.48539  ],
       [ 0.240735, 0.543833, 0.325711, 0.196303, 6.45428 , 0.103604,
              3.87344 , 0.42017 , 0.133264, 0.398618, 0.428437, 1.086   ,
              0.216046, 0.22771 , 0.381533, 0.786993, 0.291148, 0.31473 ,
              2.48539 , 0.       ]])

WG01_freqs = {
            'A': 0.086627908662790867, 'C': 0.019307801930780195,
            'E': 0.058058905805890577, 'D': 0.057045105704510574,
            'G': 0.083251808325180837, 'F': 0.038431903843190382,
            'I': 0.048466004846600491, 'H': 0.024431302443130246,
            'K': 0.062028606202860624, 'M': 0.019502701950270197,
            'L': 0.086209008620900862, 'N': 0.039089403908940397,
            'Q': 0.036728103672810368, 'P': 0.045763104576310464,
            'S': 0.069517906951790692, 'R': 0.043972004397200441,
            'T': 0.061012706101270617, 'W': 0.014385901438590145,
            'V': 0.070895607089560719, 'Y': 0.035274203527420354}

def DSO78():
    """Dayhoff et al 1978 empirical protein model
    Dayhoff, MO, Schwartz RM, and Orcutt, BC. 1978
    A model of evolutionary change in proteins. Pp. 345-352.
    Atlas of protein sequence and structure, Vol 5, Suppl. 3.
    National Biomedical Research Foundation,  Washington D. C
    Matrix imported from PAML dayhoff.dat file"""
    sm = substitution_model.EmpiricalProteinMatrix(
                    DSO78_matrix, DSO78_freqs, name='DSO78')
                        
    return sm
    
def JTT92():
    """Jones, Taylor and Thornton 1992 empirical protein model
    Jones DT, Taylor WR, Thornton JM.
    The rapid generation of mutation data matrices from protein sequences.
    Comput Appl Biosci. 1992 Jun;8(3):275-82.
    Matrix imported from PAML jones.dat file"""
    sm = substitution_model.EmpiricalProteinMatrix(
                    JTT92_matrix, JTT92_freqs, name='JTT92')
                        
    return sm
    
def AH96():
    """Adachi and Hasegawa 1996 empirical model for mitochondrial proteins.
    Adachi J, Hasegawa M.
    Model of amino acid substitution in proteins encoded by mitochondrial DNA.
    J Mol Evol. 1996 Apr;42(4):459-68.
    Matrix imported from PAML mtREV24.dat file"""
    sm = substitution_model.EmpiricalProteinMatrix(
                    AH96_matrix,
                    AH96_freqs,
                    name='AH96_mtREV24')
                        
    return sm
    
def mtREV():
    return AH96()

def AH96_mtmammals():
    """Adachi and Hasegawa 1996 empirical model for mammalian mitochondrial
    proteins.
    Adachi J, Hasegawa M.
    Model of amino acid substitution in proteins encoded by mitochondrial DNA.
    J Mol Evol. 1996 Apr;42(4):459-68.
    Matrix imported from PAML mtmam.dat file"""
    sm = substitution_model.EmpiricalProteinMatrix(
                    AH96_mtmammals_matrix,
                    AH96_mtmammals_freqs,
                    name='AH96_mtmammals')
    
    return sm
    
def mtmam():
    return AH96_mtmammals()
    
def WG01():
    """Whelan and Goldman 2001 empirical model for globular proteins.
    Whelan S, Goldman N.
    A general empirical model of protein evolution derived from multiple protein
    families using a maximum-likelihood approach.
    Mol Biol Evol. 2001 May;18(5):691-9.
    Matrix imported from PAML wag.dat file"""
    sm = substitution_model.EmpiricalProteinMatrix(
                    WG01_matrix,
                    WG01_freqs,
                    name='WG01')
                    
    return sm

