# What is PortPy?
PortPy (**P**lanning and **O**ptimization for **R**adiation **T**herapy) is a community effort to develop an open source python library to facilitate the development and clinical translation of radiotherapy cancer treatment planning algorithms. PortPy includes:
1. Research-ready data and code to promote *benchmarking*, *transparency*, *reproducibility* and *community-driven* development 
2. Interface to an open-source optimization package [CVXPy](https://www.cvxpy.org/) for easy/quick prototyping and out-of-the-box access to commercial/open-source optimization engines (e.g., Mosek, Gorubi, CPLEX, IPOPT)
3. Visualization modules to visualize releavant plan information (e.g, dose volume histograms, dose distribution, fluence map)
4. Evaluation modules to quantify plan quality with respect to established clinical metrics (e.g., RTOG metrics, dose conformality, tumor control probability, normal tissue control probability)
# Data
Data needed for optimization and algorithm development (e.g., a set of beams/beamlets/voxels, dose contribution of each beamlet to each voxel) are provided for a set of pre-specified machine parameters (e.g., beam/colimator/couch angles). We initially provide these data for a set of publicaly available dataset from [TCIA](https://www.cancerimagingarchive.net/). We hope to expand our dataset in the future. The data needed for optimization is extracted from the research version of Eclipse<sup>TM</sup> treatment planning system ([Varian Medical Systems](https://www.varian.com/)) using its API.       
# Team
PortPy is a community project initiated at [Memorial Sloan Kettering Cancer Center](https://www.mskcc.org/). It is currently developed and maintained by:
1. [Masoud Zarepisheh](https://masoudzp.github.io/) ([Memorial Sloan Kettering Cancer Center](https://www.mskcc.org/))
2. [Gourav Jhanwar](https://github.com/gourav3017) ([Memorial Sloan Kettering Cancer Center](https://www.mskcc.org/))
3. [Saad Nadeem](https://nadeemlab.org/) ([Memorial Sloan Kettering Cancer Center](https://www.mskcc.org/))
4. [Vicki Taasti](https://scholar.google.com/citations?user=PEPyvewAAAAJ&hl=en) ([Maastro Clinic, Netherlands](https://www.mskcc.org/))
5. [Seppo Tuomaala](https://www.linkedin.com/in/seppo-tuomaala-5b57913/) ([Varian Medical Systems](https://www.varian.com/))

# Installing PortPy
# License
PortPy code is distributed under **Apache 2.0 with Commons Clause** license, and is available for non-commercial academic purposes.

