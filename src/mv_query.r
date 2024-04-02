
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

fLoadLib(c("httr2", "jsonlite", "dplyr"))

CLOUDERA_FLINK_MV_URL <- "http://localhost:18131/api/v1/query/5195/summary?key=e148580d-875a-4906-b46c-f6e28b3990e8&limit=1000"

req <- request(CLOUDERA_FLINK_MV_URL) 
req <- req %>% req_headers("Accept" = "application/json")
resp <- req_perform(req)
resp <- resp %>% resp_body_json()
resp
class(resp)


