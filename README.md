# From Mechanism to Practice: Evolutionary Forecasting for SARS-CoV-2
**Marlin Figgins**<sup>1,2</sup>

<sup>1</sup> *Department of Applied Mathematics, University of Washington, Seattle, WA, USA*
<sup>2</sup> *Vaccine and Infectious Disease Division, Fred Hutchinson Cancer Research Center, Seattle, WA, USA*


## Overview

This repository contains the full text of my PhD dissertation:

**From Mechanism to Practice: Evolutionary Forecasting for SARS-CoV-2**

It presents theoretical, statistical, and operational tools for understanding and predicting viral evolution with a focus on SARS-CoV-2.

## Abstract

Novel genetic variants often arise due to mutations in circulating viral populations. 
These mutations can sometimes provide fitness advantages to members of the population allowing them to out-compete other variants through mechanisms such as partial immune escape and increased transmissibility.
This interplay of mutation, transmission, and selection leads to evolution in the population.
Therefore, understanding the genetic composition of viral populations and its relation to virus phenotype can be useful for understanding the current and future epidemic potential of viral variants.

This dissertation develops several theoretical ideas, statistical methods, and software tools that enable evolutionary forecasting for SARS-CoV-2 and other rapidly evolving pathogens using concepts from population genetics, mathematical epidemiology, and statistics.

We begin by developing a Bayesian method for estimating the effective reproduction number of genetic variants using counts of variant sequences and measures of incidence such as case counts.

To evaluate this method among others, we develop a workflow to compare frequency-based forecast models in a live forecasting environment, quantifying the short-term accuracy of such methods and suggesting a minimal sequencing capacity to ensure high quality forecasts.

Next, we develop a larger theory for how mechanistic models of transmission constrain how variant frequencies change over time.
This leads to theoretical results for the trade-off between immune escape and increased transmissibility and suggests new methods for modeling variant fitness using approximate Gaussian processes as well as latent pseudo-immune factors.

We then apply these ideas to incorporate molecular data on immune escape and phylogenetic structure into relative fitness estimates to enable out-of-sample prediction of relative fitness from sequence-level predictors.

Our focus then shifts to the operational problem of evolutionary forecasting, where we develop open-source software and visualization tools that can be used to implement, automate, and interpret evolutionary forecasts.

## Citation

```bibtex
@phdthesis{figgins2024EvoForecasting,
  title        = {From Mechanism to Practice: Evolutionary Forecasting for {SARS-CoV-2}},
  author       = {Figgins, Marlin D.},
  year         = 2024,
  month        = {December},
  school       = {University of Washington},
  type         = {PhD thesis}
}
```
