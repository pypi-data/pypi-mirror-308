# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spikesorter.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import biointerface_pb2 as biointerface__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11spikesorter.proto\x12\x06\x61llego\x1a\x0c\x63ommon.proto\x1a\x12\x62iointerface.proto\"\xaa\x02\n\x18SpikeSorterLaunchRequest\x12\x11\n\tdsourceID\x18\x01 \x01(\t\x12&\n\x06source\x18\x02 \x01(\x0b\x32\x16.allego.FileDescriptor\x12\x42\n\x0f\x63lustererParams\x18\x03 \x01(\x0b\x32).allego.SpikeSorterClustererParamsRequest\x12>\n\rfeatureParams\x18\x04 \x01(\x0b\x32\'.allego.SpikeSorterFeatureParamsRequest\x12\x15\n\rdiscoverNoise\x18\x05 \x01(\x08\x12\x10\n\x08isAutoOn\x18\x06 \x01(\x08\x12\x12\n\nnbrPattern\x18\x07 \x01(\x05\x12\x12\n\nsinkDsrcID\x18\x08 \x01(\t\"7\n\x1dSpikeSorterIsAnyActiveRequest\x12\x16\n\x0espikeSorterIDs\x18\x01 \x03(\t\"O\n\x1bSpikeSorterIsAnyActiveReply\x12\x13\n\x0bisAnyActive\x18\x01 \x02(\x08\x12\x1b\n\x13\x61\x63tiveSpikeSorterID\x18\x02 \x01(\t\"\x8e\x02\n\x19SpikeSorterCommandRequest\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\'\n\x03\x63md\x18\x02 \x02(\x0e\x32\x1a.allego.SpikeSorterCommand\x12-\n\x06subCmd\x18\x03 \x02(\x0e\x32\x1d.allego.SpikeSorterSubCommand\x12\x42\n\x0f\x63lustererParams\x18\x04 \x01(\x0b\x32).allego.SpikeSorterClustererParamsRequest\x12>\n\rfeatureParams\x18\x05 \x01(\x0b\x32\'.allego.SpikeSorterFeatureParamsRequest\"\x93\x01\n\x10SpikeSorterState\x12+\n\x03sys\x18\x01 \x02(\x0e\x32\x1e.allego.SpikeSorterStateSystem\x12\x14\n\x0c\x66racComplete\x18\x02 \x01(\x01\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x0c\n\x04isOn\x18\x08 \x01(\x08\x12\x10\n\x08\x65rrorMsg\x18\t \x01(\t\x12\x0f\n\x07warnMsg\x18\n \x01(\t\"\x81\x01\n\x0cSpkSortIOreq\x12#\n\x04type\x18\x01 \x02(\x0e\x32\x15.allego.SpkSortIOtype\x12\'\n\x06target\x18\x02 \x02(\x0e\x32\x17.allego.SpkSortIOtarget\x12#\n\x04mode\x18\x03 \x02(\x0e\x32\x15.allego.SpkSortIOmode\"\x8f\x01\n\x16SpikeSorterLaunchReply\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12+\n\nsorterType\x18\x02 \x02(\x0e\x32\x17.allego.SpikeSorterType\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12$\n\x04\x64\x65sc\x18\x04 \x01(\x0b\x32\x16.allego.FileDescriptor\"1\n\x18GetSpikeSorterIDsRequest\x12\x15\n\rstreamGroupID\x18\x01 \x02(\t\"0\n\x16GetSpikeSorterIDsReply\x12\x16\n\x0espikeSorterIDs\x18\x01 \x03(\t\"\xdd\x01\n\x1fSpikeSorterGetRasterDataRequest\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x12\n\ntimeWindow\x18\x03 \x02(\x01\x12\x17\n\x0fplotWidthPoints\x18\x04 \x02(\x01\x12\x13\n\x0b\x63omponentID\x18\x05 \x02(\t\x12\x11\n\ttimeRange\x18\x06 \x03(\x01\x12 \n\x04mode\x18\x07 \x02(\x0e\x32\x12.allego.RasterMode\x12\x13\n\x0blabeledOnly\x18\x08 \x01(\x08\x12\x17\n\x0fprimarySiteOnly\x18\t \x01(\x08\"\x9d\x01\n\x1aSpikeSorterRasterDataReply\x12/\n\x0fspikeTimestamps\x18\x02 \x03(\x0b\x32\x16.allego.SpikeTimestamp\x12\x11\n\ttimeRange\x18\x03 \x03(\x01\x12\x16\n\x0etimeStampRange\x18\x04 \x03(\x03\x12\x10\n\x08GPIOData\x18\x05 \x02(\x0c\x12\x11\n\tGPIOShape\x18\x06 \x03(\x05\"J\n\x1aSpikeSorterStandardRequest\x12\x15\n\rstreamGroupID\x18\x01 \x01(\t\x12\x15\n\rspikeSorterID\x18\x02 \x01(\t\"_\n\x1bSpikeSorterDashboardRequest\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12)\n\x0c\x64\x61shElements\x18\x02 \x03(\x0e\x32\x13.allego.DashElement\"\x86\x03\n\x12SpikeSorterDynamic\x12\x11\n\tisEnabled\x18\x01 \x01(\x08\x12\x43\n\x0fupdatePeriodSec\x18\x02 \x01(\x0b\x32*.allego.SpikeSorterDynamic.UpdatePeriodSec\x12\x35\n\x08\x63riteria\x18\x03 \x01(\x0b\x32#.allego.SpikeSorterDynamic.Criteria\x1a\xa0\x01\n\x08\x43riteria\x12\x31\n\x06\x64\x65tect\x18\x01 \x01(\x0e\x32!.allego.SpikeSorterCriterionLevel\x12\x30\n\x05train\x18\x02 \x01(\x0e\x32!.allego.SpikeSorterCriterionLevel\x12/\n\x04sort\x18\x03 \x01(\x0e\x32!.allego.SpikeSorterCriterionLevel\x1a>\n\x0fUpdatePeriodSec\x12\x0e\n\x06\x64\x65tect\x18\x01 \x01(\x01\x12\r\n\x05train\x18\x02 \x01(\x01\x12\x0c\n\x04sort\x18\x03 \x01(\x01\"\xc5\x01\n\x1cSpikeSorterSetDynamicRequest\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x42\n\x07variant\x18\x02 \x03(\x0b\x32\x31.allego.SpikeSorterSetDynamicRequest.VariantEntry\x1aJ\n\x0cVariantEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.allego.SpikeSorterDynamic:\x02\x38\x01\"\xd8\x01\n\x1aSpikeSorterGetDynamicReply\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x15\n\rrootVariantID\x18\x02 \x02(\t\x12@\n\x07variant\x18\x03 \x03(\x0b\x32/.allego.SpikeSorterGetDynamicReply.VariantEntry\x1aJ\n\x0cVariantEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.allego.SpikeSorterDynamic:\x02\x38\x01\"l\n\x1fGetSpikeSorterParamCommandReply\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x32\n\x03rec\x18\x02 \x03(\x0b\x32%.allego.SpikeSorterParamCommandRecord\"3\n\x12\x43lusterMapOutliers\x12\x0c\n\x04mild\x18\x01 \x03(\x01\x12\x0f\n\x07\x65xtreme\x18\x02 \x03(\x01\"9\n\x13\x43lusterMapQuartiles\x12\n\n\x02q1\x18\x01 \x02(\x01\x12\n\n\x02q2\x18\x02 \x02(\x01\x12\n\n\x02q3\x18\x03 \x02(\x01\"\x83\x01\n\x0f\x43lusterMapStats\x12\x16\n\x0e\x63\x65ntroidCenter\x18\x01 \x03(\x01\x12\x12\n\ncentroidSd\x18\x02 \x03(\x01\x12\x16\n\x0e\x63\x65ntroidSdNorm\x18\x03 \x02(\x01\x12\x19\n\x11intraCentroidDist\x18\x04 \x03(\x01\x12\x11\n\tnumSpikes\x18\x05 \x02(\x03\"f\n\x10\x43lusterMapRecord\x12\r\n\x05label\x18\x01 \x02(\x05\x12&\n\x05stats\x18\x03 \x02(\x0b\x32\x17.allego.ClusterMapStats\x12\x1b\n\x13numSpikesTrainCache\x18\x04 \x02(\x03\"\xa8\x01\n\x13SpikeSortSiteStatus\x12\x12\n\nntvChanIdx\x18\x01 \x02(\x05\x12\x15\n\rorderedLabels\x18\x02 \x03(\x05\x12)\n\x07\x63luster\x18\x03 \x03(\x0b\x32\x18.allego.ClusterMapRecord\x12\x11\n\tnumSpikes\x18\x04 \x03(\x03\x12\x0c\n\x04zeta\x18\x05 \x03(\x01\x12\x1a\n\x12\x61ggregateSpikeRate\x18\x06 \x02(\x01\"\x8f\x01\n\x14SpikeSortPhaseStatus\x12\x11\n\ttimeRange\x18\x01 \x03(\x01\x12\x12\n\nchunkIndex\x18\x02 \x02(\x03\x12\x14\n\x0cupdatePeriod\x18\x03 \x02(\x01\x12\x0c\n\x04\x62\x65ta\x18\x04 \x02(\x01\x12\x12\n\nisComplete\x18\x05 \x02(\x08\x12\x18\n\x10\x66ractionComplete\x18\x06 \x02(\x01\"*\n\x13SpikeSortNbrIdxList\x12\x13\n\x0bntvChanIdxs\x18\x01 \x03(\x05\"\xf2\x02\n\x16SpikeSorterStatusReply\x12\'\n\x05state\x18\x01 \x02(\x0b\x32\x18.allego.SpikeSorterState\x12\x16\n\x0e\x62iointerfaceID\x18\x03 \x02(\t\x12\x14\n\x0c\x64\x61tasourceID\x18\x04 \x02(\t\x12\x10\n\x08sampFreq\x18\x05 \x02(\x01\x12\x19\n\x11\x65nabledNtvChanIdx\x18\x06 \x03(\x05\x12+\n\x05phase\x18\x07 \x03(\x0b\x32\x1c.allego.SpikeSortPhaseStatus\x12\x30\n\x0b\x65nabledSite\x18\x08 \x03(\x0b\x32\x1b.allego.SpikeSortSiteStatus\x12\x12\n\nprobeYield\x18\t \x02(\x01\x12\x11\n\tsortStats\x18\n \x03(\x01\x12\x1b\n\x13\x64\x61tasourceTimeRange\x18\x0c \x03(\x01\x12\x1d\n\x15\x62iointerfaceTimeRange\x18\r \x03(\x01\x12\x12\n\nnumNeurons\x18\x0f \x02(\x03\"R\n\x1eSpikeSorterStatusVariantsReply\x12\x30\n\x08variants\x18\x01 \x03(\x0b\x32\x1e.allego.SpikeSorterStatusReply\"\xfd\x02\n\x19SpikeSorterClassifierSpec\x12\r\n\x05\x61lpha\x18\x01 \x02(\x01\x12\x11\n\talphaBias\x18\x02 \x02(\x01\x12\x16\n\x0e\x64imOutputLayer\x18\x03 \x02(\x05\x12\x16\n\x0e\x65rrorTolerance\x18\x04 \x02(\x01\x12\x19\n\x11hiddenLayerFactor\x18\x05 \x02(\x01\x12\n\n\x02iD\x18\x06 \x02(\t\x12\x16\n\x0einitBiasStdDev\x18\x07 \x02(\x01\x12\x18\n\x10initWeightStdDev\x18\x08 \x02(\x01\x12\x11\n\tisMasking\x18\t \x02(\x08\x12\x10\n\x08l1lambda\x18\n \x02(\x01\x12\x15\n\rminibatchSize\x18\x0b \x02(\x05\x12\x15\n\rmaxNumSamples\x18\x0c \x02(\x05\x12\x11\n\tnumEpochs\x18\r \x02(\x05\x12\x19\n\x11numSamplesTestMSE\x18\x0e \x02(\x05\x12\x1b\n\x13numConcurrentModels\x18\x0f \x02(\x05\x12\x17\n\x0flabelNoiseLevel\x18\x10 \x02(\x01\"u\n\x16SpikeSorterVariantSpec\x12\n\n\x02iD\x18\x01 \x02(\t\x12\x14\n\x0csiteConfigID\x18\x02 \x02(\t\x12\x39\n\x0e\x63lassifierSpec\x18\x03 \x02(\x0b\x32!.allego.SpikeSorterClassifierSpec\"\xcc\x01\n\x0fSpikeSorterSpec\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x14\n\x0c\x64\x61tasourceID\x18\x02 \x02(\t\x12\x16\n\x0e\x62iointerfaceID\x18\x03 \x02(\t\x12\x1b\n\x13maxNumSiteNeighbors\x18\x04 \x02(\x05\x12\x18\n\x10neighborRadiusUm\x18\x05 \x02(\x01\x12/\n\x07variant\x18\x06 \x03(\x0b\x32\x1e.allego.SpikeSorterVariantSpec\x12\x0c\n\x04seed\x18\x08 \x02(\x03\"\xc2\x01\n\x19SpikeSorterGetConfigReply\x12%\n\x04spec\x18\x01 \x02(\x0b\x32\x17.allego.SpikeSorterSpec\x12\x16\n\x0e\x61IupdatePeriod\x18\x02 \x02(\x01\x12\x19\n\x11orderedVariantIDs\x18\x03 \x03(\t\x12\x15\n\rrootVariantID\x18\x04 \x02(\t\x12\x34\n\x0csorterStatus\x18\x06 \x03(\x0b\x32\x1e.allego.SpikeSorterStatusReply\"\x90\x02\n\x15SpikeSorterVizRequest\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12\x11\n\tvariantID\x18\x02 \x02(\t\x12\x12\n\nntvChanIdx\x18\x03 \x03(\x05\x12\x13\n\x0bspikeLabels\x18\x04 \x03(\x05\x12\x34\n\x07vizType\x18\x05 \x02(\x0e\x32#.allego.SpikeSorterVizRequest.VType\x12\x14\n\x0cisYAutoScale\x18\x06 \x02(\x08\x12\x0c\n\x04yLim\x18\x07 \x03(\x01\x12\x0e\n\x06\x66igDir\x18\x08 \x02(\t\x12\x11\n\tnumSpikes\x18\t \x02(\x05\"\'\n\x05VType\x12\x1e\n\x1aVIZ_SPIKESORT_TRAIN_SPIKES\x10\x00\"y\n!SpikeSorterClustererParamsRequest\x12\x18\n\x10posInfluenceFrac\x18\x01 \x01(\x01\x12\x1d\n\x15wfmShapeInfluenceFrac\x18\x02 \x01(\x01\x12\x0b\n\x03\x65ps\x18\x03 \x01(\x01\x12\x0e\n\x06minPts\x18\x04 \x01(\x05\"\x90\x01\n\x1fSpikeSorterFeatureParamsRequest\x12\x13\n\x0bnumFeatures\x18\x01 \x02(\x05\x12-\n\x0b\x66\x65\x61tureType\x18\x02 \x01(\x0e\x32\x18.allego.InputFeatureType\x12\x11\n\tlatentDim\x18\x03 \x01(\x05\x12\x16\n\x0eresampleWfmLen\x18\x04 \x01(\x05\"\xcb\x01\n\x1dSpikeSorterFeatureParamsReply\x12\x15\n\rspikeSorterID\x18\x01 \x02(\t\x12-\n\x0b\x66\x65\x61tureType\x18\x02 \x02(\x0e\x32\x18.allego.InputFeatureType\x12\x16\n\x0emaxNumFeatures\x18\x03 \x02(\x05\x12\x13\n\x0bnumFeatures\x18\x04 \x02(\x05\x12\x18\n\x10posInfluenceFrac\x18\x05 \x02(\x02\x12\x1d\n\x15wfmShapeInfluenceFrac\x18\x06 \x02(\x02\"\xb6\x05\n\x19SpikeSorterDashboardReply\x12\"\n\x0c\x65nabledPorts\x18\x01 \x03(\x0e\x32\x0c.allego.Port\x12\x37\n\x07general\x18\x02 \x01(\x0b\x32&.allego.SpikeSorterDashboardGeneralRec\x12\x33\n\tsiteStats\x18\x03 \x01(\x0b\x32 .allego.IndicoDashboardSiteStats\x12\x43\n\tportStats\x18\x04 \x03(\x0b\x32\x30.allego.SpikeSorterDashboardReply.PortStatsEntry\x12\x43\n\tsitePanel\x18\x05 \x03(\x0b\x32\x30.allego.SpikeSorterDashboardReply.SitePanelEntry\x12G\n\x0bneuronPanel\x18\x06 \x03(\x0b\x32\x32.allego.SpikeSorterDashboardReply.NeuronPanelEntry\x12*\n\x02\x61I\x18\x07 \x01(\x0b\x32\x1e.allego.SpikeSorterDashboardAI\x1aR\n\x0ePortStatsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12/\n\x05value\x18\x02 \x01(\x0b\x32 .allego.IndicoDashboardPortStats:\x02\x38\x01\x1aW\n\x0eSitePanelEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.allego.IndicoDashboardSiteIndicators:\x02\x38\x01\x1a[\n\x10NeuronPanelEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.allego.IndicoDashboardNeuronIndicators:\x02\x38\x01\"\xac\x03\n\x1eSpikeSorterDashboardGeneralRec\x12\'\n\x05state\x18\x01 \x02(\x0b\x32\x18.allego.SpikeSorterState\x12+\n\nsorterType\x18\x02 \x02(\x0e\x32\x17.allego.SpikeSorterType\x12\x10\n\x08sorterID\x18\x03 \x02(\t\x12\x14\n\x0c\x64\x61tasourceID\x18\x04 \x02(\t\x12\x11\n\ttimeRange\x18\x05 \x03(\x01\x12\x15\n\rnumTotalSites\x18\x06 \x02(\x03\x12\x17\n\x0fnumEnabledSites\x18\x07 \x02(\x03\x12\x16\n\x0enumActiveSites\x18\x08 \x02(\x03\x12\x12\n\nnumNeurons\x18\t \x02(\x03\x12\x12\n\nprobeYield\x18\n \x02(\x01\x12\x11\n\tsiteYield\x18\x0b \x02(\x01\x12\x1a\n\x12numSpikesProcessed\x18\x0c \x02(\x03\x12\x18\n\x10numSpikesLabeled\x18\r \x02(\x03\x12\x16\n\x0esortEfficiency\x18\x0e \x02(\x01\x12(\n\x08sinkDesc\x18\x0f \x02(\x0b\x32\x16.allego.FileDescriptor\"\xd5\x01\n\x16SpikeSorterDashboardAI\x12\x0c\n\x04\x62\x65ta\x18\x01 \x02(\x01\x12\"\n\x1a\x65stimatedReaderCompleteSec\x18\x02 \x02(\x01\x12\x1a\n\x12interSessionDurSec\x18\x03 \x02(\x01\x12\x19\n\x11interSessionStart\x18\x04 \x02(\t\x12\x15\n\rsessionDurSec\x18\x05 \x02(\x01\x12\x14\n\x0csessionStart\x18\x06 \x02(\t\x12\x12\n\nsessionIdx\x18\x07 \x02(\x03\x12\x11\n\tstartTime\x18\x08 \x02(\t\"_\n\x18IndicoDashboardSiteStats\x12\x0b\n\x03snr\x18\x01 \x03(\x01\x12\r\n\x05noise\x18\x02 \x03(\x01\x12\x13\n\x0bneuronYield\x18\x03 \x03(\x01\x12\x12\n\nnumNeurons\x18\x04 \x02(\x03\"\x90\x01\n\x18IndicoDashboardPortStats\x12\x0b\n\x03snr\x18\x01 \x03(\x01\x12\r\n\x05noise\x18\x02 \x03(\x01\x12\x13\n\x0bneuronYield\x18\x03 \x03(\x01\x12\x16\n\x0esortEfficiency\x18\x04 \x02(\x01\x12\x17\n\x0fnumEnabledSites\x18\x05 \x02(\x03\x12\x12\n\nnumNeurons\x18\x06 \x02(\x03\"\xd9\x01\n\x1dIndicoDashboardSiteIndicators\x12\x12\n\nntvChanIdx\x18\x01 \x03(\x05\x12\x0b\n\x03snr\x18\x02 \x03(\x01\x12\r\n\x05noise\x18\x03 \x03(\x01\x12\x13\n\x0bneuronYield\x18\x04 \x03(\x01\x12\x16\n\x0esortEfficiency\x18\x05 \x03(\x01\x12\x11\n\tspikeRate\x18\x06 \x03(\x01\x12\x11\n\tposProbeX\x18\x07 \x03(\x01\x12\x11\n\tposProbeY\x18\x08 \x03(\x01\x12\x11\n\tposProbeZ\x18\t \x03(\x01\x12\x0f\n\x07siteNum\x18\n \x03(\x05\"\xb1\x01\n\x1fIndicoDashboardNeuronIndicators\x12\x10\n\x08neuronID\x18\x01 \x03(\t\x12\x0b\n\x03snr\x18\x02 \x03(\x01\x12\x11\n\tspikeRate\x18\x03 \x03(\x01\x12\x11\n\tposProbeX\x18\x04 \x03(\x01\x12\x11\n\tposProbeY\x18\x05 \x03(\x01\x12\x11\n\tposProbeZ\x18\x06 \x03(\x01\x12\x0f\n\x07siteNum\x18\x07 \x03(\x05\x12\x12\n\nspikeLabel\x18\x08 \x03(\x05\"\xa7\x02\n\x1cSpikeSorterDashboardSiteDesc\x12\x1a\n\x04port\x18\x01 \x02(\x0e\x32\x0c.allego.Port\x12\x12\n\nntvChanIdx\x18\x02 \x02(\x05\x12\x10\n\x08posProbe\x18\x03 \x03(\x01\x12\x10\n\x08posBrain\x18\x04 \x03(\x01\x12\x0e\n\x06snrMax\x18\x05 \x02(\x01\x12\x0e\n\x06snrMin\x18\x06 \x02(\x01\x12\x12\n\nnoiseLevel\x18\x07 \x02(\x01\x12\x12\n\nnumNeurons\x18\x08 \x02(\x03\x12/\n\rindicoCluster\x18\n \x03(\x0b\x32\x18.allego.ClusterMapRecord\x12\x1c\n\x14pileWaveformMinValue\x18\r \x02(\x02\x12\x1c\n\x14pileWaveformMaxValue\x18\x0e \x02(\x02\"\xd2\x01\n\x1eSpikeSorterDashboardNeuronDesc\x12\x1a\n\x04port\x18\x01 \x02(\x0e\x32\x0c.allego.Port\x12&\n\x04\x64\x65sc\x18\x02 \x02(\x0b\x32\x18.allego.NeuronDescriptor\x12\x0b\n\x03snr\x18\x05 \x02(\x01\x12\x0f\n\x07IsihMax\x18\x06 \x02(\x01\x12\x15\n\rIsihArgmaxSec\x18\x07 \x02(\x01\x12\x15\n\rIsihArgmaxIdx\x18\x08 \x02(\x03\x12\x10\n\x08IsihMean\x18\t \x02(\x01\x12\x0e\n\x06IsihSd\x18\n \x02(\x01\"\xfa\x01\n SpikeSorterDashboardNeuronDetail\x12&\n\x04\x64\x65sc\x18\x01 \x02(\x0b\x32\x18.allego.NeuronDescriptor\x12\x18\n\x10templateWaveform\x18\x02 \x03(\x02\x12\x1a\n\x12templateSdWaveform\x18\x03 \x03(\x02\x12\x18\n\x10pileWaveformData\x18\x04 \x03(\x02\x12\x1e\n\x16numSamplesPileWaveform\x18\x05 \x02(\x05\x12\x18\n\x10numPileWaveforms\x18\x06 \x02(\x05\x12$\n\x04isih\x18\x0b \x02(\x0b\x32\x16.allego.NeuronHistData\"\xa9\x01\n\x1eSpikeSorterDashboardSiteDetail\x12\x32\n\x04\x64\x65sc\x18\x01 \x02(\x0b\x32$.allego.SpikeSorterDashboardSiteDesc\x12\x19\n\x11orderedSpikeLabel\x18\x02 \x03(\x05\x12\x38\n\x06neuron\x18\x03 \x03(\x0b\x32(.allego.SpikeSorterDashboardNeuronDetail*\x80\x01\n\x0fSpikeSorterType\x12\x0f\n\x0bSORTER_NULL\x10\x00\x12\x15\n\x11SORTER_VEX_STREAM\x10\x01\x12\x18\n\x14SORTER_SPIKES_STREAM\x10\x02\x12\x13\n\x0fSORTER_VEX_FILE\x10\x03\x12\x16\n\x12SORTER_SPIKES_FILE\x10\x04*\x82\x01\n\x12SpikeSorterCommand\x12\x11\n\rSORTER_CMD_ON\x10\x00\x12\x12\n\x0eSORTER_CMD_OFF\x10\x01\x12\x19\n\x15SORTER_CMD_CLEAR_SORT\x10\x02\x12\x15\n\x11SORTER_CMD_REBASE\x10\x04\x12\x13\n\x0fSORTER_CMD_INIT\x10\x05*/\n\x15SpikeSorterSubCommand\x12\x16\n\x12SORTER_SUBCMD_NULL\x10\x00*@\n\x0fSpikeSorterMode\x12\x16\n\x12SORTER_MODE_STREAM\x10\x00\x12\x15\n\x11SORTER_MODE_BATCH\x10\x01*I\n\x16SpikeSorterStateSystem\x12\n\n\x06SYS_ON\x10\x00\x12\x0b\n\x07SYS_OFF\x10\x01\x12\x16\n\x12SYS_NOT_CONFIGURED\x10\x02*f\n\rSpkSortIOtype\x12\x17\n\x13SPK_SORT_IO_NETWORK\x10\x00\x12\x17\n\x13SPK_SORT_IO_TRAINER\x10\x01\x12#\n\x1fSPK_SORT_IO_NETWORK_AND_TRAINER\x10\x02*>\n\x0fSpkSortIOtarget\x12\x14\n\x10SPK_SORT_IO_FSYS\x10\x00\x12\x15\n\x11SPK_SORT_IO_CLOUD\x10\x01*;\n\rSpkSortIOmode\x12\x14\n\x10SPK_SORT_IO_SAVE\x10\x00\x12\x14\n\x10SPK_SORT_IO_LOAD\x10\x01*\'\n\nRasterMode\x12\x0c\n\x08\x43HANNELS\x10\x00\x12\x0b\n\x07NEURONS\x10\x01*\x89\x01\n\x0b\x44\x61shElement\x12\x11\n\rENABLED_PORTS\x10\x01\x12\x0b\n\x07GENERAL\x10\x02\x12\x0e\n\nPORT_STATS\x10\x03\x12\x0e\n\nSITE_STATS\x10\x04\x12\x0e\n\nSITE_PANEL\x10\x05\x12\x10\n\x0cNEURON_STATS\x10\x06\x12\x10\n\x0cNEURON_PANEL\x10\x07\x12\x06\n\x02\x41I\x10\x08*u\n\x19SpikeSorterCriterionLevel\x12\x10\n\x0cSORTER_LEAST\x10\x00\x12\x0f\n\x0bSORTER_LESS\x10\x01\x12\x13\n\x0fSORTER_BALANCED\x10\x02\x12\x0f\n\x0bSORTER_MORE\x10\x03\x12\x0f\n\x0bSORTER_MOST\x10\x04*\x84\x01\n\x07SS_STAT\x12\x08\n\x04MEAN\x10\x00\x12\x06\n\x02SD\x10\x01\x12\x08\n\x04MODE\x10\x02\x12\x07\n\x03MIN\x10\x03\x12\x07\n\x03MAX\x10\x04\x12\x0e\n\nMODE_COUNT\x10\x05\x12\n\n\x06MEDIAN\x10\x06\x12\x07\n\x03Q25\x10\x07\x12\x07\n\x03Q75\x10\x08\x12\x08\n\x04SKEW\x10\t\x12\x0c\n\x08KURTOSIS\x10\n\x12\x05\n\x01N\x10\x0b*b\n\x10InputFeatureType\x12\x10\n\x0c\x46TR_TYPE_WFM\x10\x00\x12\x10\n\x0c\x46TR_TYPE_SPD\x10\x01\x12\x14\n\x10\x46TR_TYPE_WFM_POS\x10\x02\x12\x14\n\x10\x46TR_TYPE_SPD_POS\x10\x03\x42\x15Z\x13internal/radix/grpc')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spikesorter_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\023internal/radix/grpc'
  _SPIKESORTERSETDYNAMICREQUEST_VARIANTENTRY._options = None
  _SPIKESORTERSETDYNAMICREQUEST_VARIANTENTRY._serialized_options = b'8\001'
  _SPIKESORTERGETDYNAMICREPLY_VARIANTENTRY._options = None
  _SPIKESORTERGETDYNAMICREPLY_VARIANTENTRY._serialized_options = b'8\001'
  _SPIKESORTERDASHBOARDREPLY_PORTSTATSENTRY._options = None
  _SPIKESORTERDASHBOARDREPLY_PORTSTATSENTRY._serialized_options = b'8\001'
  _SPIKESORTERDASHBOARDREPLY_SITEPANELENTRY._options = None
  _SPIKESORTERDASHBOARDREPLY_SITEPANELENTRY._serialized_options = b'8\001'
  _SPIKESORTERDASHBOARDREPLY_NEURONPANELENTRY._options = None
  _SPIKESORTERDASHBOARDREPLY_NEURONPANELENTRY._serialized_options = b'8\001'
  _SPIKESORTERTYPE._serialized_start=8534
  _SPIKESORTERTYPE._serialized_end=8662
  _SPIKESORTERCOMMAND._serialized_start=8665
  _SPIKESORTERCOMMAND._serialized_end=8795
  _SPIKESORTERSUBCOMMAND._serialized_start=8797
  _SPIKESORTERSUBCOMMAND._serialized_end=8844
  _SPIKESORTERMODE._serialized_start=8846
  _SPIKESORTERMODE._serialized_end=8910
  _SPIKESORTERSTATESYSTEM._serialized_start=8912
  _SPIKESORTERSTATESYSTEM._serialized_end=8985
  _SPKSORTIOTYPE._serialized_start=8987
  _SPKSORTIOTYPE._serialized_end=9089
  _SPKSORTIOTARGET._serialized_start=9091
  _SPKSORTIOTARGET._serialized_end=9153
  _SPKSORTIOMODE._serialized_start=9155
  _SPKSORTIOMODE._serialized_end=9214
  _RASTERMODE._serialized_start=9216
  _RASTERMODE._serialized_end=9255
  _DASHELEMENT._serialized_start=9258
  _DASHELEMENT._serialized_end=9395
  _SPIKESORTERCRITERIONLEVEL._serialized_start=9397
  _SPIKESORTERCRITERIONLEVEL._serialized_end=9514
  _SS_STAT._serialized_start=9517
  _SS_STAT._serialized_end=9649
  _INPUTFEATURETYPE._serialized_start=9651
  _INPUTFEATURETYPE._serialized_end=9749
  _SPIKESORTERLAUNCHREQUEST._serialized_start=64
  _SPIKESORTERLAUNCHREQUEST._serialized_end=362
  _SPIKESORTERISANYACTIVEREQUEST._serialized_start=364
  _SPIKESORTERISANYACTIVEREQUEST._serialized_end=419
  _SPIKESORTERISANYACTIVEREPLY._serialized_start=421
  _SPIKESORTERISANYACTIVEREPLY._serialized_end=500
  _SPIKESORTERCOMMANDREQUEST._serialized_start=503
  _SPIKESORTERCOMMANDREQUEST._serialized_end=773
  _SPIKESORTERSTATE._serialized_start=776
  _SPIKESORTERSTATE._serialized_end=923
  _SPKSORTIOREQ._serialized_start=926
  _SPKSORTIOREQ._serialized_end=1055
  _SPIKESORTERLAUNCHREPLY._serialized_start=1058
  _SPIKESORTERLAUNCHREPLY._serialized_end=1201
  _GETSPIKESORTERIDSREQUEST._serialized_start=1203
  _GETSPIKESORTERIDSREQUEST._serialized_end=1252
  _GETSPIKESORTERIDSREPLY._serialized_start=1254
  _GETSPIKESORTERIDSREPLY._serialized_end=1302
  _SPIKESORTERGETRASTERDATAREQUEST._serialized_start=1305
  _SPIKESORTERGETRASTERDATAREQUEST._serialized_end=1526
  _SPIKESORTERRASTERDATAREPLY._serialized_start=1529
  _SPIKESORTERRASTERDATAREPLY._serialized_end=1686
  _SPIKESORTERSTANDARDREQUEST._serialized_start=1688
  _SPIKESORTERSTANDARDREQUEST._serialized_end=1762
  _SPIKESORTERDASHBOARDREQUEST._serialized_start=1764
  _SPIKESORTERDASHBOARDREQUEST._serialized_end=1859
  _SPIKESORTERDYNAMIC._serialized_start=1862
  _SPIKESORTERDYNAMIC._serialized_end=2252
  _SPIKESORTERDYNAMIC_CRITERIA._serialized_start=2028
  _SPIKESORTERDYNAMIC_CRITERIA._serialized_end=2188
  _SPIKESORTERDYNAMIC_UPDATEPERIODSEC._serialized_start=2190
  _SPIKESORTERDYNAMIC_UPDATEPERIODSEC._serialized_end=2252
  _SPIKESORTERSETDYNAMICREQUEST._serialized_start=2255
  _SPIKESORTERSETDYNAMICREQUEST._serialized_end=2452
  _SPIKESORTERSETDYNAMICREQUEST_VARIANTENTRY._serialized_start=2378
  _SPIKESORTERSETDYNAMICREQUEST_VARIANTENTRY._serialized_end=2452
  _SPIKESORTERGETDYNAMICREPLY._serialized_start=2455
  _SPIKESORTERGETDYNAMICREPLY._serialized_end=2671
  _SPIKESORTERGETDYNAMICREPLY_VARIANTENTRY._serialized_start=2378
  _SPIKESORTERGETDYNAMICREPLY_VARIANTENTRY._serialized_end=2452
  _GETSPIKESORTERPARAMCOMMANDREPLY._serialized_start=2673
  _GETSPIKESORTERPARAMCOMMANDREPLY._serialized_end=2781
  _CLUSTERMAPOUTLIERS._serialized_start=2783
  _CLUSTERMAPOUTLIERS._serialized_end=2834
  _CLUSTERMAPQUARTILES._serialized_start=2836
  _CLUSTERMAPQUARTILES._serialized_end=2893
  _CLUSTERMAPSTATS._serialized_start=2896
  _CLUSTERMAPSTATS._serialized_end=3027
  _CLUSTERMAPRECORD._serialized_start=3029
  _CLUSTERMAPRECORD._serialized_end=3131
  _SPIKESORTSITESTATUS._serialized_start=3134
  _SPIKESORTSITESTATUS._serialized_end=3302
  _SPIKESORTPHASESTATUS._serialized_start=3305
  _SPIKESORTPHASESTATUS._serialized_end=3448
  _SPIKESORTNBRIDXLIST._serialized_start=3450
  _SPIKESORTNBRIDXLIST._serialized_end=3492
  _SPIKESORTERSTATUSREPLY._serialized_start=3495
  _SPIKESORTERSTATUSREPLY._serialized_end=3865
  _SPIKESORTERSTATUSVARIANTSREPLY._serialized_start=3867
  _SPIKESORTERSTATUSVARIANTSREPLY._serialized_end=3949
  _SPIKESORTERCLASSIFIERSPEC._serialized_start=3952
  _SPIKESORTERCLASSIFIERSPEC._serialized_end=4333
  _SPIKESORTERVARIANTSPEC._serialized_start=4335
  _SPIKESORTERVARIANTSPEC._serialized_end=4452
  _SPIKESORTERSPEC._serialized_start=4455
  _SPIKESORTERSPEC._serialized_end=4659
  _SPIKESORTERGETCONFIGREPLY._serialized_start=4662
  _SPIKESORTERGETCONFIGREPLY._serialized_end=4856
  _SPIKESORTERVIZREQUEST._serialized_start=4859
  _SPIKESORTERVIZREQUEST._serialized_end=5131
  _SPIKESORTERVIZREQUEST_VTYPE._serialized_start=5092
  _SPIKESORTERVIZREQUEST_VTYPE._serialized_end=5131
  _SPIKESORTERCLUSTERERPARAMSREQUEST._serialized_start=5133
  _SPIKESORTERCLUSTERERPARAMSREQUEST._serialized_end=5254
  _SPIKESORTERFEATUREPARAMSREQUEST._serialized_start=5257
  _SPIKESORTERFEATUREPARAMSREQUEST._serialized_end=5401
  _SPIKESORTERFEATUREPARAMSREPLY._serialized_start=5404
  _SPIKESORTERFEATUREPARAMSREPLY._serialized_end=5607
  _SPIKESORTERDASHBOARDREPLY._serialized_start=5610
  _SPIKESORTERDASHBOARDREPLY._serialized_end=6304
  _SPIKESORTERDASHBOARDREPLY_PORTSTATSENTRY._serialized_start=6040
  _SPIKESORTERDASHBOARDREPLY_PORTSTATSENTRY._serialized_end=6122
  _SPIKESORTERDASHBOARDREPLY_SITEPANELENTRY._serialized_start=6124
  _SPIKESORTERDASHBOARDREPLY_SITEPANELENTRY._serialized_end=6211
  _SPIKESORTERDASHBOARDREPLY_NEURONPANELENTRY._serialized_start=6213
  _SPIKESORTERDASHBOARDREPLY_NEURONPANELENTRY._serialized_end=6304
  _SPIKESORTERDASHBOARDGENERALREC._serialized_start=6307
  _SPIKESORTERDASHBOARDGENERALREC._serialized_end=6735
  _SPIKESORTERDASHBOARDAI._serialized_start=6738
  _SPIKESORTERDASHBOARDAI._serialized_end=6951
  _INDICODASHBOARDSITESTATS._serialized_start=6953
  _INDICODASHBOARDSITESTATS._serialized_end=7048
  _INDICODASHBOARDPORTSTATS._serialized_start=7051
  _INDICODASHBOARDPORTSTATS._serialized_end=7195
  _INDICODASHBOARDSITEINDICATORS._serialized_start=7198
  _INDICODASHBOARDSITEINDICATORS._serialized_end=7415
  _INDICODASHBOARDNEURONINDICATORS._serialized_start=7418
  _INDICODASHBOARDNEURONINDICATORS._serialized_end=7595
  _SPIKESORTERDASHBOARDSITEDESC._serialized_start=7598
  _SPIKESORTERDASHBOARDSITEDESC._serialized_end=7893
  _SPIKESORTERDASHBOARDNEURONDESC._serialized_start=7896
  _SPIKESORTERDASHBOARDNEURONDESC._serialized_end=8106
  _SPIKESORTERDASHBOARDNEURONDETAIL._serialized_start=8109
  _SPIKESORTERDASHBOARDNEURONDETAIL._serialized_end=8359
  _SPIKESORTERDASHBOARDSITEDETAIL._serialized_start=8362
  _SPIKESORTERDASHBOARDSITEDETAIL._serialized_end=8531
# @@protoc_insertion_point(module_scope)
