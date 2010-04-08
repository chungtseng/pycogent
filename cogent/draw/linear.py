#!/usr/bin/env python
from __future__ import division

import rlg2mpl
import matplotlib.colors
import matplotlib.ticker
import matplotlib.transforms
from matplotlib.text import Text
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
from matplotlib.collections import CircleCollection
from matplotlib.transforms import IdentityTransform

import copy
import logging
import warnings
from cogent.core.location import Map, Span, _norm_slice

__author__ = "Peter Maxwell"
__copyright__ = "Copyright 2007-2009, The Cogent Project"
__credits__ = ["Gavin Huttley", "Peter Maxwell", "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.5.0.dev"
__maintainer__ = "Peter Maxwell"
__email__ = "pm67nz@gmail.com"
__status__ = "Production"

log = logging.getLogger('cogent')

# map - a 1D space.  must support len() and in some cases [i]
# track - a panel within a sequence display holding annotations
# display - a collection of stacked tracks with a shared base sequence
# base - the map that provides the X scale
# annotation - an annotated disjoint location on a map
# span - a contiguous part of an annotation
# feature, code, variable, shade - types of anotation

# TODO: subtracks, spectra/width variables, strides, windows
#       broken ends, vscales, zero lines, sub-pixel features.
#       fuzzy ends.  more ids/qualifiers.

MAX_WIDTH = 72*8

class _Colors(object):
    """colors.white = to_rgb("white"), same as just using "white"
    except that this lookup also checks the color is valid"""   
    def __getattr__(self, attr):
        return matplotlib.colors.colorConverter.to_rgb(attr)
colors = _Colors()

def llen(label, fontSize=10):
    # placeholder for better length-of-label code
    return len(label) * fontSize
    
class TrackDefn(object):
    def __init__(self, tag, features, label=None):
        assert tag
        self.tag = tag
        self.label = label
        self.feature_types = features
    
    def makeTrack(self, features, **kw):
        """level=0, label=None, needs_border=False, max_y=None, height=None"""
        return Track(self.tag, features, **kw)
    
    def __iter__(self):
        return iter(self.feature_types)
    

class Track(object):
    def __init__(self, tag, features, level=0, label=None,
            needs_border=False, max_y=None, height=None):
        assert tag
        if label is None:
            label = tag
        self.tag = tag
        self.label = label
        assert isinstance(label, str), (tag, label)
        self.features = features
        self.height = max(height, max([f.height for f in self.features]))
        self.range = max_y or max(
            # xxx this works for zero-based only
            [getattr(f, 'value', None) for f in self.features]) or 0
        self.level = level
        self.needs_border = needs_border
    
    def getShapes(self, span, rotated, height, 
            yrange=None, done_border=False):
        shape_list = [feature.shape(height,
                yrange or self.range, rotated) for feature in self.features]
        if self.needs_border and not done_border:
            border = rlg2mpl.Group(
                    rlg2mpl.Line(span[0], 0, span[1], 0,
                            strokeWidth=.5, strokeColor=colors.black),
                    rlg2mpl.Line(span[0], height, span[1], height,
                            strokeWidth=.5, strokeColor=colors.black)
                    )
            shape_list = [border] + shape_list
        return shape_list
    
    def __repr__(self):
        return "Track(%(tag)s,%(label)s)" % vars(self)
    

class CompositeTrack(Track):
    """Overlayed tracks"""
    def __init__(self, tag, tracks, label=None):
        if label is None:
            labels = dict([(track.label, True)
                    for track in tracks if track.label]).keys()
            if len(labels) == 1:
                label = labels[0]
            else:
                label = ''
        self.tag = tag
        self.label = label
        self.tracks = tracks
        self.height = max([track.height for track in tracks])
        self.level = max([track.level for track in tracks])
        self.range = max([track.range for track in tracks])
    
    def getShapes(self, span, rotated, height, 
            yrange=None, done_border=False):
        if yrange is None:
            yrange = self.range
        shape_list = []
        for track in self.tracks:
            if track.needs_border and not done_border:
                border = rlg2mpl.Group(
                        rlg2mpl.Line(span[0], 0, span[1], 0,
                                strokeWidth=.5, strokeColor=colors.black),
                        rlg2mpl.Line(span[0], height, span[1], height,
                                strokeWidth=.5, strokeColor=colors.black)
                        )
                shape_list.append(border)
                done_border = True
            shape_list.extend(track.getShapes(span, rotated, height,
                    yrange=yrange, done_border=True))
        return shape_list
    

class Annotation(object):
    """A map, a style, and some values"""
    
    def __init__(self, map, *args, **kw):
        self.map = map
        self.values = self._make_values(*args, **kw)
    
    def _make_values(self, *args, **kw):
        # override for variables etc.
        return []
    
    def __repr__(self):
        return "%s at %s" % (type(self), getattr(self, 'map', '?'))
    
    # xxx styles do this.  what about maps/ others
    def shape(self, height, yrange, rotated):
        g = rlg2mpl.Group()
        posn = 0
        for span in self.map.spans:
            if not span.lost:
                g.add(self._item_shape(
                        span, self.values[posn:posn+span.length],
                        height, yrange, rotated))
            posn += span.length
        return g
    

class Code(Annotation):
    height = 20
    def _make_values(self, sequence, colours=None, font_properties=None):
        self.font_properties = font_properties
        self.colours = colours or {}
        for c in self.colours.keys():
            self.colours[c.upper()] = self.colours[c.lower()] = self.colours[c]
        return sequence
    
    def _item_shape(self, span, values, height, yrange, rotated):
        x_offset = span.Start+0.5
        y_offset = 10 # up a bit
        rot = 0
        if rotated: rot += 90
        if span.Reverse: rot+= 180
        g = rlg2mpl.Group()
        for (i,c) in enumerate(values):
            s = Text(
                x_offset+i, y_offset, c,
                color=self.colours.get(c, 'black'),
                ha='center', va='baseline', rotation=rot,
                font_properties=self.font_properties)
            g.add(s)
        return g 

class CodeDots(Code):
    def _item_shape(self, span, values, height, yrange, rotated):
        x_offset = span.Start+0.5
        cvalues = [self.colours.get(c, 'grey') for c in values]
        radius = 10 # points
        g = rlg2mpl.Group()
        a = CircleCollection([2*radius], 
            edgecolors=cvalues,
            facecolors=cvalues, 
            offsets=[(x_offset+i,radius) for i in range(len(values))],
            transOffset=g.combined_transform)
        g.add(a)
        a.set_transform(IdentityTransform())
        return g

class CodeLine(Annotation):
    height = 10
    def _item_shape(self, span, values, height, yrange, rotated):
        return rlg2mpl.Line(span.Start, height/2, span.End, height/2)    

class DensityGraph(Annotation):
    height = 20
    def _make_values(self, data):
        return data
    
    def _item_shape(self, span, values, height, yrange, rotated):
        #max_density = int(1.0/pixels_per_base) + 1
        #colours = [colors.linearlyInterpolatedColor(
        #        colors.white, colors.red, 0, height, i)
        #        for i in range(max_density)]
        mid = colors.linearlyInterpolatedColor(colors.pink, colors.red,
            0, 10, 5)
        
        g = rlg2mpl.Group()
        yscale = height / yrange
        last_x = -1
        ys = None
        for (p, q) in enumerate(values):
            if q is not None:
                g.add(rlg2mpl.Circle(
                    p, q*yscale, 0.5,
                    strokeWidth=0.0, strokeColor=colors.red,
                    fillColor=colors.red))
            
            #x = int(p * pixels_per_base)
            #y = int(q * yscale)
            #if x > last_x:
                #if ys:
                #    ys.sort()
                #    c = len(ys)
                    #g.add(rlg2mpl.Line(x, ys[0], x, ys[-1],
                    #    strokeColor=colors.pink))
                    #g.add(rlg2mpl.Line(x, ys[c/3], x, ys[2*c/3],
                    #    strokeColor=mid))
                    #g.add(rlg2mpl.Line(x, ys[c/2]-.5, x, ys[c/2]+.5,
                    #    strokeColor=colors.red))
            #    ys = []
            #    last_x = x
            #ys.append(y)
        return g
    

class Feature(Annotation):
    """An Annotation with a style and location rather than values"""
    def __init__(self, map, style, label=None, value=None):
        self.map = map
        self.style = style
        self.label = label
        self.value = value
        self.height = style.height
        #self.values = self._make_values(*args, **kw)
    
    def shape(self, height, yrange, rotated):
        return self.style(height, self.label, self.map, self.value, yrange, 
                rotated)
    

class _FeatureStyle(object):
    range_required = False
    def __init__(self, fill=True, color=colors.black, min_width=0.5,
            showLabel=False, height=1, thickness=0.6, closed=True,
            one_span=False, **kw):
        opts = {}
        if fill:
            opts['fillColor'] = color
            opts['strokeColor'] = None
            opts['strokeWidth'] = 0
        else:
            opts['fillColor'] = colors.white # otherwise matplotlib blue!
            opts['strokeColor'] = color
            opts['strokeWidth'] = 1
        self.filled = fill
        self.closed = closed or fill
        opts.update(kw)
        self.opts = opts
        self.min_width = min_width
        self.showLabel = showLabel
        self.height = height
        self.proportion_of_track = thickness
        self.one_span = one_span
    
    def __call__(self, height, label, map, value, yrange, rotated):
        #return self.FeatureClass(label, map)
        g = rlg2mpl.Group()
        last = first = None
        if self.range_required and not yrange:
            log.warning("'%s' graph values are all zero" % label)
            yrange = 1.0
        if map.useful and self.one_span:
            map = map.getCoveringSpan()
        for (i, span) in enumerate(map.spans):
            #if last is not None:
            #    g.add(rlg2mpl.Line(last, height, part.Start, height))
            if span.lost or (value is None and self.range_required):
                continue
            if span.Reverse:
                (start, end) = (span.End, span.Start)
                (tidy_start, tidy_end) = (span.tidy_end, span.tidy_start)
            else:
                (start, end) = (span.Start, span.End)
                (tidy_start, tidy_end) = (span.tidy_start, span.tidy_end)
            shape = self._item_shape(
                start, end,
                tidy_start, tidy_end, height, value, yrange, rotated, 
                last=i==len(map.spans)-1)
            g.add(shape)
            last = end
            if first is None:
                first = start
        if self.showLabel and label and last is not None and height > 7:
            font_height = 12 #self.label_font.get_size_in_points()
            text_width = llen(label, font_height)
            if (text_width < abs(first-last)):
                label_shape = Text(
                    (first+last)/2, height/2, label,
                    ha="center", va="center", 
                    rotation=[0,90][rotated],
                    #font_properties=self.label_font,
                    )
                g.add(label_shape)
            else:
                log.info("couldn't fit feature label '%s'" % label)
        return g

class _VariableThicknessFeatureStyle(_FeatureStyle):
    def _item_shape(self, start, end, tidy_start, tidy_end, height, value,
            yrange, rotated, last=False):
        if yrange:
            thickness = 1.0*value/yrange*height
        else:
            thickness = height*self.proportion_of_track
        return self._item_shape_scaled(start, end, tidy_start, tidy_end,
                height/2, max(2, thickness), rotated, last)
    
class Box(_VariableThicknessFeatureStyle):
    arrow = False
    blunt = False
    
    def _item_shape_scaled(self, start, end, tidy_start, tidy_end, middle,
            thickness, rotated, last):
        (top, bottom) = (middle+thickness/2, middle-thickness/2)
        kw = dict(min_width=self.min_width, pointy=False, closed=self.closed, 
            blunt=self.blunt, proportion_of_track=self.proportion_of_track)
        kw['rounded'] = tidy_start
        #kw['closed'] = self.closed or tidy_start
        end1 = rlg2mpl.End(start, end, bottom, top, **kw)
        kw['rounded'] = tidy_end
        #kw['closed'] = self.closed or tidy_end or self.filled
        kw['pointy'] = last and self.arrow
        end2 = rlg2mpl.End(end, start, top, bottom, **kw)
        path = end1 + end2
        return PathPatch(path, **rlg2mpl.line_options(**self.opts))   

class Arrow(Box):
    arrow = True
    blunt = False

class BluntArrow(Box):
    arrow = True
    blunt = True

class Diamond(_VariableThicknessFeatureStyle):
    """diamond"""
    def _item_shape_scaled(self, start, end, tidy_start, tidy_end, middle,
            thickness, rotated, last):
        x = (start+end)/2
        spread = max(abs(start-end), self.min_width) / 2
        return rlg2mpl.Polygon(
            [(x-spread, middle), (x, middle+thickness/2), (x+spread, middle), 
            (x, middle-thickness/2)], **self.opts)
    

class Line(_FeatureStyle):
    """For a line segment graph"""
    range_required = True
    def _item_shape(self, start, end, tidy_start, tidy_end, height, value,
            yrange, rotated, last=False):
        altitude = value * (height-1) / yrange
        #if self.orientation < 0:
        #    altitude = height - altitude
        return rlg2mpl.Line(start, altitude, end, altitude, **self.opts)
    

class Area(_FeatureStyle):
    """For a line segment graph"""
    range_required = True
    def _item_shape(self, start, end, tidy_start, tidy_end, height, value,
            yrange, rotated, last=False):
        altitude = value * (height-1) / yrange
        #if self.orientation < 0:
        #    altitude = height - altitude
        if end < start:
            start, end = end, start
            tidy_start, tidy_end = tidy_end, tidy_start
        return rlg2mpl.Rect(start, 0, end-start, altitude, **self.opts)
    

class DisplayPolicy(object):
    def _makeFeatureStyles(self):
        return {
            #gene structure
            'misc_RNA': Box(True, colors.lightcyan),
            'precursor_RNA': Box(True, colors.lightcyan),
            'prim_transcript': Box(True, colors.lightcyan),
            "3'clip": Box(True, colors.lightcyan),
            "5'clip": Box(True, colors.lightcyan),
            'mRNA': Box(True, colors.cyan),
            'exon': Box(True, colors.cyan),
            'intron': Box(False, colors.cyan, closed = False),
            "3'UTR": Box(True, colors.cyan),
            "5'UTR": Box(True, colors.cyan),
            'CDS': Box(True, colors.blue),
            'mat_peptide': Box(True, colors.blue),
            'sig_peptide': Box(True, colors.navy),
            'transit_peptide': Box(True, colors.navy),
            'polyA_signal': Box(True, colors.lightgreen),
            'polyA_site': Diamond(True, colors.lightgreen),
            'gene': BluntArrow(False, colors.blue,
                    showLabel=True, closed = False),
            'operon': BluntArrow(False, colors.royalblue,
                    showLabel=True, closed = False),
            #regulation
            'attenuator': Box(False, colors.red),
            'enhancer': Box(True, colors.green),
            'CAAT_signal': Diamond(True, colors.blue),
            'TATA_signal': Diamond(True, colors.teal),
            'promoter': Box(False, colors.seagreen),
            'GC_signal': Box(True, colors.purple),
            'protein_bind': Box(True, colors.orange),
            'misc_binding': Box(False, colors.black),
            '-10_signal': Diamond(True, colors.blue),
            '-35_signal': Diamond(True, colors.teal),
            'terminator': Diamond(True, colors.red),
            'misc_signal': Box(False, colors.maroon),
            'rep_origin': Box(True, colors.linen),
            'RBS': Diamond(True, colors.navy),
            #repeats
            'repeat_region': Box(True, colors.brown),
            'repeat_unit': Arrow(True, colors.brown),
            'LTR': Box(False, colors.black),
            'satellite': Box(False, colors.brown),
            'stem_loop': Box(False, colors.dimgray),
            'misc_structure': Box(False, colors.darkslategray),
            #rna genes
            'rRNA': Arrow(False, colors.darkorchid, showLabel=True),
            'scRNA': Arrow(False, colors.darkslateblue, showLabel=True),
            'snRNA': Arrow(False, colors.darkviolet, showLabel=True),
            'snoRNA': Arrow(False, colors.darkviolet, showLabel=True),
            'tRNA': Arrow(False, colors.darkturquoise, showLabel=True),
            #sequence
            'source': Box(False, colors.black, showLabel=True),
            'misc_recomb': Box(False, colors.black, showLabel=True),
            'variation': Diamond(True, colors.violet, showLabel=True),
            'domain': Box(False, colors.darkorange, showLabel=True),
            'bluediamond': Diamond(True, colors.blue),
            'reddiamond': Diamond(True, colors.red),
            'misc_feature': Box(True, colors.darkorange, showLabel=True),
            'old_sequence': Box(False, colors.darkslategray),
            'unsure': Diamond(False, colors.crimson, min_width=2,),
            'misc_difference': Diamond(False, colors.darkorange),
            'conflict': Box(False, colors.darkorange),
            'modified_base': Diamond(True, colors.black),
            'primer_bind': Arrow(False, colors.green, showLabel=True),
            'STS': Box(False, colors.black),
            'gap': Box(True, colors.gray),
            #graphs
            'blueline': Line(False, colors.blue),
            'redline': Line(False, colors.red),
            #other
            ##immune system specific
            #'C_region': Diamond(True, colors.mediumblue),
            #'N_region': Box(False, colors.linen),
            #'S_region': Box(False, colors.linen),
            #'V_region': Box(False, colors.linen),
            #'D_segment': Diamond(True, colors.mediumpurple),
            #'J_segment': Box(False, colors.linen),
            #'V_segment': Box(False, colors.linen),
            #'iDNA': Box(False, colors.grey),
            ##Mitocondria specific
            #'D-loop': Diamond(True, colors.linen),
            ##Bacterial element specific
            #'oriT': Box(False, colors.linen),
        }
    
    def _makeTrackDefns(self):
        return [TrackDefn(*args) for args in [
            ('Gene Structure',[
                'misc_RNA',
                'precursor_RNA',
                'prim_transcript',
                "3'clip",
                "5'clip",
                'mRNA',
                'exon',
                'intron',
                "3'UTR",
                "5'UTR",
                'CDS',
                'mat_peptide',
                'sig_peptide',
                'transit_peptide',
                'polyA_signal',
                'polyA_site',
                'gene',
                'operon',
                ]),
            ('Regulation',[
                'attenuator',
                'enhancer',
                'CAAT_signal',
                'TATA_signal',
                'promoter',
                'GC_signal',
                'protein_bind',
                'misc_binding',
                '-10_signal',
                '-35_signal',
                'terminator',
                'misc_signal',
                'rep_origin',
                'RBS',
                ]),
            ('Repeats',[
                'repeat_region',
                'repeat_unit',
                'LTR',
                'satellite',
                'stem_loop',
                'misc_structure',
                ]),
            ('Rna Genes',[
                'rRNA',
                'scRNA',
                'snRNA',
                'snoRNA',
                'tRNA',
                ]),
            ('Sequence',[
                'source',
                'misc_recomb',
                'domain',
                'variation',
                'bluediamond',
                'reddiamond',
                'misc_feature',
                'old_sequence',
                'unsure',
                'misc_difference',
                'conflict',
                'modified_base',
                'primer_bind',
                'STS',
                'gap',
                ]),
            ('Graphs',[
                'blueline',
                'redline',
                ]),
        ]]
    
    _default_ignored_features =    ['C_region','N_region','S_region','V_region',
        'D_segment','J_segment','V_segment','iDNA','D-loop','oriT',]
    _default_keep_unexpected_tracks = True
    
    dont_merge = []
    show_text = None # auto
    colour_sequences = False
    seqname = ''
    rowlen = None
    recursive = True
    
    def __init__(self,
            min_feature_height = 20,
            min_graph_height = None,
            ignored_features=None,
            keep_unexpected_tracks=None,
            **kw):
        
        self.seq_font = FontProperties(size=10)
        #self.label_font = FontProperties()

        if min_graph_height is None:
            min_graph_height = min_feature_height * 2
        
        feature_styles = self._makeFeatureStyles()
        # yuk
        for style in feature_styles.values():
            if style.range_required:
                style.height = max(style.height, min_graph_height)
            else:
                style.height = max(style.height, min_feature_height)
        
        self._track_defns = self._makeTrackDefns()
        
        if ignored_features is None:
            ignored_features = self._default_ignored_features
        self._ignored_features = ignored_features
        if keep_unexpected_tracks is None:
            keep_unexpected_tracks = self._default_keep_unexpected_tracks
        self.keep_unexpected_tracks = keep_unexpected_tracks
        
        if not hasattr(self, '_track_map'):
            self._track_map = {}
            for track_defn in self._track_defns:
                for (level, feature_tag) in enumerate(track_defn):
                    feature_style = feature_styles[feature_tag]
                    self._track_map[feature_tag] = (
                            track_defn, level, feature_style)
            for ft in self._ignored_features:
                self._track_map[ft] = (None, 0, None)
            for ft in feature_styles:
                if ft not in self._track_map:
                    self._track_map[ft] = (None, level, feature_style)
        self.map = None
        self.depth = 0
        self.orientation = -1
        self.show_code = True
        self._logged_drops = []
        
        self._setattrs(**kw)
    
    def _setattrs(self, **kw):                 
        for (n,v) in kw.items():
            if not hasattr(self, n):
                warnings.warn('surprising kwarg "%s"' % n, stacklevel=3)
            if n.endswith('font'):
                assert isinstance(kw[n], FontProperties)
            setattr(self, n, v)
    
    def copy(self, **kw):
        new = copy.copy(self)
        new._setattrs(**kw)
        return new
    
    def at(self, map):
        if map is None:
            return self
        else:
            return self.copy(map=self.map[map], depth=self.depth+1)
    
    def mergeTracks(self, orig_tracks, keep_unexpected=None):
        # merge tracks with same names
        # order features within a track by level  # xxx remerge
        tracks = {}
        orig_track_tags = []
        for track in orig_tracks:
            if not track.tag in tracks:
                tracks[track.tag] = {}
                orig_track_tags.append(track.tag) # ordered list
            if not track.level in tracks[track.tag]:
                tracks[track.tag][track.level] = []
            tracks[track.tag][track.level].append(track)
        
        track_order = [track.tag for track in self._track_defns
                if track.tag in tracks]
        unexpected = [tag for tag in orig_track_tags if tag not in track_order]
        if keep_unexpected is None:
            keep_unexpected = self.keep_unexpected_tracks
        if keep_unexpected:
            track_order += unexpected
        elif unexpected:
            log.warning('dropped tracks ' + ','.join(unexpected), stacklevel=2)
        
        sorted_tracks = []
        for track_tag in track_order:
            annots = []
            levels = tracks[track_tag].keys()
            levels.sort()
            for level in levels:
                annots.extend(tracks[track_tag][level])
            if len(annots)> 1 and track_tag not in self.dont_merge:
                sorted_tracks.append(CompositeTrack(track_tag, annots))
            else:
                sorted_tracks.extend(annots)
        return sorted_tracks
    
    def tracksForAlignment(self, alignment):
        annot_tracks = alignment.getAnnotationTracks(self)
        if self.recursive:
            seq_tracks = alignment.getChildTracks(self)
        else:
            seq_tracks = []
        annot_tracks = self.mergeTracks(annot_tracks)
        return seq_tracks + annot_tracks
    
    def tracksForSequence(self, sequence=None):
        result = []
        length = None
        if length is None and sequence is not None:
            length = len(sequence)
        
        label = getattr(self, 'seqname', '')
        
        if self.show_code and sequence is not None:
            # this should be based on resolution, not rowlen, but that's all
            # we have at this point
            if self.colour_sequences:
                colours = sequence.getColourScheme(colors)
            else:
                colours = {}
            show_text = self.show_text
            if show_text is None:
                show_text = self.rowlen <= 100
            if show_text and self.rowlen <= 200:
                feature = Code(self.map, str(sequence), colours=colours,
                    font_properties=self.seq_font)
            elif colours:
                feature = CodeDots(self.map, sequence, colours=colours)
            else:
                feature = CodeLine(self.map, sequence)
            result.append(Track('seq', [feature], level=2, label=label))
        else:
            pass
            # show label somewhere
        
        annot_tracks = sequence.getAnnotationTracks(self)
        annot_tracks = self.mergeTracks(annot_tracks)
        
        return annot_tracks + result
    
    def getStyleDefnForFeature(self, feature):
        if feature.type in self._track_map:
            (track_defn, level, style) = self._track_map[feature.type]
        elif self.keep_unexpected_tracks:
            (track_defn, level, style) = self._track_map['misc_feature']
        else:
            if feature.type not in self._logged_drops:
                log.warning('dropped feature ' + repr(feature.type))
                self._logged_drops.append(feature.type)
            return (None, None, None)
        
        if track_defn is None:
            log.info('dropped feature ' + repr(feature.type))
            return (None, None, None)
        else:
            track_tag = track_defn.tag or feature.type
        return (track_tag, style, level)
    
    def tracksForFeature(self, feature):
        (track_tag, style, level) = self.getStyleDefnForFeature(feature)
        if style is None:
            return []
        annot_tracks = feature.getAnnotationTracks(self)
        return annot_tracks + [Track(track_tag,
                [Feature(self.map, style, feature.Name)], level=level)]
    
    def tracksForVariable(self, variable):
        (track_tag, style, level) = self.getStyleDefnForFeature(variable)
        if style is None:
            return []
        segments = []
        max_y = 0.0
        for ((x1, x2), y) in variable.xxy_list:
            map = self.map[x1:x2]
            segments.append(Feature(map, style, variable.Name, value=y))
            if type(y) is tuple: y = max(y)
            if y > max_y: max_y = y
        return [Track(track_tag, segments, max_y=max_y, needs_border=True,
                label=variable.Name, level=level)]
    

class Display(rlg2mpl.Drawable):
    """Holds a list of tracks and displays them all aligned
    
    base: A sequence, alignment, or anything else offering .getTracks(policy)
    policy: A DisplayPolicy subclass.
    pad: Gap between tracks in points.
    
    Other keyword arguments are used to modify the DisplayPolicy: 
    show_text: Represent sequences as characters.  Slow.
    colour_sequences = Colour code sequences if MolType allows.
    rowlen: wrap at this many characters per line.
    recursive: include the sequences of the alignment.
    min_feature_height: minimum feature symbol height in points.
    min_graph_height: minimum height of any graphed features in points.
    ignored_features: list of feature type tags to leave out.
    keep_unexpected_tracks: show features not assigned to a track by the policy.
"""
    
    def __init__(self, base, policy=DisplayPolicy, _policy=None, pad=1,
            yrange=None, **kw):
        self.pad = pad
        self.base = base
        self.yrange = yrange
        assert len(base) > 0, len(base)
        
        if _policy is None:
            policy = policy(**kw).copy(
                map=Map([(0, len(base))], parent_length=len(base)),
                depth=0, 
                rowlen=len(base))
        else:
            policy = _policy
        self.policy = policy
        self.smap=Map([(0, len(base))], parent_length=len(base))

        self._calc_tracks()
    
    def __len__(self):
        return len(self.smap.inverse())
    
    def _calc_tracks(self):
        y = 0
        self._tracks = []
        for p in self.base.getTracks(self.policy)[::-1]:
            if not isinstance(p, Track):
                if not isinstance(p, list):
                    p = [p]
                p = Track('', p)
            y2 = y + p.height + self.pad
            self._tracks.append((y+self.pad/2, (y+y2)/2, p))
            y = y2
        self.height = y
        
        if self.yrange is None:
            self.yrange = {}
            for (y, ym, p) in self._tracks:
                self.yrange[p.tag] = max(self.yrange.get(p.tag, 0), p.range)
        
    def copy(self, **kw):
        new = copy.copy(self)
        new.policy = self.policy.copy(**kw)
        new._calc_tracks()
        return new
    
    def __getitem__(self, slice):
        c = copy.copy(self)
        c.smap = self.smap.inverse()[slice].inverse()
        return c
        
    def makeArtist(self, vertical=False):
        g = rlg2mpl.Group()
        for (y, ym, p) in self._tracks:
            smap = self.smap.inverse()
            for s in p.getShapes(
                    span=(smap.Start, smap.End),
                    rotated=vertical,
                    height=float(p.height), 
                    yrange=self.yrange[p.tag]):
                trans = matplotlib.transforms.Affine2D()
                trans.translate(0, y)
                s.set_transform(s.get_transform() + trans)
                g.add(s)
        if vertical:
            g.rotate(90)
            g.scale(-1.0, 1.0)
        return g
    
    def asAxes(self, fig, posn, labeled=True, **kw):
        ax = fig.add_axes(posn)
        self.applyScaleToAxes(ax, labeled=labeled, **kw)
        group = self.makeArtist(**kw)
        ax.add_artist(group)
        return ax
        
    def applyScaleToAxes(self, ax, labeled=True, vertical=False):
        (seqaxis, trackaxis) = [ax.xaxis, ax.yaxis]
        if vertical:
            (seqaxis, trackaxis) = (trackaxis, seqaxis) 

        if not labeled:
            trackaxis.set_ticks([])
        else:
            track_positions = []
            track_labels = []
            for (y, ym, p) in self._tracks:
                if p.height > 8:
                    track_labels.append(p.label)
                    track_positions.append(ym)
            trackaxis.set_ticks(track_positions)
            trackaxis.set_ticklabels(track_labels)
            if vertical:
                for tick in trackaxis.get_major_ticks():
                    tick.label1.set_rotation('vertical')
                    tick.label2.set_rotation('vertical')
            
        seqaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x,pos:str(int(x))))
        
        smap = self.smap.inverse()
        seq_lim = (smap.Start, smap.End)
        if vertical:
            ax.set_ylim(*seq_lim)
            ax.set_xlim(0, self.height)
        else:
            ax.set_xlim(*seq_lim)
            ax.set_ylim(0, self.height)
    
    def figureLayout(self, labeled=True, vertical=False, width=None, 
            height=None, left=None, **kw):

        if left is None:
            if labeled:
                left = max(len(p.label) for (y, ym, p) in self._tracks)
                left *= 12/72 * .5 # guess mixed chars, 12pt, inaccurate!
            else:
                left = 0
            
        height = height or self.height/72
        
        useful_width = len(self)*16/72 # ie bigish font, wide chars
        
        fkw = dict(leftovers=True, width=width, height=height, left=left, 
                useful_width=useful_width, **kw)  
        (w,h),posn,kw = rlg2mpl.figureLayout(**fkw)
        
        #points_per_base = w * posn[3] / len(self)
        if vertical:
            (w, h) = (h, w)
            posn[0:2] = reversed(posn[0:2])
            posn[2:4] = reversed(posn[2:4])
        return (w, h), posn, kw
    
    def makeFigure(self, width=None, height=None, rowlen=None, **kw):
        if rowlen:
            rows = [self[i:i+rowlen] for i in range(0, len(self), rowlen)]
        else:
            rows = [self]
            rowlen = len(self)
        kw.update(width=width, height=height)
        ((width, height), (x, y, w, h), kw) = self.figureLayout(**kw)
        N = len(rows)
        # since scales go below and titles go above, each row
        # gets the bottom margin, but not the top margin.
        vzoom = 1 + (y+h) * (N-1)
        fig = self._makeFigure(width, height * vzoom)
        for (i, row) in enumerate(rows):
            i = len(rows) - i - 1
            posn = [x, (y+i*(y+h))/vzoom, w*len(row)/rowlen, h/vzoom]
            row.asAxes(fig, posn, **kw)
        return fig
    
        
        