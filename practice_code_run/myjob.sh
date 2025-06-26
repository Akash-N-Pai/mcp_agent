#!/bin/bash
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
export ALRB_localConfigDir=$HOME/localConfig
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

lsetup rucio
rucio --verbose download --rse MWT2_DATADISK data16_13TeV:AOD.11071822._001488.pool.root.1

asetup AnalysisBase,21.2.81

cd data16_13TeV
truncate --size 10MB AOD.11071822._001488.pool.root.1
cp AOD.11071822._001488.pool.root.1 $DATA/myjob.output

sleep 300
