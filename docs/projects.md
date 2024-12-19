# Winter Of Code Projects for PortPy

Working on AI/ML involves many different tools from data visualizations, model/algorithm development, evaluation and testing. Below is the list of projects that can help you to gain hands on experience with these tools.
## Index
### Visualization Tools
1. [Interactive and User-Friendly Visualization for Dose-Volume Histograms (DVH)](#interactive-and-user-friendly-visualization-for-dose-volume-histograms-dvh)
2. [Enhancing Dose Distribution Analysis through User-Friendly Visualization Tools](#enhancing-dose-distribution-analysis-through-user-friendly-visualization-tools)
3. [User-Friendly Interactive Dashboard for PortPy Data Visualization with Dynamic Tables](#user-friendly-interactive-dashboard-for-portpy-data-visualization-with-dynamic-tables)
4. [Interactive Visualization of Multi-Leaf Collimator (MLC) Movements for Treatment Plans](#interactive-visualization-of-multi-leaf-collimator-mlc-movements-for-treatment-plans)

### Website Development
5. [Creating a Simple Website for PortPy](#creating-a-simple-website-for-portpy)

### AI/ML applications
6. [Implementing Top-Performing Dose Prediction Model (Cascade 3D U-Net)](#implementing-top-performing-dose-prediction-model-cascade-3d-u-net)
7. [Building Dose Prediction using Advanced U-Net Architecture (Dilated U-Net)](#building-dose-prediction-using-advanced-u-net-architecture-dilated-u-net)
8. [Feature-Based Dose Prediction with Enhanced Accuracy](#feature-based-dose-prediction-with-enhanced-accuracy)

### Optimization Techniques
10. [Gradient-Based Optimization for Radiotherapy](#gradient-based-optimization-for-radiotherapy)
11. [Multi-GPU-Based ADMM for Large-Scale Radiotherapy Optimization](#Multi-GPU-Based-ADMM:-Implement-Scalable-and-Fast-ADMM-Algorithms-for-Large-Scale-Radiotherapy-Optimization)

---

## Interactive and User-Friendly Visualization for Dose-Volume Histograms (DVH)

**Requirements:** Matplotlib, Plotly (or alternative)  
**Good to Know:** Dash, Panel (or alternative)  

### Short Description
_What is DVH?_

A DVH is a convenient two-dimensional (2D) plot for plan evaluation and can be easily calculated from the 3D delivered dose. It shows how much of a structure (volume) gets a specific radiation dose (Gy) .The x-axis shows the dose (in Gray). The y-axis shows the percentage of the volume of the structure receiving that dose.

PortPy currently does visualization using Matplotlib. We would like to create an interactive visualization using Plotly (or an alternative). We would also like the visualization to work in both Jupyter Notebook and  Desktop versions

![Dose-Volume Histogram Example](../images/dvh-example.png)
### Project Outcome
- Interactive DVH line plots.
- Ability to select structures through an interactive checkbox.
- Build, visualize, and interpret DVHs using provided data.

---

## Enhancing Dose Distribution Analysis through User-Friendly Visualization Tools

**Requirements:** Matplotlib, Plotly (or alternative)  
**Good to Know:** Dash (or alternative)  

### Short Description
_What is dose distribution?_

A spatial map that shows how radiation dose is spread across the patient body and can be visualized as 2d grid. It consist of slice of CT image, structure contours and dose as color wash on top of CT with some opacity. This project would create interactive 2d slice views of patient geometry with dose distribution

PortPy currently does visualization using Matplotlib. We would like to create an interactive visualization using Plotly (or an alternative). We would also like the visualization to work in both Jupyter Notebook and  Desktop versions

![Dose-Distribution Example](../images/dose_distribution.png)

### Project Outcome
- View and explore dose maps interactively.
- Overlay structure contours on dose maps.
- Gain hands-on experience with medical imaging visualization.

---

## User-Friendly Interactive Dashboard for PortPy Data Visualization with Dynamic Tables

**Requirements:** Matplotlib, Plotly (or alternative)  
**Good to Know:** Dash (or alternative)  

### Short Description
_What does PortPy Data consist of?_

PortPy consist of two types of data i.e. **metadata** which are small size json files and **data** which are huge size **hdf5** files. This project will help users to visualize the metadata which is in **hierarchical** format as interactive table

![Dashboard Example](../images/dashboard.png)
**Metadata** is displayed as a static Pandas DataFrame, which limits interactivity and exploration. We would like to create an interactive dashboard using Plotly (or an alternative). We would also like the visualization to work in both Jupyter Notebook and  Desktop versions

### Project Outcome
- Transform static metadata tables into dynamic, interactive dashboards.
- Enable search, filter, and expand capabilities for metadata exploration.

---

## Interactive Visualization of Multi-Leaf Collimator (MLC) Movements for Treatment Plans

**Requirements:** Matplotlib, Plotly (or alternative)  
**Good to Know:** Dash (or alternative)  

### Short Description
_What is MLC?_

An **MLC** is a key component in radiotherapy machines used to shape radiation beams. It consists of movable metal leaves that block parts of the beam, ensuring the dose conforms to the tumor shape while sparing healthy tissue.

Current state: MLC movements are displayed as static visualizations, which limit interactivity and analysis. We would like to create an interactive visualization using Plotly (or an alternative). We would also like the visualization to work in both Jupyter Notebook and  Desktop versions
![MLC Example](../images/MLC.png)

### Project Outcome
- Animate MLC movements across beam angles.
- Overlay targets and structures for better analysis.

---

## Creating a Simple Website for PortPy

**Requirements:** Markdown, reStructuredText, Sphinx  
**Good to Know:** HTML, CSS, JavaScript  

### Short Description
Design and build a simple website for PortPy using modern web technologies.

![Website Example](../images/web_1.png)
![Website Example](../images/web_2.png)
![Website Example](../images/web_3.png)
![Website Example](../images/web_4.png)
![Website Example](../images/web_5.png)

### Project Outcome
- Create a visually appealing and user-friendly website.
- Gain hands-on experience with web development.
---

## Implementing Top-Performing Dose Prediction Model (Cascade 3D U-Net) from the Open-Access Grand Challenge

**Requirements:** Proficiency in PyTorch, GPU-based training  
**Good to Know:** TensorFlow, Keras, medical imaging concepts  

### Short Description
This project focuses on integrating the winning Cascade 3D U-Net model from the open-access grand challenge into the PortPy framework. The task involves training and evaluating the model on the PortPy dataset, ensuring optimal performance for radiotherapy dose prediction. The implementation should align with PortPy's standards for usability and extensibility, contributing to advanced dose prediction workflows.

### Project Outcome
- Train and implement a state-of-the-art dose prediction model.
- Enhance workflows for radiotherapy dose prediction.

---

## Build dose prediction using advanced U-Net architecture Dilated U-Net (Runner-Up Model for Open-Access Grand Challenge)

**Requirements:** Proficiency in PyTorch, GPU-based training  
**Good to Know:** TensorFlow, Keras, medical imaging concepts  

### Short Description
This project focuses on integrating the runner up Dilated U-Net model from the open-access grand challenge into the PortPy framework. The task involves training and evaluating the model on the PortPy dataset, ensuring optimal performance for radiotherapy dose prediction. The implementation should align with PortPy's standards for usability and extensibility, contributing to advanced dose prediction workflows.

### Project Outcome
- Develop an advanced dose prediction model.
- Gain experience in radiotherapy and AI techniques.

---

## Implement Feature-Based Dose Prediction (Runner-Up Model): Use feature-based losses and One Cycle Learning for enhanced accuracy


**Requirements:** Proficiency in PyTorch, GPU-based training  
**Good to Know:** TensorFlow, Keras, medical imaging concepts  

### Short Description
This project focuses on integrating the runner model based on feature-based losses and one cycle learning from the open-access grand challenge into the PortPy.AI framework. The task involves training and evaluating the model on the PortPy dataset, ensuring optimal performance for radiotherapy dose prediction. The implementation should align with PortPy's standards for usability and extensibility, contributing to advanced dose prediction workflows.

### Project Outcome
- Implement and evaluate feature-based dose prediction models.
- Enhance accuracy in radiotherapy dose predictions.

---

## Gradient-Based Optimization: Use JAX Auto-Diff for Radiotherapy Optimization with Gradient Descent

**Requirements:** Proficiency in Python, familiarity with JAX  
**Good to Know:** Optimization techniques, NumPy, SciPy  

### Short Description
This project aims to leverage JAX's automatic differentiation capabilities to implement gradient-based optimization for radiotherapy treatment planning. The focus will be on developing efficient optimization pipelines using gradient descent.

### Project Outcome
- Develop a scalable and efficient framework for gradient-based radiotherapy optimization.
- Implement gradient descent using JAX for dose optimization tasks.
- Demonstrate improvements in computation time and plan quality through gradient-based techniques.
- Provide insights into the impact of gradient-based methods on clinical treatment planning workflows.
- Deliver a reproducible Python-based implementation integrated into the PortPy framework.


---

## Multi-GPU-Based ADMM: Implement Scalable and Fast ADMM Algorithms for Large-Scale Radiotherapy Optimization

**Requirements:** Proficiency in Python, multi-GPU programming  
**Good to Know:** JAX, CUDA, PyTorch, optimization techniques  

### Short Description
This project focuses on developing scalable and efficient ADMM (Alternating Direction Method of Multipliers) algorithms tailored for large-scale radiotherapy optimization problems. Utilizing multi-GPU systems, the implementation will achieve faster convergence and enhanced scalability, enabling solutions to complex radiotherapy optimization tasks.

### Project Outcome
- Demonstrate scalability and speed improvements for large-scale radiotherapy optimization problems.
- Benchmark the ADMM implementation against existing optimization methods.
- Deliver a Python-based implementation compatible with existing radiotherapy frameworks, such as PortPy.
- Gain insights into the role of parallelized ADMM in solving real-world optimization challenges in radiotherapy