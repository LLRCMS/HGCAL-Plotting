import ROOT
from PlotLayers import PlotLayers


inputFile = ROOT.TFile.Open("histos/histos.root")
#
# Single events
for evt in range(0,10):
    layers = PlotLayers()
    layers.name = "single_electron_xy_"+str(evt)
    layers.outputDir = "plots/SingleEvents_xy/Event_"+str(evt)
    layers.inputFile = inputFile
    layers.histoBaseName = "hStudyGunInHGCAL_hit_xy_vs_layer_evt"
    layers.varTag = "EVENT_LAYER"
    layers.event = evt
    layers.retrieveLayers()
    #
    layers = PlotLayers()
    layers.name = "single_electron_dxy_"+str(evt)
    layers.outputDir = "plots/SingleEvents_dxy/Event_"+str(evt)
    layers.inputFile = inputFile
    layers.histoBaseName = "hStudyGunInHGCAL_hit_dxy_vs_layer_evt"
    layers.titles = ["dx","dy","layer"]
    layers.varTag = "EVENT_LAYER"
    layers.event = evt
    layers.retrieveLayers()

for eta in range(1,5):
    layers = PlotLayers()
    layers.name = "integral_electron_dxy_Eta"+str(eta)
    layers.outputDir = "plots/IntegratedEvents_dxy/Eta_"+str(eta)
    layers.inputFile = inputFile
    layers.histoBaseName = "hStudyGunInHGCAL_hit_dxy_eta"+str(eta)+"_vs_layer"
    layers.titles = ["dx","dy","layer"]
    layers.varTag = "LAYER"
    layers.retrieveLayers()

inputFile.Close()
