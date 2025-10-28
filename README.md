# Can current open source guardrails defend against internal agentic risks?

During the summer of 2025, one of the Builder's in Residence wanted to see if current open source guardrails could defend against specific internal agentic risks. This is because the [risk surface of agents is greater than that of LLMs](https://arxiv.org/pdf/2504.19956). In other words, we don't just have to worry about user inputs and model outputs. The communication between different components within agents contains risks as well.

The below describes how to run our experiments and analyze our data.

# Environment Setup

We recommend using `uv` to setup your environment. Run the following command:

```
uv sync
source .venv/bin/activate
```

# Running our experiments

For all of our experiments, we used an H100 GPU. However, a high powered MacBook Pro or other equivalent machine should be fine. To run our experiments, run `jupyter lab` on the command line (after activating the environment) and access the following notebooks:

```
IPIA_Experiments.ipynb
Function_Calling_Experiments.ipynb
```

Those will allow you rerun our experiments and obtain the raw results.

# Analyzing our data

If you would rather read through our data and results, we recommend using our notebooks to get the metrics we produce in our blog post <WILL LINK TO BLOG POST>. To do so, run `jupyter lab` on the command line and access the following notebooks:

```
IPIA_Analysis.ipynb
Function_Calling_Analysis.ipynb
```


