import os
import ROOT
import subprocess


class PlotLayers:
    def __init__(self):
        self.name = "histoLayers"
        self.outputDir = "../plots/"
        self.titles = ["x","y","layer"]
        self.inputFile = None
        self.histoBaseName =""
        self.varTag = "LAYER"
        self.event = 0
        self.setPlotStyle()
        self.slices = []

    def retrieveLayers(self):
        if not os.path.isdir(self.outputDir):
            os.makedirs(self.outputDir)
        binHisto = self.inputFile.Get(self.histoBaseName+"_BIN_"+self.varTag)
        if not binHisto:
            raise StandardError("Cannot find bin histo "+self.histoBaseName)
        binHisto.__class__ = ROOT.TH1F
        nlayers = int(binHisto.GetBinContent(1))
        nevents = 0
        if len(self.varTag.split("_"))==2:
            nlayers = int(binHisto.GetBinContent(2))
            nevents = int(binHisto.GetBinContent(1))
        if self.event>nevents:
            raise StandardError("#event="+str(nevents))

        hSlices = []
        maxs = []
        for j in range(0,nlayers):
            i = self.event*nlayers+j
            hSlice = self.inputFile.Get(self.histoBaseName+str(i))
            if not hSlice:
                raise StandardError("Cannot find layer "+str(i)+" for "+self.histoBaseName)
            hSlice.__class__ = ROOT.TH1F
            hSlices.append(hSlice)
            maxs.append(hSlice.GetMaximum())
        maxi = max(maxs)

        canvas = []
        pngFiles = []
        for i,hSlice in enumerate(hSlices):
            canvas.append(ROOT.TCanvas("c_"+hSlice.GetName(), "c_"+hSlice.GetName(), 600, 600))
            hSlice.SetAxisRange(0.,maxi,"Z")
            hSlice.SetContour(99)
            hSlice.SetXTitle(self.titles[0])
            hSlice.SetYTitle(self.titles[1])
            xmin = hSlice.GetXaxis().GetBinLowEdge(0)
            xmax = hSlice.GetXaxis().GetBinUpEdge(hSlice.GetNbinsX())
            ymin = hSlice.GetYaxis().GetBinLowEdge(0)
            ymax = hSlice.GetYaxis().GetBinUpEdge(hSlice.GetNbinsY())
            leg = ROOT.TLatex(xmin+(xmax-xmin)*0.1, ymax+(ymax-ymin)*0.02, "Layer "+str(i))
            hSlice.Draw("colz")
            leg.Draw()
            canvas[-1].Print(self.outputDir+"/"+self.name+"_"+str(i)+".png")
            pngFiles.append(self.outputDir+"/"+self.name+"_"+str(i)+".png")
            #canvas[-1].Write()
            i += 1
        #outputFile.Close()

        command = ["convert", "-delay", "50"]
        for png in pngFiles:
            command.append(png)
        command.append("-loop")
        command.append("0")
        command.append(self.outputDir+"/"+self.name+"_anim.gif")
        subprocess.call(command)

    def setPlotStyle(self):
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gStyle.SetOptStat()
        ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetFrameLineWidth(1)
        ROOT.gStyle.SetPadBottomMargin(0.13)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        ROOT.gStyle.SetPadTopMargin(0.06)
        ROOT.gStyle.SetPadRightMargin(0.13)

        ROOT.gStyle.SetLabelFont(42,"X")
        ROOT.gStyle.SetLabelFont(42,"Y")
        ROOT.gStyle.SetLabelSize(0.05,"X")
        ROOT.gStyle.SetLabelSize(0.05,"Y")
        ROOT.gStyle.SetLabelOffset(0.01,"Y")
        ROOT.gStyle.SetTickLength(0.04,"X")
        ROOT.gStyle.SetTickLength(0.04,"Y")
        ROOT.gStyle.SetLineWidth(1)
        ROOT.gStyle.SetTickLength(0.04 ,"Z")

        ROOT.gStyle.SetTitleSize(0.1)
        ROOT.gStyle.SetTitleFont(42,"X")
        ROOT.gStyle.SetTitleFont(42,"Y")
        ROOT.gStyle.SetTitleSize(0.05,"X")
        ROOT.gStyle.SetTitleSize(0.05,"Y")
        ROOT.gStyle.SetTitleOffset(1.1,"X")
        ROOT.gStyle.SetTitleOffset(1.5,"Y")
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetPalette(1)
        ROOT.gStyle.SetPaintTextFormat("3.2f")
        ROOT.gROOT.ForceStyle()

 

