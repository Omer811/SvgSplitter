import copy,os,sys
import xml.etree.ElementTree as ET

USAGE = "USAGE: python3 splitter.py <multi-layer svg file> " \
          "<output-folder>"

OUTPUT_FILE_FORMAT = ".svg"

FILE_NOT_FOUND = "ERROR: svg file not found"


class Splitter:

    def __init__(self, filePath=None, outputDir=None):
        self.filePath = filePath
        self.outputDir = outputDir

    def setSvgFile(self, filePath):
        self.filePath = filePath

    def splitSvgFile(self):
        if not os.path.exists(self.filePath):
            print(FILE_NOT_FOUND)
        if not os.path.exists(self.outputDir):
            os.mkdir(self.outputDir)
        self._splitLayers()

    def _splitLayers(self):
        my_namespaces = dict([node for _, node in
                              ET.iterparse(self.filePath,
                              events=['start-ns'])])  # collect
        # all namespaces
        for ns in my_namespaces:
            ET.register_namespace(ns, my_namespaces[ns])  # register all
            # namespeces
        tree = ET.parse(self.filePath)
        root = tree.getroot()
        for child in root:
            svgLayer = ET.Element('svg')
            svgLayer.tag = root.tag  # copy xmls tag
            for key in root.attrib:  # copy attributes of main svg tag
                svgLayer.set(key, root.attrib[key])
            svgLayer.append(
                copy.copy(child))  # add a copy of the current child

            layerFilePath = self.outputDir + "/" + child.attrib["id"] + OUTPUT_FILE_FORMAT

            layerFile = open(layerFilePath, "w")
            layerFile.write(str(ET.tostring(svgLayer, encoding="unicode")))
            layerFile.close()

def main():
    if len(sys.argv) != 3:
        print(USAGE)
        exit()
    spl = Splitter(sys.argv[0],sys.argv[1])
    spl.splitSvgFile()

if __name__ == "__main__":
    main()
#parser = Splitter("/Users/omerdvora/Downloads/Main.svg",
# "/Users/omerdvora/Downloads/Main")
# parser.splitSvgFile()
# parser._splitLayers()
