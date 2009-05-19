Specifying and using an restricted nucleotide substitution model
================================================================

Do standard ``cogent`` imports.

.. doctest::

    >>> from cogent import LoadSeqs, LoadTree, DNA
    >>> from cogent.evolve.predicate import MotifChange
    >>> from cogent.evolve.substitution_model import Nucleotide

.. don't pollute screen during execution with uninteresting warning

.. doctest::
    :hide:
    
    >>> import warnings
    >>> warnings.filterwarnings("ignore", "Model not reversible")

To specify substitution models we use the ``MotifChange`` class from predicates. In the case of an unrestricted nucleotide model, we specify 11 such ``MotifChanges``, the last possible change being ignored (with the result it is constrained to equal 1, thus calibrating the matrix).

.. doctest::

    >>> ACTG = list('ACTG')
    >>> preds = [MotifChange(i, j, forward_only=True) for i in ACTG for j in ACTG if i != j]
    >>> del(preds[-1])
    >>> preds
    [A>C, A>T, A>G, C>A, C>T, C>G, T>A, T>C, T>G, G>A, G>C]
    >>> sm = Nucleotide(predicates=preds, recode_gaps=True)
    >>> print sm
    <BLANKLINE>
    Nucleotide ( name = ''; type = 'None'; params = ['A>T', 'C>G', 'T>G', 'G>A', 'T>A', 'T>C', 'C>A', 'G>C', 'C>T', 'A>G', 'A>C']; number of motifs = 4; motifs = ['T', 'C', 'A', 'G'])
    <BLANKLINE>

We'll illustrate this with a sample alignment and tree in "data/test.paml".

.. doctest::

    >>> tr = LoadTree("data/test.tree")
    >>> print tr
    (((Human,HowlerMon),Mouse),NineBande,DogFaced);
    >>> al = LoadSeqs("data/test.paml", moltype=DNA)
    >>> al
    5 x 60 dna alignment: NineBande[GCAAGGCGCCA...], Mouse[GCAGTGAGCCA...], Human[GCAAGGAGCCA...], ...

We now construct the parameter controller with each predicate constant across the tree, and get the likelihood function calculator.

.. doctest::

    >>> lf = sm.makeLikelihoodFunction(tr)
    >>> lf.setAlignment(al)
    >>> lf.setName('Unrestricted model')
    >>> lf.optimise()
    Outer loop = 0...

In the output from the ``optimise`` call you'll see progress from the simulated annealing optimiser which is used first, and the Powell optimiser which finishes things off.

.. doctest::

    >>> print lf
    Unrestricted model
    ============================================================================
       A>C       A>G       A>T       C>A       C>G       C>T       G>A       G>C
    ----------------------------------------------------------------------------
    0.6890    1.8880    0.0000    0.0000    0.0000    2.1652    0.2291    0.4868
    ----------------------------------------------------------------------------
    <BLANKLINE>
    continued:
    ====================================
       A>C       T>A       T>C       T>G
    ------------------------------------
    0.6890    0.0000    2.2755    0.0000
    ------------------------------------
    <BLANKLINE>
    =============================
         edge    parent    length
    -----------------------------
        Human    edge.0    0.0333
    HowlerMon    edge.0    0.0165
       edge.0    edge.1    0.0164
        Mouse    edge.1    0.1980
       edge.1      root    0.0000
    NineBande      root    0.0335
     DogFaced      root    0.0503
    -----------------------------
    ===============
    motif    mprobs
    ---------------
        T    0.1433
        C    0.1600
        A    0.3800
        G    0.3167
    ---------------

This data set is very small, so the parameter estimates are poor and hence doing something like allowing the parameters to differ between edges is silly. **But** if you have lots of data it makes sense and can be specified by modifying the ``lf`` as follows.

.. doctest::

    >>> for pred in preds:
    ...     lf.setParamRule(str(pred), is_independent=True)

You then make a new ``lf`` and optimise as above, but I won't do that now as the optimiser would struggle due to the low information content of this sample.