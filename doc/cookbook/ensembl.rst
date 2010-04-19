Note that much more extensive documentation is available in :ref:`query-ensembl`.

Connecting
----------

.. Gavin Huttley

`Ensembl <http://www.ensembl.org>`_ provides access to their MySQL databases directly or users can download and run those databases on a local machine. To use the Ensembl's UK servers for running queries, nothing special needs to be done as this is the default setting for PyCogent's ``ensembl`` module. To use a different Ensembl installation, you create an account instance:

.. doctest::

    >>> from cogent.db.ensembl import HostAccount
    >>> account = HostAccount('fastcomputer.topuni.edu', 'username',
    ...                       'canthackthis')

To specify a specific port to connect to MySQL on:

.. doctest::

    >>> from cogent.db.ensembl import HostAccount
    >>> account = HostAccount('fastcomputer.topuni.edu', 'dude',
    ...                       'ucanthackthis', port=3306)

.. we create valid account now to work on my local machines here at ANU

.. doctest::
    :hide:

    >>> import os
    >>> uname, passwd = os.environ['ENSEMBL_ACCOUNT'].split()
    >>> account = HostAccount('cg.anu.edu.au', uname, passwd)

Species to be queried
---------------------

To see what existing species are available

.. doctest::

    >>> from cogent.db.ensembl import Species
    >>> print Species
    ================================================================================
           Common Name                   Species Name              Ensembl Db Prefix
    --------------------------------------------------------------------------------
             A.aegypti                  Aedes aegypti                  aedes_aegypti
                Alpaca                  Vicugna pacos                  vicugna_pacos...

If Ensembl has added a new species which is not yet included in ``Species``, you can add it yourself.

.. doctest::

    >>> Species.amendSpecies('A latinname', 'a common name')

You can get the common name for a species

.. doctest::

    >>> Species.getCommonName('Procavia capensis')
    'Rock hyrax'

and the Ensembl database name prefix which will be used for all databases for this species.

.. doctest::

    >>> Species.getEnsemblDbPrefix('Procavia capensis')
    'procavia_capensis'

Get genomic features
--------------------

Find a gene by gene symbol
^^^^^^^^^^^^^^^^^^^^^^^^^^

We query for the *BRCA2* gene for humans.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> print human
    Genome(Species='Homo sapiens'; Release='56')
    >>> genes = human.getGenesMatching(Symbol='BRCA2')
    >>> for gene in genes:
    ...     if gene.Symbol == 'BRCA2':
    ...         print gene
    ...         break
    Gene(Species='Homo sapiens'; BioType='protein_coding'; Description='Breast cancer type...'; StableId='ENSG00000139618'; Status='KNOWN'; Symbol='BRCA2')

Find a gene by Ensembl Stable ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We use the stable ID for *BRCA2*.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> for gene in genes:
    ...     if gene.Symbol == 'BRCA2':
    ...         print gene
    ...         break
    Gene(Species='Homo sapiens'; BioType='protein_coding'; Description='Breast cancer type...'; StableId='ENSG00000139618'; Status='KNOWN'; Symbol='BRCA2')

Find genes matching a description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We look for breast cancer related genes that are estrogen induced.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(Description='breast cancer estrogen')
    >>> for gene in genes:
    ...     print gene
    Gene(Species='Homo sapiens'; BioType='protein_coding'; Description='Trefoil factor 1...'; StableId='ENSG00000160182'; Status='KNOWN'; Symbol='TFF1')
    Gene(Species='Homo sapiens'; BioType='protein_coding'; Description='breast cancer estrogen-induced...'; StableId='ENSG00000181097'; Status='KNOWN'; Symbol='AC105219.2')

Get canonical transcript for a gene
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We get the canonical transcripts for *BRCA2*.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> transcript = brca2.CanonicalTranscript
    >>> print transcript
    Transcript(Species='Homo sapiens'; CoordName='13'; Start=32889610; End=32973347; length=83737; Strand='+')

Get the CDS for a transcript
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> transcript = brca2.CanonicalTranscript
    >>> cds = transcript.Cds
    >>> print type(cds)
    <class 'cogent.core.sequence.DnaSequence'>
    >>> print cds
    ATGCCTATTGGATCCAAAGAGAGGCCA...

Look at all transcripts for a gene
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> for transcript in brca2.Transcripts:
    ...     print transcript
    Transcript(Species='Homo sapiens'; CoordName='13'; Start=32953976; End=32972409; length=18433; Strand='+')
    Transcript(Species='Homo sapiens'; CoordName='13'; Start=32889610; End=32973347; length=83737; Strand='+')

Get the first exon for a transcript
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We show just for the canonical transcript.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> print brca2.CanonicalTranscript.Exons[0]
    Exon(StableId=ENSE00001184784, Rank=1)

Inspect the genomic coordinate for a feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> print brca2.Location.CoordName
    13
    >>> print brca2.Location.Start
    32889610
    >>> print brca2.Location.Strand
    1

Get repeat elements in a genomic interval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We query the genome for repeats within a specific coordinate range on chromosome 13.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> repeats = human.getFeatures(CoordName='13', Start=32879610, End=32889610, feature_types='repeat')
    >>> for repeat in repeats:
    ...     print repeat.RepeatClass
    ...     print repeat
    ...     break
    SINE/Alu
    Repeat(CoordName='13'; Start=32879362; End=32879662; length=300; Strand='-', Score=2479.0)

Get CpG island elements in a genomic interval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We query the genome for CpG islands within a specific coordinate range on chromosome 11.

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> islands = human.getFeatures(CoordName='11', Start=2150341, End=2170833, feature_types='cpg')
    >>> for island in islands:
    ...     print island
    ...     break
    CpGisland(CoordName='11'; Start=2158951; End=2162484; length=3533; Strand='-', Score=3254.0)

Get SNPs
--------

We find the genetic variants for the canonical transcript of *BRCA2*.

.. note:: The output is significantly truncated!

.. doctest::

    >>> from cogent.db.ensembl import Genome
    >>> human = Genome('human', Release=56, account=account)
    >>> genes = human.getGenesMatching(StableId='ENSG00000139618')
    >>> brca2 = [gene for gene in genes][0]
    >>> transcript = brca2.CanonicalTranscript
    >>> print transcript.Variants
    (<cogent.db.ensembl.region.Variation object at ...
    >>> for variant in transcript.Variants:
    ...     print variant
    ...     break
    Variation(Symbol='rs55880202'; Effect='5PRIME_UTR'; Alleles='C/T')...

What alignment types available
------------------------------

We create a ``Compara`` instance for human, chimpanzee and macaque.

.. doctest::

    >>> from cogent.db.ensembl import Compara
    >>> compara = Compara(['human', 'chimp', 'macaque'], Release=56,
    ...                  account=account)
    >>> print compara.method_species_links
    Align Methods/Clades
    ===================================================================================================================
    method_link_species_set_id  method_link_id  species_set_id      align_method                            align_clade
    -------------------------------------------------------------------------------------------------------------------
                           424              10           32309             PECAN           12 amniota vertebrates Pecan
                           426              13           32310               EPO              4 catarrhini primates EPO...


Get genomic alignment for a gene region
---------------------------------------

We first get the syntenic region corresponding to human gene *BRCA2*.

.. doctest::

    >>> from cogent.db.ensembl import Compara
    >>> compara = Compara(['human', 'chimp', 'macaque'], Release=56,
    ...                  account=account)
    >>> genes = compara.Human.getGenesMatching(StableId='ENSG00000139618')
    >>> human_brca2 = [gene for gene in genes][0]
    >>> regions = compara.getSyntenicRegions(region=human_brca2, align_method='EPO', align_clade='primates')
    >>> for region in regions:
    ...     print region
    SyntenicRegions:
      Coordinate(Human,chro...,13,32889610-32973347,1)
      Coordinate(Chimp,chro...,13,32082473-32165688,1)
      Coordinate(Macaque,chro...,17,11686607-11778359,1)

We then get a cogent ``Alignment`` object, requesting that sequences be annotated for gene spans.

.. doctest::

    >>> aln = region.getAlignment(feature_types='gene')
    >>> print repr(aln)
    3 x 97987 dna alignment: Homo sapiens:chromosome:13:3288961...

Getting related genes
---------------------

What gene relationships are available
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.db.ensembl import Compara
    >>> compara = Compara(['human', 'chimp', 'macaque'], Release=56,
    ...                  account=account)
    >>> print compara.getDistinct('relationship')
    ['within_species_paralog', 'ortholog_one2one', 'ortholog_one2many',...

Get one-to-one orthologs
^^^^^^^^^^^^^^^^^^^^^^^^

We get the one-to-one orthologs for *BRCA2*.

.. doctest::

    >>> from cogent.db.ensembl import Compara
    >>> compara = Compara(['human', 'chimp', 'macaque'], Release=56,
    ...                  account=account)
    >>> orthologs = compara.getRelatedGenes(StableId='ENSG00000139618',
    ...                  Relationship='ortholog_one2one')
    >>> print orthologs
    RelatedGenes:
     Relationships=ortholog_one2one
      Gene(Species='Pan troglodytes'; BioType='protein_coding'; Description='Breast cancer 2...'; Location=Coordinate(Chimp,chro...,13,32082479-32166147,1); StableId='ENSPTRG00000005766'; Status='KNOWN'; Symbol='Q8HZQ1_PANTR')...

We iterate over the related members.

.. doctest::
    
    >>> for ortholog in orthologs.Members:
    ...     print ortholog
    Gene(Species='Pan troglodytes'; BioType='protein_coding'; Description='Breast...

We get statistics on the ortholog CDS lengths.

.. doctest::
    
    >>> print orthologs.getMaxCdsLengths()
    [10242, 10008, 10257]

We get the sequences as a sequence collection, with annotations for gene.

.. doctest::
    
    >>> seqs = orthologs.getSeqCollection(feature_types='gene')

Get within species paralogs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::
    
    >>> paralogs = compara.getRelatedGenes(StableId='ENSG00000164032',
    ...             Relationship='within_species_paralog')
    >>> print paralogs
    RelatedGenes:
     Relationships=within_species_paralog
      Gene(Species='Homo sapiens'; BioType='protein_coding'; Description='Histone...
