setwd('C:/Users/Rui/Desktop/nba')
library(clValid)
library(ape)
library(colorRamps)
library(colorspace)
csvfiles<-"C:/Users/Rui/Desktop/nba/021617allcluster.csv"
MyData <- read.csv(file=csvfiles, header=TRUE, sep=",")
head(MyData,5)
players <- subset( MyData, select = -X )
row.names(players) <-MyData$'X'

players <- subset( players, select = -total )
players <- subset( players, select = -X.all )
##players <- subset( players, select = -run.D )
##players <- subset( players, select = -r.dif )
##players <- subset( players, select = -dist.D )
##players <- subset( players, select = -X.diff )
##players2<-scale(players, center = TRUE, scale = TRUE)
medians = apply(players,2,median)
mads = apply(players,2,mad)
players2 = scale(players,center=medians,scale=mads)
players3<-data.frame(players2)
players3$X.diff<-players3$X*sqrt(10)
clmethods <- c("hierarchical","kmeans","pam")
intern <- clValid(players2, nClust = 5:8,
              clMethods = clmethods, validation = "internal")
# Summary
summary(intern)
plot(intern)
stab <- clValid(players2, nClust = 5:8, clMethods = clmethods,
                validation = "stability")
optimalScores(stab)
plot(stab)

player_clusters <- dist(players2, method = "euclidean")
res.hc <- hclust(player_clusters, method = "ward.D2" )
# Cut tree into 4 groups
grp <- cutree(res.hc, k = 5)
# Visualize
##tiff("plotcluster5.tiff",width = 1800, height = 1800, res = 300)
##plot(res.hc, cex = 0.3, hang=-1) # plot tree
##rect.hclust(res.hc, k = 5, border = 2:5) # add rectangle
##dev.off()

source("plotBranchbyTrait.R") # load source
tiff("plotcluster5d9.tiff",width = 1800, height = 1800, res = 300)
plotBranchbyTrait(res.hc,players$X.,mode="edges",palette="colord")
##rect.hclust(res.hc, k = 5, border = 2:5) # add rectangle
dev.off()

players4<-data.frame(players,grp)
c1<-players4[players4$grp==1,]
c2<-players4[players4$grp==2,]
c3<-players4[players4$grp==3,]
c4<-players4[players4$grp==4,]
c5<-players4[players4$grp==5,]
c6<-players4[players4$grp==6,]
c7<-players4[players4$grp==7,]
c8<-players4[players4$grp==8,]
colMeans(c1)
colMeans(c2)
colMeans(c3)
colMeans(c4)
colMeans(c5)
colMeans(c6)
colMeans(c7)
colMeans(c8)

> colMeans(c1)
          X.        r.dif       dist.D        run.D          grp 
-0.002972003  0.779608493  0.475163940  0.820582384  1.000000000 
> colMeans(c2)
         X.       r.dif      dist.D       run.D         grp 
-0.02943269  1.93048969 -0.35912726  0.11342435  2.00000000 
> colMeans(c3)
         X.       r.dif      dist.D       run.D         grp 
-0.11646847  0.01004611 -0.25688115  0.99473698  3.00000000 
> colMeans(c4)
         X.       r.dif      dist.D       run.D         grp 
 0.07063814 -1.00812463 -1.20201093  0.11980896  4.00000000 
> colMeans(c5)
        X.      r.dif     dist.D      run.D        grp 
0.06591457 0.89286663 2.26391636 0.21181662 5.00000000 
