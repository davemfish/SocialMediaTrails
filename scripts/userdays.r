### 9 May 2016 - DMF
###
###   This script computes photo user days
###      for every polygon in the provided shapefile
###      using all geolocated photos in flickr from 20050101 - 20141231
###      stored in individual csv files for each year

### USAGE: Rscript userdays.r shp/aoi.shp > userdays.out

# the single argument is relative path to aoi shapefile

### Photo files should be like:

# photo_id,owner_name,date_taken,latitude,longitude,accuracy
# 219208114,53231487@N00,2005-04-29 18:00:41,48.208201,16.372718,12
# 219209109,46083256@N00,2005-07-10 11:18:46,37.867811,-122.25764,16
# 219211262,46083256@N00,2005-07-10 12:57:29,37.802231,-122.418015,16
# 219211144,46083256@N00,2005-07-10 12:46:06,37.800128,-122.410644,16
# 219211609,46083256@N00,2005-07-10 16:45:13,37.785766,-122.408251,15


### AOI shapefile should be anything with a projection defined
### unproject it ahead of time to wgs84 lon/lat if you prefer 
### not to trust spTransform() to do it on lines 80-89

###   This script returns daily photo-user counts per polygon
###   those counts can by summed to monthly or yearly totals 
###   using globalrec/flickr/post-ud-locations.r (that script does other stuff too)


library(SearchTrees)
library(rgdal)
require(rgeos)
library(raster)
library(dplyr)
library(readr)
# library(feather)

args=(commandArgs(TRUE))

if(length(args)!=1){
    print("userdays.r takes only 1 argument (aoi.shp)")
    stop
} else {
    aoipath <- args[1]
    shpname <- sub(x=basename(aoipath), pattern=".shp$", replacement="")
}

########################
### SET PARAMS BELOW IF:
### this script is not being called from userdays-locations.sh
########################

workingdir <- "."                          

outpath <- file.path(workingdir, "output")

## Set photos by pointing to dir of csv files
csvpath <- file.path("/home/dfisher5/flickrphotos") ## the latest flickr tables. Includes usernames.
# csvpath <- file.path("/home/dmf/Recdev/flickrphotos") ## local path for development
photofiles <- list.files(csvpath, pattern="*.csv$")
## OR an individual file
# photofiles <- "allpics_2100.csv"

setwd(workingdir)

### Load A Shapefile
# shpname <- "nps_boundary"
AOIpolys <- shapefile(aoipath)
## Choose 1: 
## Create a unique ID field for the shapefile, or use existing field 
polyIDs <- sapply(slot(AOIpolys, "polygons"), function(x) slot(x, "ID"))
# polyIDs <- AOIpolys@data$ID
AOIpolys@data$pid <- as.numeric(polyIDs)
writeOGR(AOIpolys, dsn="shp", paste0(shpname, "_pid"), driver="ESRI Shapefile", overwrite=T)


########################
########################
########################

### Re-project AOI to match photo's CRS, if necessary
prj <- projection(AOIpolys)
print(paste("AOI: ", prj))

if (grepl("\\+proj=longlat\\s+\\+datum=WGS84", prj)){
  print("Checking AOI CRS...OK")
} else {
  print("AOI CRS does not match photo's CRS....transforming to longlat WGS84")
  AOIpolys <- spTransform(AOIpolys, CRS=CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"))
}


### DEFINE FUNCTIONS ####

WriteOUT <- function(x, suffix){
  write.csv(x, file.path(outpath, paste(shpname, sub("\\.[^.]*$", "", photofiles[p]), paste0(suffix, ".csv"), sep="_")), row.names=F)
}


return_no_photo_users <- function(pid){
  users <- data.frame(pid=pid, owner_name=NA, date_taken=NA)
  return(list(users=users))
}

## INTERSECT CURRENT AOI POLYGON/CELL WITH QUADTREE
LookupPUD <- function(pgon, pid){
  ## for debugging: pgon=AOIpolys[75,]; pid=0

  inrect.ls <- list()
  ## sp objects already contain sub-polygons, so run rectLookup on those
  ## FOR each sub-polygon
  for (k in 1:length(pgon@polygons[[1]]@Polygons)){
    lons <- bbox(pgon@polygons[[1]]@Polygons[[k]])[1,]
    lats <- bbox(pgon@polygons[[1]]@Polygons[[k]])[2,]
    inrect.ls[[k]] <- rectLookup(tree, xlim=lons, ylim=lats)
  }
  ## aggregate subpolygons by unlisting
  ## prevent double-counting by keeping unique points
  inrect <- unique(unlist(inrect.ls))

  ## ## no photos returned from quadtree lookup?
  if (length(inrect) == 0) { 
    return(return_no_photo_users(pid=pid))
  } 
  
  ## rectLookup returned indices of points
  ## use indices to create SP object from the photos table
  ## overlay sp object with current polygon
  pics <- SpatialPointsDataFrame(coords=photos[inrect, c("longitude","latitude")], data=photos[inrect,], proj4string=CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"))
  a <- which(!is.na(over(pics, as(pgon, "SpatialPolygons"))))

  ## ## no photos after intersecting with the current polygon?
  if(length(a) == 0){
    return(return_no_photo_users(pid=pid))
  }

  ## subset the pics table with only pics inside the current polygon
  df <- pics@data[a, ]

  photo_ids <- cbind(pid, df$photo_id)
  names(photo_ids)[2] <- "photo_id"

  users.day <- unique(df[,c("owner_name", "date_taken")])
  users.day <- cbind(pid, users.day)

  return(list(users=users.day, photo_ids=photo_ids))
} 


#### RUN SCRIPT #####

## Compute PUD values
## ## Loop through each year of photos
# ptm <- proc.time()
for (p in 1:length(photofiles)){
  print(paste("IMPORTING", photofiles[p], proc.time()[3]))
  ptm <- proc.time()
  photos <- as.data.frame(read_csv(file.path(csvpath, photofiles[p]),
    col_names=TRUE,
    col_types= list(
    photo_id=col_character(),
    owner_name=col_character(),
    date_taken=col_character(),
    latitude=col_double(),
    longitude=col_double(),
    accuracy=col_skip())
    )) # as.data.frame wrapper required for passing photos to createTree()
  totaltime <- proc.time() - ptm
  
  if(nchar(photos$date_taken[1]) != 8){
      if(nchar(photos$date_taken[1]) == 19){
        newdates <- unlist(lapply(photos$date_taken, FUN=function(x){
          a <- strsplit(x, split=" ")[[1]][1]
          b <- gsub(a, pattern="-", replacement="", fixed=T)
        }))
        photos$date_taken <- newdates
      } else {
        stop("ERROR: Bad date format in photo's csv file")
      }
  }

  ## Create quadtree
  ## ## requires ~8 Gb memory for the global flickr collection
  ## ## takes a few mins to build the tree
  # specify either maxDepth or minNodeArea
  # option: maxBucket = max points allowed in a single node (not used)
  # For the globe, Depth 11 creates leaves ~0.18 degrees on a side
  # A 1km cell is approx 0.01 degrees on a side at 23N/S latitude
  
  print(paste("BUILDING QUADTREE FOR", photofiles[p], proc.time()[3]))
  photo_x <- which(names(photos) == "longitude")
  photo_y <- which(names(photos) == "latitude")
  tree <- createTree(photos, columns=c(photo_x, photo_y), dataType="point", maxDepth=11)
    
  print(paste("LOOKUP AND PUD FOR", photofiles[p], proc.time()[3]))
  pud <- list()
  for (i in 1:length(AOIpolys)) {
    if((i/1000) %% 1 == 0) { print(paste("SHAPE LOOP", i, proc.time()[3])) }
    pud[[i]] <- LookupPUD(AOIpolys[i,], pid=polyIDs[i])
  }

  print(paste("WRITING OUTPUT TABLES FOR", photofiles[p], proc.time()[3]))

  d.photoid <- lapply(pud, FUN=function(x){ 
    return(x$photo_ids) 
    })
  photoidout <- data.frame(do.call("rbind", d.photoid))
  WriteOUT(photoidout, "photoid")

  d.users <- lapply(pud, FUN=function(x){ 
      return(x$users)
    })
  usersout <- data.frame(do.call("rbind", d.users))
  WriteOUT(usersout, "users")
}

totaltime <- proc.time() - ptm