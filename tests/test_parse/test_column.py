#!/usr/bin/env python

from cogent.util.unit_test  import TestCase, main
from cogent.core.info       import Info
from cogent.parse.foldalign import find_struct
from cogent.parse.pfold     import tree_struct_sep
from cogent.parse.column    import column_parser

__author__ = "Shandy Wikman"
__copyright__ = "Copyright 2007-2011, The Cogent Project"
__contributors__ = ["Shandy Wikman"]
__license__ = "GPL"
__version__ = "1.6.0dev"
__maintainer__ = "Shandy Wikman"
__email__ = "ens01svn@cs.umu.se"
__status__ = "Development"

class ColumnParserTest(TestCase):
    """Provides tests for Column format RNA secondary structure parsers"""

    def setUp(self):
        """Setup function"""
        
        #output
        self.pfold_out = PFOLD
        self.foldalign_out = FOLDALIGN
        #expected
        self.pfold_exp = [['GCAGAUUUAGAUGC',[(0,13),(1,12),(2,11),(6,10)]]]
        self.foldalign_exp = [['GCAGAUUUAGAUGC',[(0,13),(1,12),(2,11),(6,10)]]]
        self.find_struct_exp = [[[(0,13),(1,12),(2,11),(6,10)],'GCCACGUAGCUCAG',
                                'GCCGUAUGUUUCAG']]
        
    def test_pfold_output(self):
        """Test for column_parser for pfold format"""
        
        tree,lines = tree_struct_sep(self.pfold_out)
        self.assertEqual(tree,PFOLD_tree)
        obs = column_parser(lines)
        self.assertEqual(obs,self.pfold_exp)

    def test_foldalign_output(self):
        """Test for column_parser for foldalign format"""
        
        obs = column_parser(self.foldalign_out)
        self.assertEqual(obs,self.foldalign_exp)

    def test_foldalign_find_struct(self):
        """ Test for foldalign parser find struct function"""

        obs = find_struct(self.foldalign_out)
        self.assertEqual(obs,self.find_struct_exp)


FOLDALIGN = ['; FOLDALIGN           2.0.3\n', 
'; REFERENCE           J.H. Havgaard, R.B. Lyngs\xf8, G.D. Stormo, J. Gorodkin\n', 
'; REFERENCE           Pairwise local structural alignment of RNA sequences\n',
 '; REFERENCE           with sequence similarity less than 40%\n', 
'; REFERENCE           Bioinformatics 21(9), 1815-1824, 2005\n', 
'; ALIGNMENT_ID        n.a.\n', '; ALIGNING            seq1 against seq2\n', 
'; ALIGN               seq1          \n', 
'; ALIGN               seq2          \n', 
'; ALIGN               Score: 929\n', 
'; ALIGN               Identity: 69 % ( 48 / 70 )\n', 
'; ALIGN               Begin\n', '; ALIGN\n', 
'; ALIGN               seq1          GCCACGUAGC UCAG\n', 
'; ALIGN               Structure     (((...(... ))))\n', 
'; ALIGN               seq2          GCCGUAUGUU UCAG\n', 
'; ALIGN \n', '; ALIGN               End\n', 
'; ==============================================================================\n', 
'; TYPE                RNA\n', '; COL 1               label\n', 
'; COL 2               residue\n', '; COL 3               seqpos\n', 
'; COL 4               alignpos\n', '; COL 5               align_bp\n', 
'; COL 6               seqpos_bp\n', '; ENTRY               seq1\n', 
'; ALIGNMENT_ID        n.a.\n', '; ALIGNMENT_LIST      seq1 seq2\n', 
'; FOLDALIGN_SCORE     929\n', '; GROUP               1\n', 
'; FILENAME            seq1.fasta\n', '; START_POSITION      2\n', 
'; END_POSITION        71\n', '; ALIGNMENT_SIZE      2\n', 
'; ALIGNMENT_LENGTH    70\n', '; SEQUENCE_LENGTH     76\n', 
'; PARAMETER           max_length=76\n', 
'; PARAMETER           max_diff=76\n', 
'; PARAMETER           min_loop=3\n', 
'; PARAMETER           score_matrix=<default>\n', 
'; PARAMETER           nobranching=<false>\n', 
'; PARAMETER           global=<false>\n', 
'; ----------\n', 
'N     G     1    1      14      0.90\n', 
'N     C     2    2      13      0.79\n', 
'N     A     3    3      12      0.87\n', 
'N     G     4    4       .      0.60\n', 
'N     A     5    5       .      0.34\n', 
'N     U     6    6       .      0.34\n', 
'N     U     7    7      11      0.98\n', 
'N     U     8    8       .      0.34\n', 
'N     A     9    9       .      0.56\n', 
'N     G    10    10      .      0.67\n', 
'N     A    11    11      7      0.78\n', 
'N     U    12    12      3      0.87\n', 
'N     G    13    13      2      0.87\n', 
'N     C    14    14      1      0.90\n', 
'; **********\n']
PFOLD = ['; generated by fasta2col\n', 
'; ============================================================\n', 
'; TYPE              TREE\n', '; COL 1             label\n', 
'; COL 2             number\n', '; COL 3             name\n', 
'; COL 4             uplen\n', '; COL 5             child\n', 
'; COL 6             brother\n', '; ENTRY             tree\n', 
'; root              1\n', '; ----------\n', 
' N     1         seq1 0.001000     .     .\n', 
'; **********\n', '; TYPE              RNA\n', '; COL 1             label\n', 
'; COL 2             residue\n', '; COL 3             seqpos\n', 
'; COL 4             alignpos\n', '; COL 5             align_bp\n', 
'; COL 6             certainty\n', '; ENTRY             seq1\n', 
'; ----------\n', 
'N     G     1    1      14      0.90\n', 
'N     C     2    2      13      0.79\n', 
'N     A     3    3      12      0.87\n', 
'N     G     4    4       .      0.60\n', 
'N     A     5    5       .      0.34\n', 
'N     U     6    6       .      0.34\n', 
'N     U     7    7      11      0.98\n', 
'N     U     8    8       .      0.34\n', 
'N     A     9    9       .      0.56\n', 
'N     G    10    10      .      0.67\n', 
'N     A    11    11      7      0.78\n', 
'N     U    12    12      3      0.87\n', 
'N     G    13    13      2      0.87\n', 
'N     C    14    14      1      0.90\n', 
'; **********\n'] 


PFOLD_tree = ['; generated by fasta2col\n', 
'; ============================================================\n', 
'; TYPE              TREE\n', '; COL 1             label\n', 
'; COL 2             number\n', '; COL 3             name\n', 
'; COL 4             uplen\n', '; COL 5             child\n', 
'; COL 6             brother\n', '; ENTRY             tree\n', 
'; root              1\n', '; ----------\n', 
' N     1         seq1 0.001000     .     .\n', '; **********\n']

if __name__ == '__main__':
    main()
