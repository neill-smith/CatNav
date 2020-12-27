# CatNavDownloader

Download utility for Here maps updates for Jaguar Touch Pro Sat Nav. You will need a subscription to maps for this to work.

Replicates the provided MapDownloader utility with following benefits:
 * Portable Python command line tool - should work on Mac, Linux, Windows
 * Higher performance - Europe Map can be downloaded in <15 minutes with a fast connection.
 * Download to a folder on local disk - Copy the HereV1 folder to a USB drive at a convenient time when the download is complete.

Use at your own risk - not testsed against more than one car or with a region other than Europe. This may break your Sat Nav!

Contributions and reports of success or failure welcomed.

## Usage

You will need a 'catalog' URL from the http://www.jaguar.here.com website. This is personalised to your login (the downloaded map is locked to your car's VIN). Get this by copying the URL from the link on the 'Download Map' button where you would normally click to launch the MapUpdater application. This should start with heremapdownloader://delivery.cc.api.here.com/delivery/*/. These catalog links expire after ~48 hours.

Run CatNavDownloader.py -u <the catalog URL> -d <destination folder>. A HereV1 folder will be created in the destination folder. The car looks for this folder in the root of the drive when you plug in a USB stick. You can either download direct to a USB drive or download locally and copy the folder later.
  
You will see 'Done!' printed when the download is complete.
  
You can kill the utility at any point and run it again to resume the download. The catalog contains checksums for each data file and these are verified each time the utility is run. Any missing or incomplete files are downloaded again. 

## Future

Ideas for the future:
 * It may be possible to avoid downloading the map data for every different car. If anyone has two cars with Touch Pro and is willing to share the catalog files please get in touch.
 * Resume download of partially downloaded files. The largest files are >1GB so this could represent a worthwhile saving.

