================================================
KaiTian: High-level Package for Machine Learning
================================================

KaiTian is a high-level package for machine learning. It provides a simple and
intuitive interface for users to train and evaluate machine learning models.
It also provides a variety of tools for data preprocessing, model selection,
and model saving & loading.

🏗️ Install KaiTian in Specific Environment
==========================================

In general, the new release of KaiTian will be uploaded to pypi, you can 
install KaiTian simply with:

.. code-block:: bash
    
    pip install kaitian

To install KaiTian in Kaggle notebook offline, you need to upload the `.whl` file as 
a dataset and execute:

.. code-block:: bash
    
    pip install --no-index -q /kaggle/input/{dataset}/{kaitian_version.whl}

All the requriements of KaiTian are alrealy included in Kaggle environment, 
so you don't need try to find them while installing.

If you do need to install KaiTian with some updated requriements, try this:

.. code-block:: bash
    
    pip install --no-index -q --find-links /path/to/requriements/pkgs /kaggle/input/{dataset}/{kaitian_version.whl}

