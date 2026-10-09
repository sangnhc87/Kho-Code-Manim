#!/bin/bash
RUN_02=$(gh run list --workflow="render_comb02_MASTER.yml" --json databaseId -q ".[0].databaseId")

echo "Waiting for COMB02 (ID: $RUN_02)..."
gh run watch $RUN_02 --exit-status
if [ $? -eq 0 ]; then
  echo "Downloading COMB02..."
  gh run download $RUN_02 -D Series-Dai-So-To-Hop/media_v2_02
  find Series-Dai-So-To-Hop/media_v2_02 -name "*.mp4" -exec mv {} Series-Dai-So-To-Hop/COMB02_FullHD.mp4 \;
  rm -rf Series-Dai-So-To-Hop/media_v2_02
fi
echo "Done!"
