#!/usr/bin/env python

# BSD Licensed, Copyright (c) 2006-2010 TileCache Contributors

import sys, urllib, urllib2, time, os, math
import time
import httplib
try:
    from optparse import OptionParser
except ImportError:
    OptionParser = False 

from shapely.wkt import loads
from shapely.geometry import Point,Polygon,MultiPolygon

# setting this to True will exchange more useful error messages
# for privacy, hiding URLs and error messages.
HIDE_ALL = False 


def seed (layer, levels = (0, 5), bbox = None, zone = "", path_to_tiles= "", delete = False):
    from Layer import Tile

    if not bbox: bbox = layer.bbox

    geom_filter = loads(zone)

    for z in range(*levels):
        bottomleft = layer.getClosestCell(z, bbox[0:2])
        topright   = layer.getClosestCell(z, bbox[2:4])

        print "###### %s, %s" % (bottomleft, topright)
        zcount = 0 
        metaSize = (1,1)
        ztiles = int(math.ceil(float(topright[1] - bottomleft[1]) / metaSize[0]) * math.ceil(float(topright[0] - bottomleft[0]) / metaSize[1]))
        
        startX = topright[0] + metaSize[0]
        endX = bottomleft[0]
        stepX = -metaSize[0]
        startY = topright[1] + metaSize[1]
        endY = bottomleft[1]
        stepY = -metaSize[1]
        
        for y in range(startY, endY, stepY):
            for x in range(startX, endX, stepX):
                tile = Tile(layer,x,y,z)
                bounds = tile.bounds()
    
                tile_wkt = "POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))" % (bounds[0], bounds[1], bounds[0], bounds[3], bounds[2], bounds[3], bounds[2], bounds[1], bounds[0], bounds[1])
                tile_geom = loads(tile_wkt)
                intersect =  geom_filter.intersects(tile_geom)
                
                if not intersect:
                    # Then delete the tile
                    zcount += 1
                    file_to_del = "%s/%s/%d/%d/%d.%s" % (path_to_tiles,layer.name, z, x, y, layer.extension)
                    if not delete:
                        print "To be deleted : %s" % (file_to_del)
                    else :
                        try:
                            os.remove(file_to_del)
                            print "File deleted : %s" % (file_to_del)
                        except:
                            print "File not found : %s" % (file_to_del)
                            pass
                        

def main ():
    if not OptionParser:
        raise Exception("TileCache cleaner requires optparse/OptionParser. Your Python may be too old.\nSend email to the mailing list \n(http://openlayers.org/mailman/listinfo/tilecache) about this problem for help.")
    usage = "usage: %prog <layer> [<zoom start> <zoom stop>]"
    
    parser = OptionParser(usage=usage, version="%prog $Id: Cleaner.py 406 2010-10-15 11:00:18Z sbeorchia inspired by Client.py $")
    
    parser.add_option("-b","--bbox",action="store", type="string", dest="bbox", default = None,
                      help="restrict to specified bounding box")
    parser.add_option("-c", "--config", action="store", type="string", dest="tilecacheconfig", 
        default=None, help="path to configuration file")                 
   
    parser.add_option("-z","--zone", action="store", type="string", dest="zone", default = False,
                      help="define the filter zone")

    parser.add_option("-d","--delete", action="store_true", dest="delete", default = False,
                      help="define if the tile are to be deleted")
                      
    (options, args) = parser.parse_args()
    
    if len(args) > 4:
        parser.error("Incorrect number of arguments. bbox and padding are now options (-b and -p)")

    from Service import Service, cfgfiles
    from Layer import Layer
    cfgs = cfgfiles
    if options.tilecacheconfig:
        configFile = options.tilecacheconfig
        print "Config file set to %s" % (configFile)
        cfgs = cfgs + (configFile,)
 
    svc = Service.load(*cfgs)

    layer = svc.layers[args[0]]

    if options.bbox:
        bboxlist = map(float,options.bbox.split(","))
    else:
        bboxlist=None
        
    if len(args)>1:    
        seed(layer, map(int, args[1:3]), bboxlist , zone = options.zone, path_to_tiles = layer.cache.basedir, delete = options.delete)

if __name__ == '__main__':
    main()
