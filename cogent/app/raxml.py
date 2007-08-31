#!/usr/bin/env python
"""Application controller for RAxML-V (v2.23) 
"""
from cogent.app.parameters import FlagParameter, ValuedParameter
from cogent.app.util import CommandLineApplication, ResultPath
from random import choice
from os import walk
from cogent.parse.tree import DndParser

__author__ = "Micah Hamady"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Micah Hamady", "Catherine Lozupone", "Rob Knight"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Micah Hamady"
__email__ = "hamady@colorado.edu"
__status__ = "Prototype"

class Raxml(CommandLineApplication):
    """RAxML application controller"""

    _options ={

        # Specify a column weight file name to assign individual wieghts to 
        # each column of the alignment. Those weights must be integers 
        # separated by any number and type of whitespaces whithin a separate 
        # file, see file "example_weights" for an example.
        '-a':ValuedParameter('-',Name='a',Delimiter=' '),

        #  Specify an integer number (random seed) for bootstrapping
        '-b':ValuedParameter('-',Name='b',Delimiter=' '),


        # Specify number of distinct rate catgories for raxml when 
        # ModelOfEvolution is set to GTRCAT or HKY85CAT.
        # Individual per-site rates are categorized into numberOfCategories 
        # rate categories to accelerate computations. (Default = 50)
        '-c':ValuedParameter('-',Name='c',Delimiter=' ', Value=50),

        # This option allows you to start the RAxML search with a complete 
        # random starting tree instead of the default Maximum Parsimony 
        # Starting tree. On smaller datasets (around 100-200 taxa) it has 
        # been observed that this might sometimes yield topologies of distinct 
        # local likelihood maxima which better correspond to empirical 
        # expectations. 
        '-d':FlagParameter('-',Name='d'),

        # This allows you to specify up to which likelihood difference.
        # Default is 0.1 log likelihood units, author recommends 1 or 2 to
        # rapidly evaluate different trees.
        
        '-e':ValuedParameter('-',Name='e',Delimiter=' ', Value=0.1),
        

        # select search algorithm: 
        #   d for normal hill-climbing search (Default)
        #     when -f option is omitted this algorithm will be used
        #   o old (slower) algorithm from v. 2.1.3
        #   c (check) just tests whether it can read the alignment
        #   e (evaluate) to optimize model+branch lengths for given input tree
        #   b (bipartition) draws bipartitions
        #   s (split) splits into individual genes, provided with model file
        '-f':ValuedParameter('-',Name='f',Delimiter=' ', Value="d"),

        # select grouping file name: allows incomplete multifurcating constraint
        # tree in newick format -- resolves multifurcations randomly, adds
        # other taxa using parsimony insertion
        '-g':ValuedParameter('-', Name='g',Delimiter=' '),

        # prints help and exits

        '-h':FlagParameter('-', Name='h'),

        # allows initial rearrangement to be constrained, e.g. 10 means
        # insertion will not be more than 10 nodes away from original.
        # default is to pick a "good" setting.

        '-i':ValuedParameter('-', Name='i', Delimiter=' '),

        # writes checkpoints (off by default)

        '-j':FlagParameter('-', Name='j'),

        #specifies that RAxML will optimize model parameters (for GTRMIX and
        # GTRGAMMA) as well as calculating likelihoods for bootstrapped trees.

        '-k':FlagParameter('-', Name='k'),

        # Model of Nucleotide Substitution:
        # -m GTRGAMMA: GTR + Optimization of substitution rates + Gamma
        # -m GTRCAT: GTR + Optimization of substitution rates +  Optimization 
        #    of site-specific evolutionary rates which are categorized into 
        #    numberOfCategories distinct rate categories for greater 
        #    computational efficiency
        # -m GTRMIX: Searches for GTRCAT, then switches to GTRGAMMA
        
        # Amino Acid Models
        # matrixName (see below): DAYHOFF, DCMUT, JTT, MTREV, WAG, RTREV, 
        # CPREV, VT, BLOSUM62, MTMAM, GTR.
        # F means use empirical nucleotide frequencies (append to string)
        # -m PROTCATmatrixName[F]: uses site-specific rate categories
        # -m PROTGAMMAmatrixName[F]: uses Gamma
        # -m PROTMIXmatrixName[F]: switches between gamma and cat models
        # e.g. -m PROTCATBLOSUM62F would use protcat with BLOSUM62 and
        # empirical frequencies

        '-m':ValuedParameter('-',Name='m',Delimiter=' '),

        # Specifies the name of the output file.
        '-n':ValuedParameter('-',Name='n',Delimiter=' '),

        # Specifies the name of the outgroup (or outgroups: comma-delimited,
        # no spaces, should be monophyletic).
        '-o':ValuedParameter('-',Name='o',Delimiter=' '),

        # Specified MultipleModel file name, in format:
        #    gene1 = 1-500
        #    gene2 = 501-1000
        #    (note: ranges can also be discontiguous, e.g. 1-100, 200-300,
        #     or can specify codon ranges as e.g. 1-100/3, 2-100/3, 3-100/3))
        '-q':ValuedParameter('-', Name='q', Delimiter=' '),

        # Name of the working directory where RAxML-V will write its output 
        # files.
        '-w':ValuedParameter('-',Name='w',Delimiter=' '),

        # Constraint file name: allows a bifurcating Newick tree to be passed
        # in as a constraint file, other taxa will be added by parsimony.
        '-r':ValuedParameter('-',Name='r',Delimiter=' '),
        
        # specify the name of the alignment data file, in relaxed PHYLIP
        # format.
        '-s':ValuedParameter('-',Name='s',Delimiter=' '),

        # Specify a user starting tree file name in Newick format
        '-t':ValuedParameter('-',Name='t',Delimiter=' '),

        # Print the version
        '-v':FlagParameter('-',Name='v'),

        # Specify working directory for output files
        '-w':ValuedParameter('-', Name='w', Delimiter=' '),

        # Compute only randomized starting parsimony tree with RAxML, do not
        # optimize an ML analysis of the tree
        '-y':FlagParameter('-', Name='y'),

        # Multiple tree file, for use with -f b (to draw bipartitions onto the
        # common tree specified with -t)
        '-z':ValuedParameter('-', Name='z', Delimiter=' '),

        # Specifies number of runs on distinct starting trees.
        '-#':ValuedParameter('-', Name='#', Delimiter=' '),


    }

    _parameters = {}
    _parameters.update(_options)
    _command = "raxmlHPC"
    _out_format = "RAxML_%s.%s"

    def _input_as_seqs(self,data):
        lines = []
        for i,s in enumerate(data):
            #will number the sequences 1,2,3,etc.
            lines.append(''.join(['>',str(i+1)]))
            lines.append(s)
        return self._input_as_lines(lines)

    def _input_as_lines(self,data):
        if data:
            self.Parameters['-s']\
                .on(super(Raxml,self)._input_as_lines(data))
        return ''

    def _input_as_string(self,data):
        """Makes data the value of a specific parameter
     
        This method returns the empty string. The parameter will be printed
        automatically once set.
        """
        if data:
            self.Parameters['-in'].on(str(data))
        return ''

    def _input_as_multiline_string(self, data):
        if data:
            self.Parameters['-s']\
                .on(super(Raxml,self)._input_as_multiline_string(data))
        return ''

   
    def _absolute(self,path):
        if path.startswith('/'):
            return path
        elif self.Parameters['-w'].isOn():
            return self.Parameters['-w'].Value + path
        else:
            return self.WorkingDir + path

    def _log_out_filename(self):
        if self.Parameters['-n'].isOn():
            out_filename = self._absolute(
                   self._out_format % ("log", str(self.Parameters['-n'].Value)))
        else:
            raise ValueError, "No output file specified." 
        return out_filename

    def _info_out_filename(self):
        if self.Parameters['-n'].isOn():
            out_filename = self._absolute(
                   self._out_format % ("info",
                                        str(self.Parameters['-n'].Value)))
        else:
            raise ValueError, "No output file specified." 
        return out_filename

    def _parsimony_tree_out_filename(self):
        if self.Parameters['-n'].isOn():
            out_filename = self._absolute(
                   self._out_format % ("parsimonyTree",
                                        str(self.Parameters['-n'].Value)))
        else:
            raise ValueError, "No output file specified." 
        return out_filename

    def _result_tree_out_filename(self):
        if self.Parameters['-n'].isOn():
            out_filename = self._absolute(
                   self._out_format % ("result",
                                        str(self.Parameters['-n'].Value)))
        else:
            raise ValueError, "No output file specified." 
        return out_filename


    def _checkpoint_out_filenames(self):
        """
        RAxML generates a crapload of checkpoint files so need to
        walk directory to collect names of all of them.
        """
        out_filenames = []
        if self.Parameters['-n'].isOn():
            out_name = str(self.Parameters['-n'].Value)
            walk_root = self.WorkingDir
            if self.Parameters['-w'].isOn(): 
                walk_root = str(self.Parameters['-w'].Value)
            for tup in walk(walk_root):
                dpath, dnames, dfiles = tup
                if dpath == walk_root:
                    for gen_file in dfiles:
                        if out_name in gen_file and "checkpoint" in gen_file:
                            out_filenames.append(walk_root + gen_file)
                    break

        else:
            raise ValueError, "No output file specified." 
        return out_filenames

    def _get_result_paths(self,data):
        
        result = {}
        result['Log'] = ResultPath(Path=self._log_out_filename(),
                                            IsWritten=True)
        result['Info'] = ResultPath(Path=self._info_out_filename(),
                                            IsWritten=True)
        result['ParsimonyTree'] = ResultPath(
                        Path=self._parsimony_tree_out_filename(),
                        IsWritten=True)
        result['Result'] = ResultPath(
                        Path=self._result_tree_out_filename(),
                        IsWritten=True)
        for checkpoint_file in self._checkpoint_out_filenames():
            checkpoint_num = checkpoint_file.split(".")[-1]
            try:
                checkpoint_num = int(checkpoint_num)
            except Exception, e:
                raise ValueError, "%s does not appear to be a valid checkpoint file"
            result['Checkpoint%d' % checkpoint_num] = ResultPath(
                        Path=checkpoint_file,
                        IsWritten=True)
 
        return result


#SOME FUNCTIONS TO EXECUTE THE MOST COMMON TASKS
def raxml_alignment(align_obj,
                 params={},
                 SuppressStderr=True,
                 SuppressStdout=True):
    """Run raxml on alignment object 

    align_obj: Alignment object
    params: you can set any params except -w and -n

    returns: tuple (phylonode, 
                    parsimonyphylonode, 
                    log likelihood, 
                    total exec time)
    """

    # generate temp filename for output
    params["-w"] = "/tmp/"
    params["-n"] = get_tmp_filename()
    ih = '_input_as_multiline_string'
    seqs, align_map = align_obj.toPhylip()

    # set up command
    raxml_app = Raxml(
                   params=params,
                   InputHandler=ih,
                   WorkingDir=None,
                   SuppressStderr=SuppressStderr,
                   SuppressStdout=SuppressStdout)

    # run raxml
    ra = raxml_app(seqs)

    # generate tree
    tree_node =  DndParser(ra["Result"])

    # generate parsimony tree
    parsimony_tree_node =  DndParser(ra["ParsimonyTree"])

    # extract log likelihood from log file
    log_file = ra["Log"]
    total_exec_time = exec_time = log_likelihood = 0.0
    for line in log_file:
        exec_time, log_likelihood = map(float, line.split())
        total_exec_time += exec_time

    # remove output files
    ra.cleanUp()

    return tree_node, parsimony_tree_node, log_likelihood, total_exec_time

def get_tmp_filename(tmp_dir=""):
    # temp hack - change this to lookup and generate file in class
    chars = "abcdefghigklmnopqrstuvwxyz"
    all_chars = chars + chars.upper() + "0123456789"
    picks = list(all_chars)
    if tmp_dir:
        tmp_dir = tmp_dir + "/"

    return tmp_dir + "tmp%s.txt" % ''.join([choice(picks) for i in range(10)]) 


