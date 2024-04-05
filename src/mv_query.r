
fLoadLib <- function(pkgs, repo='http://cran.rstudio.com', deps=TRUE)
{
# Downloaded the package if not already present
  downloadNeeded <- pkgs[which(!pkgs %in% installed.packages()[, 1])]
  if (length(downloadNeeded) > 0) 
  {
    tryCatch( {
      install.packages(downloadNeeded, repos=repo, dependencies=deps)
    }, 
    warning = function(w) {
      stop(w)    
    },
    error = function(e) {
      stop(e)    
    }) 
  }
# Load the package if not already attached
  searchPkgs <- search()
  alreadyLoaded <- searchPkgs[grepl("package", searchPkgs)]
  libraryNeeded <- pkgs[which(!pkgs %in% gsub("package:", "", alreadyLoaded))]
  n <- length(libraryNeeded)
  if (n > 0) {
    for (i in 1:n) require(libraryNeeded[i], character.only=TRUE)
  }
}

fLoadLib(c("httr2", "jsonlite", "dplyr", "tidyjson", "data.table", "ggplot2", "osmdata", "showtext", "ggtext", "tidyr"))

CLOUDERA_FLINK_MV_URL <- "http://localhost:18131/api/v1/query/5195/summary?key=e148580d-875a-4906-b46c-f6e28b3990e8&limit=1000"

req <- request(CLOUDERA_FLINK_MV_URL) 
req <- req %>% req_headers("Accept" = "application/json")
resp <- req_perform(req)
resp <- resp %>% resp_body_json()
class(resp)

mv_data <- as.data.frame(do.call(rbind, resp))
mv_source <- cbind(mv_data, purrr::map_dfr(mv_data$location, fromJSON)) 
save(mv_source, file="/Users/statisticalfx/Documents/GitHub/simulator_fraudulent_transactions/demo/example_mv_data_frame.txt")
load("/Users/statisticalfx/Documents/GitHub/simulator_fraudulent_transactions/demo/example_mv_data_frame.txt")
  
setDT(mv_source)
class(mv_source)

 mv_source[, .N, by = sapply(location, paste)]
 mv_source[, .(total = sum(sapply(total_amount, as.numeric))), by = sapply(window_end, paste)]

available_features()
available_tags(feature = "highway")
print(n = 100, available_tags(feature = "building"))

points_of_interest = c("apartments", "barracks", "college", "hotel", "house", "residential", "university")
sf_osm <- getbb(place_name = "San Francisco") %>%
  opq() %>%
  add_osm_feature(key = "building", 
                  value = points_of_interest) %>%
  osmdata_sf()



available_tags(feature = "water")
water_points_of_interest = c("basin", "canal", "lake", "pond", "reservoir", "river")
water_osm <- getbb("San Francisco") %>%
  opq() %>%
  add_osm_feature(key = "water", 
                  value = water_points_of_interest) %>%
  osmdata_sf()


print(n = 100, available_tags(feature = "natural"))
large_water_points_of_interest = c("bay", "beach", "coastline")
large_water_osm <- getbb("San Francisco") %>%
  opq() %>%
  add_osm_feature(key = "natural", 
                  value = large_water_points_of_interest) %>%
  osmdata_sf()

  
sf_osm
Object of class 'osmdata' with:
                 $bbox : 37.6403143,-123.173825,37.929811,-122.281479
        $overpass_call : The call submitted to the overpass API
                 $meta : metadata including timestamp and version numbers
           $osm_points : 'sf' Simple Features Collection with 213297 points
            $osm_lines : 'sf' Simple Features Collection with 6 linestrings
         $osm_polygons : 'sf' Simple Features Collection with 21676 polygons
       $osm_multilines : 'sf' Simple Features Collection with 4 multilinestrings
    $osm_multipolygons : 'sf' Simple Features Collection with 108 multipolygons

big_streets_osm <- getbb("San Francisco")%>%
  opq()%>%
  add_osm_feature(key = "highway", 
                  value = c("motorway", "primary", "motorway_link", "primary_link")) %>%
  osmdata_sf()

bayshore_highway_freeway <- big_streets_osm[["osm_lines"]] %>% 
  filter(name=="Bayshore Freeway")

railway_osm <- getbb("San Francisco")%>%
  opq()%>%
  add_osm_feature(key = "railway", value="rail") %>%
  osmdata_sf()

target_streets = big_streets_osm$osm_lines[, c("name", "geometry")]
target_streets %>% drop_na %>% arrange(name) %>% View()


font_size = 3
font_add_google(name = "Lato", family = "lato")
showtext_auto()
ggplot() +
  geom_sf(data = sf_osm$osm_polygons,
          inherit.aes = FALSE,
          color = "black") +
  geom_sf(data = big_streets_osm$osm_lines,
          inherit.aes = FALSE,
          color = "black",
          size = .3,
          alpha = .5) +
  geom_sf(data = railway_osm$osm_lines,
          inherit.aes = FALSE,
          color = "green",
          size = .2,
          linetype="dotdash",
          alpha = .5) +
  geom_sf(data = bayshore_highway_freeway, # Identify Bayshore Freeway
          inherit.aes = FALSE,
          color = "orange",
          size = 1,
          alpha = 1) +
  geom_sf(data = water_osm$osm_polygons,
        inherit.aes = FALSE,
        alpha = 1,
        color = NA,
        fill = "lightblue") + 
  geom_sf(data = large_water_osm$osm_multipolygons,
        inherit.aes = FALSE,
        alpha = 1,
        color = NA,
        fill = "lightblue") + 
  geom_richtext(
          size = font_size,
          hjust = 0.2, vjust = 0.2,
          aes(x = -122.37, y = 37.7, label = "Bayshore_Freeway"),
          fill = NA, label.color = NA,
          label.padding = grid::unit(rep(0, 4), "pt")) +
  geom_richtext(
          size = font_size,
          hjust = 0.2, vjust = 0.2,
          aes(x = -122.38, y = 37.89, label = "Martinez_Subdivision"),
          fill = NA, label.color = NA,
          label.padding = grid::unit(rep(0, 4), "pt")) +
  geom_richtext(
          size = font_size,
          hjust = 0.2, vjust = 0.2,
          aes(x = -122.37, y = 37.74, label = "3rd_Street"),
          fill = NA, label.color = NA,
          label.padding = grid::unit(rep(0, 4), "pt")) +
  geom_richtext(
          size = font_size,
          hjust = 0.2, vjust = 0.2,
          aes(x = -122.4081, y = 37.645, label = "Airport_Boulevard"),
          fill = NA, label.color = NA,
          label.padding = grid::unit(rep(0, 4), "pt")) +
  geom_richtext(
          size = font_size,
          hjust = 0.2, vjust = 0.2,
          aes(x = -122.42, y = 37.92, label = "Frontage_Road"),
          fill = NA, label.color = NA,
          label.padding = grid::unit(rep(0, 4), "pt")) +
  theme_void() +
  theme(plot.title = element_text(size = 20, family = "lato", face="bold", hjust=.5),
        plot.subtitle = element_text(family = "lato", size = 8, hjust=.5, margin=margin(2, 0, 5, 0))) +
  labs(title = "SAN FRANCISCO BAY", subtitle = "green=Railway, black=Highway", x = NULL, y = NULL) 


