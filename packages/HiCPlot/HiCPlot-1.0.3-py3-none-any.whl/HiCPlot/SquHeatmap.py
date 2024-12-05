#!/usr/bin/env python
import argparse
import os
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyBigWig
import pyranges as pr
import numpy as np
import matplotlib.pyplot as plt
import cooler
from matplotlib.ticker import EngFormatter
import itertools
import sys
import scipy.sparse
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors

dir = os.path.dirname(os.path.abspath(__file__))
version_py = os.path.join(dir, "_version.py")
exec(open(version_py).read())

def plot_genes(ax, gtf_file, region, color='blue', track_height=1):
    spacing_factor = 1.5
    chrom, start, end = region
    # Load the GTF file using pyranges
    gtf = pr.read_gtf(gtf_file)
    # Filter relevant region and keep only the longest isoform for each gene
    region_genes = gtf[(gtf.Chromosome == chrom) & (gtf.Start < end) & (gtf.End > start)]
    
    if region_genes.empty:
        print("No genes found in the specified region.")
        ax.axis('off')  # Hide the axis if no genes are present
        return
    
    # Select the longest isoform for each gene
    longest_isoforms = region_genes.df.loc[region_genes.df.groupby('gene_id')['End'].idxmax()]
    
    y_offset = 0
    y_step = track_height * spacing_factor  # Adjusted vertical step for tighter spacing
    plotted_genes = []
    
    # Iterate over each gene and plot
    for _, gene in longest_isoforms.iterrows():
        # Determine y_offset to avoid overlap with previously plotted genes
        for plotted_gene in plotted_genes:
            if not (gene['End'] < plotted_gene['Start'] or gene['Start'] > plotted_gene['End']):
                y_offset = max(y_offset, plotted_gene['y_offset'] + y_step)
        
        # Plot gene line with increased linewidth for better visibility
        ax.plot([gene['Start'], gene['End']], [y_offset, y_offset], color=color, lw=1)
        
        # Plot exons as larger rectangles for increased height
        exons = region_genes.df[
            (region_genes.df['gene_id'] == gene['gene_id']) & (region_genes.df['Feature'] == 'exon')
        ]
        for _, exon in exons.iterrows():
            ax.add_patch(
                plt.Rectangle(
                    (exon['Start'], y_offset - 0.3 * track_height),  # Lowered to center the exon vertically
                    exon['End'] - exon['Start'],
                    0.6 * track_height,  # Increased height of exon rectangles
                    color=color
                )
            )
        
        # Add gene name at the center of the gene, adjusted vertically
        ax.text(
            (gene['Start'] + gene['End']) / 2,
            y_offset + 0.4 * track_height,  # Adjusted position for better alignment
            gene['gene_name'],
            fontsize=8,  # Increased font size for readability
            ha='center',
            va='bottom'  # Align text below the exon
        )
        
        # Track the plotted gene's range and offset
        plotted_genes.append({'Start': gene['Start'], 'End': gene['End'], 'y_offset': y_offset})
    
    # Set y-axis limits based on the final y_offset
    ax.set_ylim(-track_height, y_offset + track_height * 2)
    ax.set_ylabel('Genes')
    ax.set_yticks([])  # Hide y-ticks for a cleaner look
    ax.set_xlim(start, end)
    ax.set_xlabel("Position (Mb)")
    
    # Format x-axis to display positions in megabases (Mb)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x / 1e6:.2f}'))

def read_bigwig(file_path, region):
    """Read BigWig or bedGraph file and return positions and values."""
    chrom, start, end = region
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.bw', '.bigwig']:
        # Open the BigWig file
        bw = pyBigWig.open(file_path)
        # Fetch values from the region
        values = bw.values(chrom, start, end, numpy=True)
        bw.close()  # Close the BigWig file
        positions = np.linspace(start, end, len(values))
    elif file_extension in ['.bedgraph', '.bg']:
        # Read the bedGraph file using pandas
        # Assuming bedGraph files have columns: chrom, start, end, value
        bedgraph_df = pd.read_csv(file_path, sep='\t', header=None, comment='#', 
                                  names=['chrom', 'start', 'end', 'value'])
        # Filter the data for the specified region
        region_data = bedgraph_df[
            (bedgraph_df['chrom'] == chrom) &
            (bedgraph_df['end'] > start) &
            (bedgraph_df['start'] < end)
        ]
        if region_data.empty:
            return None, None
        # Prepare the positions and values
        positions = np.sort(np.unique(np.concatenate([region_data['start'].values, 
                                                      region_data['end'].values])))
        values = np.zeros_like(positions, dtype=float)
        for idx in range(len(region_data)):
            s = region_data.iloc[idx]['start']
            e = region_data.iloc[idx]['end']
            v = region_data.iloc[idx]['value']
            mask = (positions >= s) & (positions <= e)
            values[mask] = v
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are BigWig (.bw) and bedGraph (.bedgraph, .bg).")
    return positions, values

def get_track_min_max(bigwig_files_sample1, bigwig_files_sample2, layoutid, region, normalization_method):
    if layoutid == "horizontal":
        max_num_tracks = max(len(bigwig_files_sample1), len(bigwig_files_sample2))
    elif layoutid == "vertical":
        max_num_tracks = len(bigwig_files_sample1) + len(bigwig_files_sample2)
    else:
        raise ValueError("Invalid layoutid. Use 'horizontal' or 'vertical'.")

    min_max_list = []

    for i in range(max_num_tracks):
        min_val = np.inf
        max_val = -np.inf

        if layoutid == "horizontal":
            # In horizontal layout, track i corresponds to sample1[i] and sample2[i]
            # Sample 1
            if i < len(bigwig_files_sample1):
                positions, values = read_bigwig(bigwig_files_sample1[i], region)
                if values is not None and len(values) > 0:
                    current_min = np.nanmin(values)
                    current_max = np.nanmax(values)
                    min_val = min(min_val, current_min)
                    max_val = max(max_val, current_max)

            # Sample 2
            if i < len(bigwig_files_sample2):
                positions, values = read_bigwig(bigwig_files_sample2[i], region)
                if values is not None and len(values) > 0:
                    current_min = np.nanmin(values)
                    current_max = np.nanmax(values)
                    min_val = min(min_val, current_min)
                    max_val = max(max_val, current_max)

        elif layoutid == "vertical":
            # In vertical layout, first all sample1 tracks, then sample2 tracks
            if i < len(bigwig_files_sample1):
                # Sample 1 tracks
                positions, values = read_bigwig(bigwig_files_sample1[i], region)
                if values is not None and len(values) > 0:
                    current_min = np.nanmin(values)
                    current_max = np.nanmax(values)
                    min_val = min(min_val, current_min)
                    max_val = max(max_val, current_max)
            else:
                # Sample 2 tracks
                sample2_idx = i - len(bigwig_files_sample1)
                if sample2_idx < len(bigwig_files_sample2):
                    positions, values = read_bigwig(bigwig_files_sample2[sample2_idx], region)
                    if values is not None and len(values) > 0:
                        current_min = np.nanmin(values)
                        current_max = np.nanmax(values)
                        min_val = min(min_val, current_min)
                        max_val = max(max_val, current_max)

        # Handle cases where no data was found for the track
        if min_val == np.inf and max_val == -np.inf:
            min_max_list.append((None, None))
        else:
            min_max_list.append((min_val, max_val))

    return min_max_list

def plot_seq(ax, file_path, region, color='blue', y_min=None, y_max=None):
    """Plot RNA-seq/ChIP-seq expression from BigWig or bedGraph file on given axis."""
    chrom, start, end = region
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.bw', '.bigwig']:
        # Open the BigWig file
        bw = pyBigWig.open(file_path)
        # Fetch values from the region
        values = bw.values(chrom, start, end, numpy=True)
        bw.close()  # Close the BigWig file
        positions = np.linspace(start, end, len(values))
    elif file_extension in ['.bedgraph', '.bg']:
        # Read the bedGraph file using pandas
        # Assuming bedGraph files have columns: chrom, start, end, value
        bedgraph_df = pd.read_csv(file_path, sep='\t', header=None, comment='#', 
                                  names=['chrom', 'start', 'end', 'value'])
        # Filter the data for the specified region
        region_data = bedgraph_df[
            (bedgraph_df['chrom'] == chrom) &
            (bedgraph_df['end'] > start) &
            (bedgraph_df['start'] < end)
        ]
        if region_data.empty:
            print(f"No data found in the specified region ({chrom}:{start}-{end}) in {file_path}")
            ax.axis('off')  # Hide the axis if no data
            return
        # Prepare the positions and values
        positions = np.sort(np.unique(np.concatenate([region_data['start'].values, 
                                                      region_data['end'].values])))
        values = np.zeros_like(positions, dtype=float)
        for idx in range(len(region_data)):
            s = region_data.iloc[idx]['start']
            e = region_data.iloc[idx]['end']
            v = region_data.iloc[idx]['value']
            mask = (positions >= s) & (positions <= e)
            values[mask] = v
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are BigWig (.bw) and bedGraph (.bedgraph, .bg).")
    
    # Plot the RNA-seq/ChIP-seq expression as a filled line plot
    ax.fill_between(positions, values, color=color, alpha=0.7)
    ax.set_xlim(start, end)
    if y_min is not None and y_max is not None:
        ax.set_ylim(y_min, y_max)
    elif y_max is not None:
        ax.set_ylim(0, y_max)
    elif y_min is not None:
        ax.set_ylim(y_min, 1)  # Default upper limit if only y_min is provided
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x / 1e6:.2f}'))

def plot_bed(ax, bed_file, region, color='green', linewidth=1):
    """Plot BED file annotations on the given axis."""
    chrom, start, end = region
    # Read the BED file
    bed_df = pd.read_csv(bed_file, sep='\t', header=None, comment='#', 
                         names=['chrom', 'start', 'end'] + [f'col{i}' for i in range(4, 10)])
    # Filter for the region and chromosome
    region_bed = bed_df[
        (bed_df['chrom'] == chrom) &
        (bed_df['end'] > start) &
        (bed_df['start'] < end)
    ]
    if region_bed.empty:
        print(f"No BED entries found in the specified region ({chrom}:{start}-{end}) in {bed_file}")
        ax.axis('off')
        return
    
    for _, entry in region_bed.iterrows():
        bed_start = max(entry['start'], start)
        bed_end = min(entry['end'], end)
        ax.add_patch(
            plt.Rectangle(
                (bed_start, 0.1),  # y-coordinate fixed
                bed_end - bed_start,
                0.8,  # Height of the BED feature
                color=color,
                linewidth=linewidth
            )
        )
    
    ax.set_xlim(start, end)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Hide axis for BED tracks

def pcolormesh_square(ax, matrix, start, end, cmap='bwr', vmin=None, vmax=None, *args, **kwargs):
    """
    Plot the difference matrix as a heatmap on the given axis.
    """
    if matrix is None:
        return None
    im = ax.imshow(matrix, aspect='auto', origin='upper',
                   extent=[start, end, end, start], cmap=cmap, vmin=vmin, vmax=vmax, *args, **kwargs)
    return im

def plot_heatmaps(cooler_file1, sampleid1,
                 bigwig_files_sample1, bigwig_labels_sample1, colors_sample1,
                 bed_files_sample1, bed_labels_sample1, colors_bed_sample1,
                 gtf_file, resolution=10000,
                 start=10500000, end=13200000, chrid="chr2",
                 cmap='autumn_r', vmin=None, vmax=None,
                 output_file='comparison_heatmap.pdf', layout='horizontal',
                 cooler_file2=None, sampleid2=None,
                 bigwig_files_sample2=[], bigwig_labels_sample2=[], colors_sample2=[],
                 bed_files_sample2=[], bed_labels_sample2=[], colors_bed_sample2=[],
                 track_size=5, track_spacing=0.5, normalization_method='raw'):
    plt.rcParams['font.size'] = 8
    # Set parameters
    region = (chrid, start, end)
    
    # Load cooler data
    clr1 = cooler.Cooler(f'{cooler_file1}::resolutions/{resolution}')
    data1 = clr1.matrix(balance=True).fetch(region)
    
    # Load sample2 data if provided
    single_sample = cooler_file2 is None
    if not single_sample:
        clr2 = cooler.Cooler(f'{cooler_file2}::resolutions/{resolution}')
        data2 = clr2.matrix(balance=True).fetch(region)
    
    # Apply normalization to Hi-C matrices
    if normalization_method == 'raw':
        normalized_data1 = data1
        normalized_data2 = data2 if not single_sample else None
    elif normalization_method == 'log2':
        normalized_data1 = np.log2(np.maximum(data1, 1e-10))
        if not single_sample:
            normalized_data2 = np.log2(np.maximum(data2, 1e-10))
    elif normalization_method == 'log2_add1':
        normalized_data1 = np.log2(data1 + 1)
        if not single_sample:
            normalized_data2 = np.log2(data2 + 1)
    elif normalization_method == 'log':
        normalized_data1 = np.log(np.maximum(data1, 1e-10))
        if not single_sample:
            normalized_data2 = np.log(np.maximum(data2, 1e-10))
    elif normalization_method == 'log_add1':
        normalized_data1 = np.log(data1 + 1)
        if not single_sample:
            normalized_data2 = np.log(data2 + 1)
    else:
        raise ValueError(f"Unsupported normalization method: {normalization_method}")
    
    # Determine vmin and vmax if not provided
    if vmin is None and vmax is None:
        if single_sample:
            global_min = np.nanmin(normalized_data1)
            global_max = np.nanmax(normalized_data1)
        else:
            global_min = min(np.nanmin(normalized_data1), np.nanmin(normalized_data2))
            global_max = max(np.nanmax(normalized_data1), np.nanmax(normalized_data2))
        vmin = global_min
        vmax = global_max
    elif vmin is None:
        if normalization_method.startswith('log'):
            vmin = np.nanmin(normalized_data1)
        else:
            vmin = 0  # For raw data
    elif vmax is None:
        if normalization_method.startswith('log'):
            vmax = np.nanmax(normalized_data1)
        else:
            vmax = np.nanmax(normalized_data1)
    
    # Define normalization for color mapping
    #norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    
    bp_formatter = EngFormatter()

    def format_ticks(ax, x=True, y=True, rotate=True):
        def format_million(x, pos):
            return f'{x / 1e6:.2f}'
        if y:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(format_million))
        if x:
            ax.xaxis.set_major_formatter(plt.FuncFormatter(format_million))
            ax.xaxis.tick_bottom()
        if rotate:
            ax.tick_params(axis='x', rotation=45)

    # Set up the figure based on layout
    if layout == 'horizontal':
        ncols = 1 if single_sample else 2
        num_genes = 1 if gtf_file else 0
        # Calculate the number of BigWig and BED tracks per sample
        max_num_bigwig_files = max(len(bigwig_files_sample1), len(bigwig_files_sample2)) if not single_sample else len(bigwig_files_sample1)
        max_num_bed_files = max(len(bed_files_sample1), len(bed_files_sample2)) if not single_sample else len(bed_files_sample1)
        max_bigwig_bed_tracks = max(max_num_bigwig_files, max_num_bed_files) if not single_sample else max(len(bigwig_files_sample1), len(bed_files_sample1))
        
        # Total rows:
        # Row0: Heatmaps
        # Row1: Colorbar
        # Rows2 to (2 + max_bigwig_bed_tracks -1): BigWig and BED tracks
        # Row after Tracks: Genes
        num_rows = 2 + max_bigwig_bed_tracks + num_genes
        
        # Define height ratios: [Heatmaps, Colorbar, BigWig/BED tracks..., Genes]
        small_colorbar_height = 0.1  # Reduced height
        track_height_ratio = 0.5  # Adjust as needed for BigWig/BED tracks
        height_ratios = [1, small_colorbar_height] + [track_height_ratio] * max_bigwig_bed_tracks + [track_height_ratio * num_genes]
        
        # Calculate scaling factor to make the main heatmap row height equal to track_size (in inches)
        per_unit = track_size / height_ratios[0]  # track_size=5 inches / 1 = 5 inches per unit
        
        # Calculate the figure height based on all height ratios and per_unit
        figsize_height = sum(hr * per_unit for hr in height_ratios) + (num_rows -1)*track_spacing
        figsize_width = ncols * track_size + (ncols -1)*track_spacing
        
        # Initialize GridSpec with adjusted height ratios
        gs = gridspec.GridSpec(num_rows, ncols, height_ratios=height_ratios, hspace=0.3, wspace=0.3)
        
        # Create figure with calculated size
        f = plt.figure(figsize=(figsize_width, figsize_height))
        
        # Plot first heatmap
        ax1 = f.add_subplot(gs[0, 0])
        im1 = pcolormesh_square(ax1, normalized_data1, region[1], region[2], cmap=cmap, vmin=vmin, vmax=vmax)
        format_ticks(ax1, rotate=False)
        ax1.set_title(sampleid1, fontsize=10)
        ax1.set_aspect('equal')  # Ensure square aspect
        ax1.set_ylim(end, start)
        ax1.set_xlim(start, end)
        
        # Create a colorbar for Heatmap 1 in GridSpec row 1
        cax1 = f.add_subplot(gs[1, 0])
        cbar1 = plt.colorbar(im1, cax=cax1, orientation='horizontal')
        cbar1.ax.tick_params(labelsize=8)
        cax1.xaxis.set_label_position('bottom')
        cax1.xaxis.set_ticks_position('bottom')
        cbar1.set_label(normalization_method, labelpad=3)
        cbar1.ax.xaxis.set_label_position('top')
        # Plot second heatmap if sample2 data is provided
        if not single_sample:
            ax2 = f.add_subplot(gs[0, 1])
            im2 = pcolormesh_square(ax2, normalized_data2, region[1], region[2], cmap=cmap, vmin=vmin, vmax=vmax)
            format_ticks(ax2, rotate=False)
            ax2.set_title(sampleid2, fontsize=10)
            ax2.set_aspect('equal')  # Ensure square aspect
            ax2.set_ylim(end, start)
            ax2.set_xlim(start, end)
            # Create a colorbar for Heatmap 2 in GridSpec row 1
            cax2 = f.add_subplot(gs[1, 1])
            im2 = pcolormesh_square(ax2, normalized_data2, region[1], region[2], cmap=cmap, vmin=vmin, vmax=vmax)
            cbar2 = plt.colorbar(im2, cax=cax2, orientation='horizontal')
            cbar2.ax.tick_params(labelsize=8)
            cax2.xaxis.set_label_position('bottom')
            cax2.xaxis.set_ticks_position('bottom')
            cbar2.set_label(normalization_method, labelpad=3)
            cbar2.ax.xaxis.set_label_position('top')
        # Compute y_max_list for BigWig tracks to ensure consistent y-axis across samples per track row
        y_min_max_list_bigwig = get_track_min_max(bigwig_files_sample1, bigwig_files_sample2, layout, region, normalization_method)
        #y_max_list_bed = get_bed_max(bed_files_sample1, bed_files_sample2, layout, region) if (bed_files_sample1 or bed_files_sample2) else []
        
        # Plot BigWig and BED tracks
        track_start_row = 2
        # Plot BigWig tracks for Sample1
        if len(bigwig_files_sample1):
            for i in range(len(bigwig_files_sample1)):
                ax_bw = f.add_subplot(gs[track_start_row + i, 0])
                plot_seq(ax_bw, bigwig_files_sample1[i], region, color=colors_sample1[i], 
                         y_min=y_min_max_list_bigwig[i][0], y_max=y_min_max_list_bigwig[i][1])
                ax_bw.set_title(f"{bigwig_labels_sample1[i]} ({sampleid1})", fontsize=8)
        # Plot BigWig tracks for Sample2 if provided
        if not single_sample and len(bigwig_files_sample2):
            for j in range(len(bigwig_files_sample2)):
                ax_bw = f.add_subplot(gs[track_start_row + j, 1])
                plot_seq(ax_bw, bigwig_files_sample2[j], region, color=colors_sample2[j], 
                         y_min=y_min_max_list_bigwig[j][0], y_max=y_min_max_list_bigwig[j][1])
                ax_bw.set_title(f"{bigwig_labels_sample2[j]} ({sampleid2})", fontsize=8)
        # Plot BED tracks for Sample1
        bed_start_row = track_start_row + len(bigwig_files_sample1)
        if len(bed_files_sample1):
            for k in range(len(bed_files_sample1)):
                ax_bed = f.add_subplot(gs[bed_start_row + k, 0])
                plot_bed(ax_bed, bed_files_sample1[k], region, color=colors_bed_sample1[k], label=bed_labels_sample1[k])
                ax_bed.set_title(f"{bed_labels_sample1[k]} ({sampleid1})", fontsize=8)
        # Plot BED tracks for Sample2 if provided
        if not single_sample and len(bed_files_sample2):
            for l in range(len(bed_files_sample2)):
                ax_bed = f.add_subplot(gs[bed_start_row + l, 1])
                plot_bed(ax_bed, bed_files_sample2[l], region, color=colors_bed_sample2[l], label=bed_labels_sample2[l])
                ax_bed.set_title(f"{bed_labels_sample2[l]} ({sampleid2})", fontsize=8)
    
        # Plot Genes if GTF file is provided
        if gtf_file:
            gene_row = 2 + max_bigwig_bed_tracks
            ax_genes = f.add_subplot(gs[gene_row, 0])
            plot_genes(ax_genes, gtf_file, region)
            ax_genes.set_xlim(start, end)
            ax_genes.set_aspect('auto')  # Default aspect
            format_ticks(ax_genes, rotate=False)
            if not single_sample:
                ax_genes2 = f.add_subplot(gs[gene_row, 1])
                plot_genes(ax_genes2, gtf_file, region)
                ax_genes2.set_xlim(start, end)
                ax_genes2.set_aspect('auto')  # Default aspect
                format_ticks(ax_genes2, rotate=False)
    elif layout == 'vertical':
        # Similar approach but stacking vertically
        # Row0: Heatmap Sample1
        # Row1: Heatmap Sample2
        # Row2: Colorbar spanning all columns
        # Rows3 to N: BigWig and BED tracks
        # Last row: Genes
        num_genes = 1 if gtf_file else 0
        ncols = 1
        max_cool_sample = 1 if single_sample else 2
        # Calculate the maximum number of tracks across samples
        max_bigwig_sample = len(bigwig_files_sample1) + len(bigwig_files_sample2)
        max_bed_sample = len(bed_files_sample1) + len(bed_files_sample2)
        max_tracks = max_bigwig_sample + max_bed_sample
        num_colorbars = 1

        num_rows = max_cool_sample + num_colorbars + max_tracks + num_genes
        # Define height ratios: [Heatmaps..., Colorbar, BigWig tracks..., BED tracks..., Genes]
        # Define a small height for the colorbar
        small_colorbar_height = 0.1  # Adjust as needed
        track_height_ratio = 0.5  # Adjust as needed for BigWig/BED tracks
        height_ratios = [1] * max_cool_sample + [small_colorbar_height] + [track_height_ratio] * (max_tracks) + [track_height_ratio * num_genes]

        # Initialize GridSpec
        gs = gridspec.GridSpec(num_rows, 1, height_ratios=height_ratios, hspace=0.3)
        # Define default figsize if not provided
        width = track_size
        # Calculate figure height
        figsize_height = sum(height_ratios) * (track_size / height_ratios[0]) + (num_rows -1)*track_spacing
        # Initialize figure
        f = plt.figure(figsize=(width, figsize_height))
        # Plot Heatmaps
        ax_heatmap1 = f.add_subplot(gs[0, 0])
        im1 = pcolormesh_square(ax_heatmap1, normalized_data1, region[1], region[2], cmap=cmap, vmin=vmin, vmax=vmax)
        #ax_heatmap1.set_aspect('auto')
        ax_heatmap1.set_ylim(end, start)
        ax_heatmap1.set_xlim(start, end)
        format_ticks(ax_heatmap1, rotate=False)
        ax_heatmap1.set_title(sampleid1, fontsize=8)

        # Plot second heatmap if sample2 data is provided
        if not single_sample:
            ax_heatmap2 = f.add_subplot(gs[1, 0])
            im2 = pcolormesh_square(ax_heatmap2, normalized_data2, region[1], region[2], cmap=cmap, vmin=vmin, vmax=vmax)
            #ax_heatmap2.set_aspect('auto')
            ax_heatmap2.set_ylim(end, start)
            ax_heatmap2.set_xlim(start, end)
            format_ticks(ax_heatmap2, rotate=False)
            ax_heatmap2.set_title(sampleid2, fontsize=10)

        # Create a shared colorbar for both heatmaps in GridSpec row
        cax = f.add_subplot(gs[max_cool_sample, 0])
        cbar = plt.colorbar(im1, cax=cax, orientation='horizontal')
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label(normalization_method, labelpad=3)
        cbar.ax.xaxis.set_label_position('top')

        # Compute y_max_list for BigWig tracks to ensure consistent y-axis across samples per track row
        y_min_max_list_bigwig = get_track_min_max(bigwig_files_sample1, bigwig_files_sample2, layout, region, normalization_method)
        #y_max_list_bed = get_bed_max(bed_files_sample1, bed_files_sample2, layout, region)

        track_start_row = max_cool_sample + 1
        # Plot BigWig files for sample 1
        if len(bigwig_files_sample1):
            for i in range(len(bigwig_files_sample1)):
                ax_bw = f.add_subplot(gs[track_start_row + i, 0])
                plot_seq(ax_bw, bigwig_files_sample1[i], region, color=colors_sample1[i], 
                    y_min=y_min_max_list_bigwig[i][0], y_max=y_min_max_list_bigwig[i][1])
                ax_bw.set_title(f"{bigwig_labels_sample1[i]} ({sampleid1})", fontsize=8)
                ax_bw.set_xlim(start, end)
                ax_bw.set_ylim(y_min_max_list_bigwig[i][0], y_min_max_list_bigwig[i][1] * 1.1)
        track_start_row = max_cool_sample + 1 + len(bigwig_files_sample1)
        # Plot BigWig files for sample 2 if provided
        if not single_sample and len(bigwig_files_sample2):
            for j in range(len(bigwig_files_sample2)):
                ax_bw = f.add_subplot(gs[track_start_row + j, 0])
                plot_seq(ax_bw, bigwig_files_sample2[j], region, color=colors_sample2[j], 
                    y_min=y_min_max_list_bigwig[j][0], y_max=y_min_max_list_bigwig[j][1])
                ax_bw.set_title(f"{bigwig_labels_sample2[j]} ({sampleid2})", fontsize=8)
                ax_bw.set_xlim(start, end)
                ax_bw.set_ylim(y_min_max_list_bigwig[j][0], y_min_max_list_bigwig[j][1] * 1.1)
        track_start_row = max_cool_sample + 1 + len(bigwig_files_sample1) + len(bigwig_files_sample2)
        # Plot BED tracks for Sample1
        if len(bed_files_sample1):
            for k in range(len(bed_files_sample1)):
                    ax_bed = f.add_subplot(gs[track_start_row + k, 0])
                    plot_bed(ax_bed, bed_files_sample1[k], region, color=colors_bed_sample1[k], label=bed_labels_sample1[k])
                    ax_bed.set_title(f"{bed_labels_sample1[k]} ({sampleid1})", fontsize=8)
        # Plot BED tracks for Sample2 if provided
        if not single_sample and len(bed_files_sample2):
            for l in range(len(bed_files_sample2)):
                    ax_bed = f.add_subplot(gs[track_start_row + l, 0])
                    plot_bed(ax_bed, bed_files_sample2[l], region, color=colors_bed_sample2[l], label=bed_labels_sample2[l])
                    ax_bed.set_title(f"{bed_labels_sample2[l]} ({sampleid2})", fontsize=8)

        # Plot Genes
        if gtf_file:
            gene_row = max_cool_sample + 1 + max_tracks
            ax_genes = f.add_subplot(gs[gene_row, 0])
            plot_genes(ax_genes, gtf_file, region)
            ax_genes.set_xlim(start, end)

    else:
        raise ValueError("Invalid layout option. Use 'horizontal' or 'vertical'.")
    
    # Adjust layout
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
    # Save the figure
    f.savefig(output_file, bbox_inches='tight')
    plt.close(f)


def main():
    parser = argparse.ArgumentParser(description='Plot heatmaps from cooler files.')

    parser.add_argument('--cooler_file1', type=str, required=True, help='Path to the first .cool or .mcool file.')
    parser.add_argument('--cooler_file2', type=str, required=False, help='Path to the second .cool or .mcool file.', default=None)
    parser.add_argument('--resolution', type=int, default=10000, help='Resolution for the cooler data.')
    parser.add_argument('--start', type=int, default=10500000, help='Start position for the region of interest.')
    parser.add_argument('--end', type=int, default=13200000, help='End position for the region of interest.')
    parser.add_argument('--chrid', type=str, default='chr2', help='Chromosome ID.')
    parser.add_argument('--cmap', type=str, default='autumn_r', help='Colormap to be used for plotting.')
    parser.add_argument('--vmin', type=float, default=None, help='Minimum value for color scaling.')
    parser.add_argument('--vmax', type=float, default=None, help='Maximum value for color scaling.')
    parser.add_argument('--output_file', type=str, default='comparison_heatmap.pdf', help='Filename for the saved comparison heatmap PDF.')
    parser.add_argument('--layout', type=str, default='horizontal', choices=['horizontal', 'vertical'],
                        help="Layout of the heatmaps: 'horizontal' or 'vertical'.")
    parser.add_argument('--sampleid1', type=str, default='Sample1', help='Sample ID for the first dataset.')
    parser.add_argument('--sampleid2', type=str, default='Sample2', help='Sample ID for the second dataset.')
    parser.add_argument('--gtf_file', type=str, required=True, help='Path to the GTF file for gene annotations.')
    
    # BigWig arguments
    parser.add_argument('--bigwig_files_sample1', type=str, nargs='*', help='Paths to BigWig files for sample 1.', default=[])
    parser.add_argument('--bigwig_labels_sample1', type=str, nargs='*', help='Labels for BigWig tracks of sample 1.', default=[])
    parser.add_argument('--colors_sample1', type=str, nargs='+', help='Colors for sample 1 BigWig tracks.', default=None)
    parser.add_argument('--bigwig_files_sample2', type=str, nargs='*', help='Paths to BigWig files for sample 2.', default=[])
    parser.add_argument('--bigwig_labels_sample2', type=str, nargs='*', help='Labels for BigWig tracks of sample 2.', default=[])
    parser.add_argument('--colors_sample2', type=str, nargs='+', help='Colors for sample 2 BigWig tracks.', default=None)
    
    # BED arguments
    parser.add_argument('--bed_files_sample1', type=str, nargs='*', help='Paths to BED files for sample 1.', default=[])
    parser.add_argument('--bed_labels_sample1', type=str, nargs='*', help='Labels for BED tracks of sample 1.', default=[])
    parser.add_argument('--colors_bed_sample1', type=str, nargs='+', help='Colors for sample 1 BED tracks.', default=None)
    parser.add_argument('--bed_files_sample2', type=str, nargs='*', help='Paths to BED files for sample 2.', default=[])
    parser.add_argument('--bed_labels_sample2', type=str, nargs='*', help='Labels for BED tracks of sample 2.', default=[])
    parser.add_argument('--colors_bed_sample2', type=str, nargs='+', help='Colors for sample 2 BED tracks.', default=None)
    
    # New Argument for Normalization Method
    parser.add_argument('--normalization_method', type=str, default='raw', choices=['raw', 'log2', 'log2_add1','log','log_add1'],
                        help="Method for normalization: 'raw', 'log2', 'log2_add1', 'log', or 'log_add1'.")
    
    parser.add_argument('--track_size', type=float, default=5, help='Width of each track (in inches).')
    parser.add_argument('--track_spacing', type=float, default=0.5, help='Spacing between tracks (in inches).')
    parser.add_argument("-V", "--version", action="version",version="TriHeatmap {}".format(__version__)\
                      ,help="Print version and exit")
    args = parser.parse_args()

if __name__ == '__main__':
    main()
