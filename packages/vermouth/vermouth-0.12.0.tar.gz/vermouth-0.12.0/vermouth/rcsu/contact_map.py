# Copyright 2023 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Read RCSU Go model contact maps.
"""

def read_go_map(file_path):
    """
    Read a RCSU contact map from the c code as published in
    doi:10.5281/zenodo.3817447. The format requires all 
    contacts to have 18 columns and the first column to be 
    a capital R.

    Parameters
    ----------
    file_path: :class:`pathlib.Path`
        path to the contact map file

    Returns
    -------
    list(tuple)
        contact as chain id, res id, chain id, res id
    """
    with open(file_path, "r", encoding='UTF-8') as _file:
        contacts = []
        for line in _file:
            tokens = line.strip().split()
            if len(tokens) == 0:
                continue

            if tokens[0] == "R" and len(tokens) == 18:
                # this is a bad place to filter but follows
                # the old script
                if tokens[11] == "1" or (tokens[11] == "0" and tokens[14] == "1"):
                    # this is a OV or rCSU contact we take it
                    contacts.append((int(tokens[5]), tokens[4], int(tokens[9]), tokens[8]))

        if len(contacts) == 0:
            raise IOError("You contact map is empty. Are you sure it has the right formatting?")

    return contacts
