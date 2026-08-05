#!/bin/bash
# run_spectra_experiments.sh
# Automated batch execution of spectra analysis for multiple PBL configurations on NCAR clusters.

# Common base path for your experiments
BASE_PATH="$SCRATCH/../morrison/cm1_dci_study/cm1r21.0/run"

# Array of experiment directory names and corresponding clean output tags
declare -A EXPERIMENTS
EXPERIMENTS["test11_highres_pbl0.42km_rh0.9"]="pbl0.42km"
EXPERIMENTS["test11_highres_pbl0.84km_rh0.9"]="pbl0.84km"
EXPERIMENTS["test11_highres_pbl1.68km_rh0.9"]="pbl1.68km"

# Execute sequentially
for dir in "${!EXPERIMENTS[@]}"; do
    tag=${EXPERIMENTS[$dir]}
    workdir="$BASE_PATH/$dir"

    output_name="test11_${tag}_spectra.mp4"

    echo "=========================================================================="
    echo "Processing experiment: $dir"
    echo "Source directory: $workdir"
    echo "Output files: $output_name & test11_${tag}_spectra_timeline.png"
    echo "=========================================================================="

    # Execute the python script with the target files and bounds
    # Note: quoting the expansion is avoided here to let the shell expand the NC glob patterns correctly
    python cm1_w_spectra_animated.py \
        $workdir/cm1out_0000[7-9]*.nc \
        $workdir/cm1out_000[12]*.nc \
        --pbl-bot 2 \
        --pbl-top 5 \
        --var winterp \
        --save-video "$output_name"

    echo "Finished processing $tag."
    echo ""
done

echo "All simulations completed successfully!"
