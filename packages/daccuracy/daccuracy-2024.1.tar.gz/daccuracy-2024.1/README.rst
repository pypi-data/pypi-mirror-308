..
   Copyright CNRS/Inria/UniCA
   Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2019
   SEE COPYRIGHT NOTICE BELOW

.. |PROJECT_NAME|      replace:: DAccuracy
.. |SHORT_DESCRIPTION| replace:: Detection and Segmentation Accuracy Measures

.. |PYPI_NAME_LITERAL| replace:: ``daccuracy``
.. |PYPI_PROJECT_URL|  replace:: https://pypi.org/project/daccuracy/
.. _PYPI_PROJECT_URL:  https://pypi.org/project/daccuracy/

.. |DOCUMENTATION_URL| replace:: https://src.koda.cnrs.fr/eric.debreuve/daccuracy/-/wikis/home
.. _DOCUMENTATION_URL: https://src.koda.cnrs.fr/eric.debreuve/daccuracy/-/wikis/home

.. |DEPENDENCIES_MANDATORY| replace:: matplotlib, numpy, scikit-image, scipy
.. |DEPENDENCIES_OPTIONAL|  replace:: None



===================================
|PROJECT_NAME|: |SHORT_DESCRIPTION|
===================================



Documentation
=============

After installation, the ``daccuracy`` command should be available from a command-line console.
The usage help is obtained with ``daccuracy --help`` (see **Usage Help** below).


Input Formats
-------------

The ground-truth can be specified through a CSV file, a labeled image, or a labeled Numpy array. The detection can be specified through a labeled image or a labeled Numpy array. A labeled image or Numpy array must have the background labeled with zero, with the objects labeled consecutively from 1.

.. note::
    The input images are requested to be labeled (as opposed to binary: zero for the background and 1 for any of the objects) in order to be able to deal with tangent objects. With a binary image, there is no way to distinguish a unique object from a set of tangent objects.

In CSV format, the ground-truth must be specified as one row per object where ``n`` columns (the first ``n`` ones by default) correspond to the row, column, and remaining ``n-2`` coordinates of the object center. Note that these coordinates can have floating-point values (as opposed to being restricted to integers). See the usage help below for details.

Example CSV::

    1.2, 2.3
    3.4, 4.5

This specifies two ground-truth object centers in dimension 2, the first one being at row 1.2 and column 2.3. Alternatively, the center coordinates can be passed in x/y coordinate system. See the usage help below for details.


Accuracy Measures
-----------------

The following accuracy measures are computed:

- Number of ground-truth objects
- Number of detected objects
- Number of true positives, false positives, and false negatives
- Precision, recall, and F1 score
- Free-response Receiver Operating Characteristic (FROC) curve sample: named ``froc_sample`` and corresponding to the tuple (false positives, true positive rate)
- Values for measure correctness checking: ``check_tp_fn_equal_gt`` (true_positives + false_negatives ?=? ground-truths) and ``check_tp_fp_equal_dn`` (true_positives + false_positives ?=? detections)

Additionally, if the ground-truth has been passed as an image or a Numpy array, the mean, standard deviation, minimum, and maximum of the following measures are also computed:

- Ground-truth/detection overlap (as a percentage with respect to the smaller region among ground-truth and detection)
- Ground-truth/detection Jaccard index
- Pixel-wise precision, recall, and F1 score


Output Formats
--------------

See usage help below.


Usage Help (``daccuracy --help``)
---------------------------------

Usage Help::

    usage: daccuracy [-h] --gt ground_truth --dn detection [--shifts Dn_shift Dn_shift] [-e] [-t TOLERANCE] [-f {csv,nev}]
                     [-o Output file] [-s]

    3 modes:
        - one-to-one: one ground-truth (csv, image, or Numpy array) vs. one detection (image or Numpy array)
        - one-to-many: one ground-truth vs. several detections (folder of detections)
        - many-to-many: several ground-truths (folder of ground-truths) vs. corresponding detections (folder of detections)

    In many-to-many mode, each detection file must have a counterpart ground-truth file with the same name, but not
    necessarily the same extension.

    With 8-bit image formats, ground-truth and detection cannot contain more than 255 objects. If they do, they could be
    saved using higher-depth formats. However, it is recommended to save them in NPY or NPZ Numpy formats instead.

    optional arguments:
      -h, --help            show this help message and exit
      --gt ground_truth     Ground-truth CSV file of centers or labeled image or labeled Numpy array, or ground-truth folder;
                            If CSV, --rAcB (or --xAyB) can be passed additionally to indicate that columns A and B contain
                            the centers' rows and cols, respectively (or x's and y's in x/y mode). Columns must be specified
                            as (possibly sequences of) uppercase letters, as is usual in spreadsheet applications. For
                            ground-truths of dimension "n" higher than 2, the symbol "+" must be used for the remaining
                            "n-2" dimensions. For example, --rAcB+C+D in dimension 4.
      --relabel-gt {seq,full}
                            If present, this option instructs to relabel the ground-truth
                            sequentially.
      --dn detection        Detection labeled image or labeled Numpy array, or detection folder.
      --relabel-gt {seq,full}
                            If present, this option instructs to relabel the ground-truth
                            sequentially.
      --shifts Dn_shift [Dn_shift ...]
                            Vertical (row), horizontal (col), and higher dimension shifts to apply to detection. Default:
                            all zeroes.
      -e, --exclude-border  If present, this option instructs to discard objects touching image border, both in ground-truth
                            and detection.
      -t TOLERANCE, --tol TOLERANCE, --tolerance TOLERANCE
                            Max ground-truth-to-detection distance to count as a hit (meant to be used when ground-truth is
                            a CSV file of centers). Default: zero.
      -f {csv,nev}, --format {csv,nev}
                            nev: one "Name = Value"-row per measure; csv: one CSV-row per ground-truth/detection pairs.
                            Default: "nev".
      -o Output file        CSV file to store the computed measures or "-" for console output. Default: console output.
      -s, --show-image      If present, this option instructs to show an image superimposing ground-truth onto detection.
                            It is actually done only for 2-dimensional images.



Installation
============

This project is published
on the `Python Package Index (PyPI) <https://pypi.org/>`_
at: |PYPI_PROJECT_URL|_.
It should be installable from Python distribution platforms or Integrated Development Environments (IDEs).
Otherwise, it can be installed from a command console using `pip <https://pip.pypa.io/>`_:

+--------------+-------------------------------------------------------+----------------------------------------------------------+
|              | For all users (after acquiring administrative rights) | For the current user (no administrative rights required) |
+==============+=======================================================+==========================================================+
| Installation | ``pip install`` |PYPI_NAME_LITERAL|                   | ``pip install --user`` |PYPI_NAME_LITERAL|               |
+--------------+-------------------------------------------------------+----------------------------------------------------------+
| Update       | ``pip install --upgrade`` |PYPI_NAME_LITERAL|         | ``pip install --user --upgrade`` |PYPI_NAME_LITERAL|     |
+--------------+-------------------------------------------------------+----------------------------------------------------------+



Dependencies
============

The development relies on several packages:

- Mandatory: |DEPENDENCIES_MANDATORY|
- Optional:  |DEPENDENCIES_OPTIONAL|

The mandatory dependencies, if any, are installed automatically by `pip <https://pip.pypa.io/>`_, if they are not already, as part of the installation of |PROJECT_NAME|.
Python distribution platforms or Integrated Development Environments (IDEs) should also take care of this.
The optional dependencies, if any, must be installed independently by following the related instructions, for added functionalities of |PROJECT_NAME|.



Brief Description
=================

``DAccuracy`` (Detection Accuracy) allows to compute

- some accuracy measures
- on an N-dimensional detection or segmentation image
- when the ground-truth is available as a `CSV file <https://en.wikipedia.org/wiki/Comma-separated_values>`_, an image, or a `Numpy <https://numpy.org/>`_ file.

It works in 3 contexts:

- one-to-one: single ground-truth, single detection image;
- one-to-many: unique ground-truth, several detection images (typically obtained by various methods);
- many-to-many: set of "(ground-truth, detection image)" pairs.

.. note::
    **With 8-bit image formats**, ground-truth and detection **cannot contain more than 255 objects**. If they do, they could be saved using higher-depth formats. However, it is recommended to save them in `NPY <https://numpy.org/doc/stable/reference/generated/numpy.save.html>`_ or `NPZ <https://numpy.org/doc/stable/reference/generated/numpy.savez_compressed.html>`_ Numpy formats instead. Note that using Numpy arrays does not remove the limit on the number of objects, but with the `uint64 dtype <https://numpy.org/doc/stable/reference/arrays.scalars.html#numpy.uint64>`_, the limit goes up to close to 2e19 objects. See a note below as to why ground-truth and detection are requested to be labeled (which raises this issue), as opposed to binary (which a priori would not).

Example console output (accuracy measures can also be written to a CSV file)::

            Ground truth = ground-truth.csv
               Detection = detection.png
         N ground truths = 55
            N detections = 47
           True_positive = 43
          False_positive = 4
          False_negative = 12
               Precision = 0.9148936170212766
                  Recall = 0.7818181818181819
                F1_score = 0.8431372549019609
             Froc_sample = (4, 0.7818181818181819)
    Check_tp_fn_equal_gt = 55
    Check_tp_fp_equal_dn = 47



Acknowledgments
===============

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

The project is developed with `PyCharm Community <https://www.jetbrains.com/pycharm/>`_.

The code is formatted by `Black <https://github.com/psf/black/>`_, *The Uncompromising Code Formatter*.

The imports are ordered by `isort <https://github.com/timothycrosley/isort/>`_... *your imports, so you don't have to*.

..
  COPYRIGHT NOTICE

  This software is governed by the CeCILL  license under French law and
  abiding by the rules of distribution of free software.  You can  use,
  modify and/ or redistribute the software under the terms of the CeCILL
  license as circulated by CEA, CNRS and INRIA at the following URL
  "http://www.cecill.info".

  As a counterpart to the access to the source code and  rights to copy,
  modify and redistribute granted by the license, users are provided only
  with a limited warranty  and the software's author,  the holder of the
  economic rights,  and the successive licensors  have only  limited
  liability.

  In this respect, the user's attention is drawn to the risks associated
  with loading,  using,  modifying and/or developing or reproducing the
  software by the user in light of its specific status of free software,
  that may mean  that it is complicated to manipulate,  and  that  also
  therefore means  that it is reserved for developers  and  experienced
  professionals having in-depth computer knowledge. Users are therefore
  encouraged to load and test the software's suitability as regards their
  requirements in conditions enabling the security of their systems and/or
  data to be ensured and,  more generally, to use and operate it in the
  same conditions as regards security.

  The fact that you are presently reading this means that you have had
  knowledge of the CeCILL license and that you accept its terms.

  SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

  This software is being developed by Eric Debreuve, a CNRS employee and
  member of team Morpheme.
  Team Morpheme is a joint team between Inria, CNRS, and UniCA.
  It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
  I3S, and Laboratory iBV.

  CNRS: https://www.cnrs.fr/index.php/en
  Inria: https://www.inria.fr/en/
  UniCA: https://univ-cotedazur.eu/
  Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
  I3S: https://www.i3s.unice.fr/en/
  iBV: http://ibv.unice.fr/
  Team Morpheme: https://team.inria.fr/morpheme/
