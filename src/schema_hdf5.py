# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2015, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import tables

class BayesdbApplication(tables.IsDescription):
    id = tables.IntCol(pos=1)

class BayesdbUserVersion(tables.IsDescription):
    user_version = tables.IntCol(pos=1)

class BayesdbMetamodel(tables.IsDescription):
    name = tables.StringCol(512, pos=1)
    version = tables.StringCol(512, pos=2)


class BayesdbStatType(tables.IsDescription):
    name = tables.StringCol(512, pos=1)

class BayesdbColumn(tables.IsDescription):
    tabname = tables.StringCol(512, pos=1)
    colno = tables.IntCol(pos=2)
    name = tables.StringCol(1024, pos=3)
    shortname = tables.StringCol(512, pos=4)
    description = tables.StringCol(4096, pos=5)

class BayesdbColumnMap(tables.IsDescription):
    tabname = tables.StringCol(512, pos=1)
    colno = tables.IntCol(pos=2)
    key = tables.StringCol(512, pos=3)
    value = tables.StringCol(512, pos=4)

class BayesdbGenerator(tables.IsDescription):
    id = tables.IntCol(pos=1)
    name = tables.StringCol(512, pos=2)
    tabname = tables.StringCol(512, pos=3)
    metamodel = tables.IntCol(pos=4)
    defaultp = tables.BoolCol()

class BayesdbGeneratorColumn(tables.IsDescription):
    generator_id = tables.IntCol(pos=1)
    colno = tables.IntCol(pos=2)
    stattype = tables.StringCol(512, pos=3, dflt=False)

class BayesdbGeneratorModel(tables.IsDescription):
    generator_id = tables.IntCol(pos=1)
    modelno = tables.IntCol(pos=2)
    iterations = tables.IntCol(pos=3)

class BayesdbSession(tables.IsDescription):
    id = tables.IntCol(pos=1)
    sent = tables.BoolCol(pos=2, dflt=False)
    version = tables.StringCol(512, pos=3)

class BayesdbSessionEntries(tables.IsDescription):
    id = tables.IntCol(pos=1)
    session_id = tables.IntCol(pos=2)
    type = tables.StringCol(512, pos=3)
    data = tables.StringCol(100000, pos=4)
    start_time = tables.IntCol(pos=5)
    end_time = tables.IntCol(pos=6)
    error = tables.StringCol(100000, pos=7)

bayesdb_schema_5 = '''
INSERT INTO bayesdb_stattype VALUES ('categorical');
INSERT INTO bayesdb_stattype VALUES ('cyclic');
INSERT INTO bayesdb_stattype VALUES ('cyclic');
'''


### BayesDB PyTables setup

def bayesdb_install_schema(db, version=None, compatible=None):

    db.hdf_store.create_table('/', 'bayesdb_metamodel', BayesdbMetamodel, "BayesDb metamodels")
    tbl = db.hdf_store.create_table('/', 'bayesdb_stattype', BayesdbStatType, "BayesDb stattypes")
    for stattype in ['categorical', 'cyclic', 'cyclic']:
        row = tbl.row
        row['name'] = stattype
        row.append()

    tbl = db.hdf_store.create_table('/', 'bayesdb_column', BayesdbColumn, "BayesDb column")
    tbl.cols.tabname.create_index()
    tbl.cols.colno.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_column_map', BayesdbColumnMap, "BayesDb column map")
    tbl.cols.tabname.create_index()
    tbl.cols.colno.create_index()
    tbl.cols.key.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_generator', BayesdbGenerator, "BayesDb generator")
    tbl.cols.id.create_index()
    tbl.cols.defaultp.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_generator_column', BayesdbGeneratorColumn, "BayesDb generator column")
    tbl.cols.generator_id.create_index()
    tbl.cols.colno.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_generator_model', BayesdbGeneratorModel, "BayesDb generator model")
    tbl.cols.generator_id.create_index()
    tbl.cols.modelno.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_session', BayesdbSession, "BayesDb session")
    tbl.cols.id.create_index()

    tbl = db.hdf_store.create_table('/', 'bayesdb_session_entries', BayesdbSessionEntries, "BayesDb session entries")
    tbl.cols.session_id.create_index()


