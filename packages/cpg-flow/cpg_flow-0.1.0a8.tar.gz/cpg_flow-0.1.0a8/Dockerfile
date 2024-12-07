FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest

RUN pip install metamist
COPY README.md .
COPY src/cpg_flow cpg_flow
RUN pip install .
