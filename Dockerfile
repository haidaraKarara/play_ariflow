FROM quay.io/astronomer/astro-runtime:11.2.0

# As we will develop in a Dev Container with VsCode, we decide to install the airbyte package from here
# The auto-completion didn't work after installing it directly with pip inside docker container.
# To fix that, we do this.

RUN pip install apache-airflow-providers-airbyte

USER root

RUN cp -r /home/astro/.local/lib/python3.11/site-packages/* /usr/local/lib/python3.11/site-packages/

USER astro