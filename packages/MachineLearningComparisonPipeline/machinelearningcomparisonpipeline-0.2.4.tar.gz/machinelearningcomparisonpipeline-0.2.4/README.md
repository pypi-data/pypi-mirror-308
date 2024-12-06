![Pipeline Logo](designer.png " ") 
# machine-learning-comparison-pipeline

Analysis of classification through machine learning is often accomplished with what the researcher is most comfortable
using in the analysis. But that does not mean that the most optimal learner was selected for the research question. It
is also often that feature selection is performed, but only with minimal processing with variation in the selection 
process.

During the analysis of a series of acoustic measurement from candidate propellers designed by the United States Air
Force Academy it was determined that the 711th Human Performance Wing did not want to fall into these limitations. 
The wing developed a importance getter function using sensitivity analysis to determine the feature importance. This
method was applied to random decision forests, support vector machines, neural networks, logistic regressions, and 
nearest neighbor machine learners. 

This package was developed from that research in effort to canonize the process for future work.

#   Usage
##  Define the inputs to the class, including the feature DataFrame, targets Series, the learners and cross-validation

    clf1 = nn.KNeighborsClassifier(n_neighbors=5)
    clf2 = nn.KNeighborsClassifier(n_neighbors=5, weights='distance')
    learners = list([clf1, clf2])
    cv = ms.KFold(n_splits=10)
    dataset = pd.read_csv(str(pathlib.Path(__file__).parents[1]) + '/data/features.csv')
    features = dataset.iloc[:, 1:74]
    targets = dataset['PROPELLER']
    pipe = pipeline.ProcessingPipeline(learners, cv, features, targets)

    pipe.process(72, verbose=True)
	
Cleared for public release on 14 November 2024 with case number AFRL-2024-6348.