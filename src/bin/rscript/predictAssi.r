
calculate_metrics_apply_prediction <- function(act_assi){
	act_assi$PErr <- 1.0 - act_assi$nPrdCorAssi/act_assi$nPrdAssi
	act_assi$PErr[is.na(act_assi$PErr)] <- 0.5
	act_assi$TrPErr <- 1.0 - act_assi$nLogPrdCorAssi/act_assi$nLogPrdAssi
	act_assi$TrPErr[is.na(act_assi$TrPErr)] <- 0.5

	act_assi$MaxSNExp <- act_assi$cntMaxExp
	act_assi$SNSize <- act_assi$cntN	
	act_assi$AvgSNDep <- act_assi$cmtN / (act_assi$cntN + 1)
	act_assi$P <- as.factor(as.character(act_assi$new))

	act_assi
}

predict_from_file <- function(file, modelFile){
	act_assi <- read.table(file, sep=";", header=T)
	
	predict_share(modelFile, act_assi)
}

predict_from_input <- function(modelFile, nPrdCorAssi, nPrdAssi, nLogPrdCorAssi, nLogPrdAssi, cntMaxExp, cntN, cmtN, new){
	act_assi <- data.frame(nPrdCorAssi, nPrdAssi, nLogPrdCorAssi, nLogPrdAssi, cntMaxExp, cntN, cmtN, new)
	
	predict_share(modelFile, act_assi)
}

predict_share <- function(modelFile, act_assi){
	act_assi <- calculate_metrics_apply_prediction(act_assi)
	load(modelFile)
	prd <- predict(glm_assi, act_assi)
	prd <- exp(prd)/(1+exp(prd))

	prd
}


