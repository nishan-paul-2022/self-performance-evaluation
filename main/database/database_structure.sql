CREATE TABLE main_academic (
    id int NOT NULL,
    year text NOT NULL,
    event text NOT NULL,
    weight text NOT NULL,
    value text NOT NULL
);

CREATE TABLE main_daily (
    id int NOT NULL,
    day text NOT NULL,
    n2021 text NOT NULL,
    n2022 text NOT NULL DEFAULT '0'
);

CREATE TABLE main_imonlyhuman (
    id int NOT NULL,
    name text NOT NULL,
    classname text NOT NULL,
    time text NOT NULL,
    value text NOT NULL DEFAULT '10'
);

CREATE TABLE main_undergraduate (
    id int NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    credit text NOT NULL,
    grade text NOT NULL,
    gpa text NOT NULL,
    level text NOT NULL
);

CREATE TABLE main_value_year_a (
    id int NOT NULL,
    year text NOT NULL,
    event text NOT NULL,
    book text NOT NULL,
    routine_2am_7am text NOT NULL,
    writing text NOT NULL,
    study_time text NOT NULL,
    response_teacher text NOT NULL,
    response_friend text NOT NULL
);

CREATE TABLE main_value_year_b (
    id int NOT NULL,
    year text NOT NULL,
    event text NOT NULL,
    pro_contest text NOT NULL,
    pro_solving text NOT NULL,
    algorithm text NOT NULL,
    soft_developing text NOT NULL,
    research text NOT NULL,
    software text NOT NULL,
    online_course text NOT NULL
);

CREATE TABLE main_weight_year_a (
    id int NOT NULL,
    parameter text NOT NULL,
    n2004 text NOT NULL,
    n2005 text NOT NULL,
    n2006 text NOT NULL,
    n2007 text NOT NULL,
    n2008 text NOT NULL,
    n2009 text NOT NULL,
    n2010 text NOT NULL,
    n2011 text NOT NULL,
    n2012 text NOT NULL,
    n2013 text NOT NULL,
    n2014 text NOT NULL,
    n2015 text NOT NULL,
    n2016 text NOT NULL,
    n2017 text NOT NULL,
    n2018 text NOT NULL,
    n2019 text NOT NULL,
    n2020 text NOT NULL,
    n2021 text NOT NULL,
    n2022 text NOT NULL
);

CREATE TABLE main_weight_year_b (
    id int NOT NULL,
    parameter text NOT NULL,
    n2017 text NOT NULL,
    n2018 text NOT NULL,
    n2019 text NOT NULL,
    n2020 text NOT NULL,
    n2021 text NOT NULL,
    n2022 text NOT NULL
);

ALTER TABLE main_academic
  ADD PRIMARY KEY (id);

ALTER TABLE main_daily
  ADD PRIMARY KEY (id);

ALTER TABLE main_imonlyhuman
  ADD PRIMARY KEY (id);

ALTER TABLE main_undergraduate
  ADD PRIMARY KEY (id);

ALTER TABLE main_value_year_a
  ADD PRIMARY KEY (id);

ALTER TABLE main_value_year_b
  ADD PRIMARY KEY (id);

ALTER TABLE main_weight_year_a
  ADD PRIMARY KEY (id);

ALTER TABLE main_weight_year_b
  ADD PRIMARY KEY (id);