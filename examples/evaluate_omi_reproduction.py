# -*- coding: utf-8 -*-

# Copyright (C) 2019 Christoph G. Hoffmann. All rights reserved.

# This file is part of mjoindices

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Contact: christoph.hoffmann@uni-greifswald.de

"""
This example evaluates the quality of the OMI reproduction, but does not calculate the OMI values.
To generate the reproduction data, execute the example recalculate_original_omi.py.
Change path- and filenames below according to the settings in recalculate_original_omi.py.
"""

from pathlib import Path
import numpy as np
import os.path
import matplotlib.pyplot as plt

import mjoindices.empirical_orthogonal_functions as eof
import mjoindices.evaluation_tools
import mjoindices.principal_components as pc
import mjoindices.tools as tools

# ################ Settings. Change with respect to your system ###################

# Download the data file from ftp://ftp.cdc.noaa.gov/Datasets/interp_OLR/olr.day.mean.nc to your local file system and
# adjust the local path below.
# Note: If you have set up the test suite using the reference data package (https://doi.org/10.5281/zenodo.3746562) and
# if you have kept the original directory structure, the following default setting should directly work.
olr_data_filename = Path(os.path.abspath('')).parents[0] / "tests" / "testdata" / "olr.day.mean.nc"

# The following directory should contain the two subdirectories "eof1" and "eof2", which should contain the files
# downloaded from ftp://ftp.cdc.noaa.gov/Datasets.other/MJO/eof1/ and
# ftp://ftp.cdc.noaa.gov/Datasets.other/MJO/eof2/ , respectively.
# Note: If you have set up the test suite using the reference data package (https://doi.org/10.5281/zenodo.3746562) and
# if you have kept the original directory structure, the following default setting should directly work.
originalOMIDataDirname = Path(os.path.abspath('')).parents[0] / "tests" / "testdata" / "OriginalOMI"

# Download the original OMI values from https://www.esrl.noaa.gov/psd/mjo/mjoindex/omi.1x.txt to your local file system
# and adjust the local path below.
# Note: If you have set up the test suite using the reference data package (https://doi.org/10.5281/zenodo.3746562) and
# if you have kept the original directory structure, the following default setting should directly work.
originalOMIPCFile = Path(os.path.abspath('')).parents[0] / "tests" / "testdata" / "OriginalOMI" / "omi.1x.txt"

# The following file is included in the reference data package (https://doi.org/10.5281/zenodo.3746562).
# Note: If you have set up the test suite using the reference data package (https://doi.org/10.5281/zenodo.3746562) and
# if you have kept the original directory structure, the following default setting should directly work.
original_omi_explained_variance_file = Path(os.path.abspath('')).parents[0] / "tests" / "testdata" / "OriginalOMI" / "omi_var.txt"

# Files with recalculated OMI values (These files will be generated by the example recalculate_original_omi.py), adjust
# according to the settings in recalculate_original_omi.py:
# The EOFs
eofnpzfile = Path(os.path.abspath('')) / "example_data" / "EOFs.npz"
# The PCs
pctxtfile = Path(os.path.abspath('')) / "example_data" / "PCs.txt"
#

# Directory in which the figures are saved.
fig_dir = Path(os.path.abspath('')) / "example_data" / "omi_reproduction_evaluation_plots"

# Decide whether DOY 366 should be included in the evaluation or not.
setting_exclude_doy_366 = True

# ######## End of settings (There should be no need to change anything below)

if not fig_dir.exists():
    fig_dir.mkdir(parents=True, exist_ok=False)

# ########## evaluate EOFs.

eofs = eof.restore_all_eofs_from_npzfile(eofnpzfile)
orig_eofs = eof.load_all_original_eofs_from_directory(originalOMIDataDirname)

# Correlations.
fig = mjoindices.evaluation_tools.plot_correlation_for_eofs_all_doys(eofs, orig_eofs, exclude_doy366=setting_exclude_doy_366, do_print=True)
fig.show()
fig.savefig(fig_dir / "EOFCorrelations.png")
fig.savefig(fig_dir / "EOFCorrelations.pdf")

# Extended statistics.
fig = mjoindices.evaluation_tools.plot_comparison_stats_for_eofs_all_doys(eofs, orig_eofs, exclude_doy366=setting_exclude_doy_366, do_print=True)
fig.show()
fig.savefig(fig_dir / "EOFComparisonStatistics.png")
fig.savefig(fig_dir / "EOFComparisonStatistics.pdf")

#
doy=23 #among the best agreements.
# doy = 218 #worst agreement.
fig = mjoindices.evaluation_tools.plot_vector_agreement(orig_eofs.eof1vector_for_doy(doy), eofs.eof1vector_for_doy(doy), title="EOF1 for DOY %i" % doy, do_print=True)
fig.show()
fig.savefig(fig_dir / ("EOF1DetailedComparisonDOY%i.png"%doy))
fig.savefig(fig_dir / ("EOF1DetailedComparisonDOY%i.pdf"%doy))
fig = mjoindices.evaluation_tools.plot_vector_agreement(orig_eofs.eof2vector_for_doy(doy), eofs.eof2vector_for_doy(doy), title="EOF2 for DOY %i" % doy, do_print=True)
fig.show()
fig.savefig(fig_dir / ("EOF2DetailedComparisonDOY%i.png"%doy))
fig.savefig(fig_dir / ("EOF2DetailedComparisonDOY%i.pdf"%doy))

fig = mjoindices.evaluation_tools.plot_individual_eof_map_comparison(orig_eofs.eofdata_for_doy(doy), eofs.eofdata_for_doy(doy), doy=doy)
fig.show()
fig.savefig(fig_dir / ("EOFComparisonMapDOY%i.png"%doy))
fig.savefig(fig_dir / ("EOFComparisonMapDOY%i.pdf"%doy))

# # ########## Evaluate explained variance.
fig = eof.plot_explained_variance_for_all_doys(eofs, include_no_observations=False)
fig.show()
fig.savefig(fig_dir / "ExplainedVarianceForAllDoys.png")
fig.savefig(fig_dir / "ExplainedVarianceForAllDoys.pdf")

orig_explained_variance_1, orig_explained_variance_2 = mjoindices.evaluation_tools.load_omi_explained_variance(original_omi_explained_variance_file)
eofs = eof.restore_all_eofs_from_npzfile(eofnpzfile)
fig = mjoindices.evaluation_tools.plot_comparison_stats_for_explained_variance(orig_explained_variance_1, eofs.explained_variance1_for_all_doys(), title="Explained Variance for EOF1", do_print=True, exclude_doy366=setting_exclude_doy_366)
fig.show()
fig.savefig(fig_dir / "ExplainedVarianceComparison_EOF1.png")
fig.savefig(fig_dir / "ExplainedVarianceComparison_EOF1.pdf")
fig = mjoindices.evaluation_tools.plot_comparison_stats_for_explained_variance(orig_explained_variance_2, eofs.explained_variance2_for_all_doys(), title="Explained Variance for EOF2", do_print=True, exclude_doy366=setting_exclude_doy_366)
fig.show()
fig.savefig(fig_dir / "ExplainedVarianceComparison_EOF2.png")
fig.savefig(fig_dir / "ExplainedVarianceComparison_EOF2.pdf")

# ########## Evaluate PCs.

pcs = pc.load_pcs_from_txt_file(pctxtfile)
orig_pcs = pc.load_original_pcs_from_txt_file(originalOMIPCFile)

# Plot sample period.
fig = mjoindices.evaluation_tools.plot_comparison_orig_calc_pcs(pcs, orig_pcs, start_date=np.datetime64("2011-01-01"), end_date=np.datetime64("2011-12-31"))
fig.show()
fig.savefig(fig_dir / "PCTimeSeriesSample.png")
fig.savefig(fig_dir / "PCTimeSeriesSample.pdf")

fig = mjoindices.evaluation_tools.plot_timeseries_agreement(orig_pcs.pc1, orig_pcs.time, pcs.pc1, pcs.time, title="PC1", do_print=True)
fig.show()
fig.savefig(fig_dir / "PC1_Comparison.png")
fig.savefig(fig_dir / "PC1_Comparison.pdf")
fig = mjoindices.evaluation_tools.plot_timeseries_agreement(orig_pcs.pc2, orig_pcs.time, pcs.pc2, pcs.time, title="PC2", do_print=True)
fig.show()
fig.savefig(fig_dir / "PC2_Comparison.png")
fig.savefig(fig_dir / "PC2_Comparison.pdf")

strength = np.sqrt(np.square(pcs.pc1) + np.square(pcs.pc2))
orig_strength = np.sqrt(np.square(orig_pcs.pc1) + np.square(orig_pcs.pc2))
fig = mjoindices.evaluation_tools.plot_timeseries_agreement(orig_strength, orig_pcs.time, strength, pcs.time, title="MJO Strength", do_print=True)
fig.show()
fig.savefig(fig_dir / "MJOStrength_Comparison.png")
fig.savefig(fig_dir / "MJOStrength_Comparison.pdf")



